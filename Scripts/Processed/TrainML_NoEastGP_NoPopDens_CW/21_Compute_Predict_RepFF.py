import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv
import tensorflow as tf
import shap
shap.initjs()

####################################################################################
# CODE DESCRIPTION
# 21_Compute_Predict_RepFF.py predicts the probabilities of having a flash flood event in a given 
# grid-box. 
# Runtime: the script can take up to 30 minutes to compute in serial.

# INPUT PARAMETERS DESCRIPTION
# Date_S (date): start date for the verification period.
# Date_F (date): final date for the verification period.
# Acc (integer, in hours): accumulation period.
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# Years_Train (string): years covered in the training dataset.
# Specification_PDT (string): specification of the dataset (PDT) used  for training.
# Git_Repo (string): repository's local path
# FileIN_Mask (string): relative path where the USA's mask is stored.
# FileIN_slor (string): relative path of the file containg the slop of the sub-grid orography.
# FileIN_stdor (string): relative path of the file containg the standar deviation of the sub-grid orography.
# DirIN_RainThr (string): relative path of the directory containg the rainfall thresholds.
# DirIN_Rain (string): relative path of the directory containg the rainfall analysis.
# DirIN_SS (string): relative path of the directory containg the percentage of soil moisture.
# DirIN_TrainML (string): relative path of the directory containing the training dataset.
# DirIN_ML (string): relative path of the directory containg the weights for the ML model.
# DirOUT (string): relative path containing the ML predictions.

# INPUT PARAMETERS
Date_S = datetime(2021,1,1)
Date_F = datetime(2021,12,31)
Acc = 12
Mask_Domain = [22,-130,52,-60]
Years_Train = "2005_2020"
Specification_PDT = "NoEastGP_NoPopDens_CW"
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
FileIN_slor = "Data/Raw/Analysis/ENS_9km/slor/slor.grib"
FileIN_stdor = "Data/Raw/Analysis/ENS_9km/sdor/sdor.grib"
DirIN_RainThr = "Data/Raw/Analysis/ERA5_ecPoint/tp_climate"
DirIN_Rain = "Data/Raw/Analysis/ERA5_ecPoint/tp"
DirIN_SS = "Data/Compute/07_Percentage_Soil_Saturation"
DirIN_TrainML = "Data/Compute/19_Combine_PDT"
DirIN_ML = "Data/Compute/20_TrainML"
DirOUT = "Data/Compute/21_Predict_RepFF"
####################################################################################

# Import the ML model
model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(4,)),  # Input layer specifying the input shape
    tf.keras.layers.Dense(4, activation=tf.nn.relu),  # First hidden dense layer with ReLU activation
    tf.keras.layers.Dense(4, activation=tf.nn.relu),  # Second hidden dense layer with ReLU activation
    tf.keras.layers.Dense(2, activation=tf.nn.softmax)  # Output Dense layer with Softmax activation
    ])

FileIN = Git_Repo + "/" + DirIN_ML + "/" + Specification_PDT + "_" + Years_Train + "/weights"
model.load_weights(FileIN)

model.compile(
    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss = tf.keras.losses.CategoricalCrossentropy(),
    metrics = [tf.keras.metrics.CategoricalAccuracy(name = "accuracy")],
    )

# # Creating explainer for the computation of shap values
# train = np.load(Git_Repo + "/" + DirIN_TrainML + "/pdt_" + Specification_PDT + "_" + Years_Train + ".npy")
# train = train[:,1:]
# explainer = shap.Explainer(model, train)

# Reading domain's mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask_lats = mv.latitudes(mask)
mask_lons = mv.longitudes(mask)
mask_vals = mv.values(mask)
mask_index = np.where(mask_vals == 1)[0]
mask_lats = mask_lats[mask_index]
mask_lons = mask_lons[mask_index]

# Reading slor and extracting the nearest values to the mask grid-points 
slor = mv.read(Git_Repo + "/" + FileIN_slor)
slor_mask = mv.nearest_gridpoint(slor, mask_lats, mask_lons).reshape(-1, 1)

# Reading sdor and extracting the nearest values to the mask grid-points 
stdor = mv.read(Git_Repo + "/" + FileIN_stdor)
stdor_mask = mv.nearest_gridpoint(stdor, mask_lats, mask_lons).reshape(-1, 1)

# Reading the predictors that are time-dipendent
TheDate = Date_S
while TheDate <= Date_F:

      for EndPeriod in range(0+Acc, 24+1, Acc): 

            TheDateTime = TheDate + timedelta(hours=EndPeriod)

            print("Creating prediction for: " + TheDateTime.strftime("%Y%m%d%H"))

            # Reading the percentage of soil moisture and extracting the nearest values to the mask grid-points 
            DateTime_Final_ss = TheDateTime - timedelta(days=1) # selecting the soil saturation percentage for an antecedent period of time compared to when the rainfall fell (i.e., 24 hours)
            FileIN_SS = Git_Repo + "/" + DirIN_SS + "/" + DateTime_Final_ss.strftime("%Y") + "/" + DateTime_Final_ss.strftime("%Y%m%d") + "/soil_saturation_perc_" + DateTime_Final_ss.strftime("%Y%m%d%H") + ".grib"
            ss = mv.read(FileIN_SS)
            ss_mask = mv.nearest_gridpoint(ss, mask_lats, mask_lons).reshape(-1, 1)
            
            # Reading the rainfall analysis and categorizing it climatologically, and extracting the nearest values to the mask grid-points 
            FileIN_Rain = Git_Repo + "/" + DirIN_Rain + "/" + TheDate.strftime("%Y%m") + "/Pt_BC_PERC_" + TheDate.strftime("%Y%m%d") + "_" + f"{EndPeriod:02}" + ".grib2"
            tp = mv.read(FileIN_Rain)[-1]
            tp_mask = mv.nearest_gridpoint(tp, mask_lats, mask_lons).reshape(-1, 1)

            Perc_list = [99.8, 99.9, 99.95, 99.98, 99.99]
            RP_list = [1,2,5,10,20]
            tp_climate = mv.read(Git_Repo + "/" + DirIN_RainThr + "/tp_climate_12h_ERA5_ecPoint.grib")
            percs = np.load(Git_Repo + "/" + DirIN_RainThr + "/percs_computed_4_tp_climate.npy")
            
            tp_cat_mask = np.zeros(tp_mask.shape)
            for i in range(len(Perc_list)):

                  if i < len(Perc_list)-1:
                        
                        Perc1 = Perc_list[i]
                        Perc2 = Perc_list[i+1]
                        RP = RP_list[i]
                        
                        ind_perc1 = np.where(percs == Perc1)[0]
                        ind_perc2 = np.where(percs == Perc2)[0]
                        tp_thr1 = mv.nearest_gridpoint(tp_climate[ind_perc1], mask_lats, mask_lons).reshape(-1, 1)
                        tp_thr2 = mv.nearest_gridpoint(tp_climate[ind_perc2], mask_lats, mask_lons).reshape(-1, 1)
                        ind = np.where((tp_mask>=tp_thr1) & (tp_mask<tp_thr2))[0]
                        tp_cat_mask[ind] = RP
                        
                  else:
                        
                        Perc = Perc_list[i]
                        RP = RP_list[i]
                        
                        ind_perc = np.where(percs == Perc)[0]
                        tp_thr = mv.nearest_gridpoint(tp_climate[ind_perc], mask_lats, mask_lons).reshape(-1, 1)
                        ind = np.where(tp_mask>=tp_thr)[0]
                        tp_cat_mask[ind] = RP
                  
            # Building the predictors' table
            predictors = np.concatenate((tp_cat_mask, ss_mask, slor_mask, stdor_mask), axis=1)
            
            # Creating the predictions
            ff_pred_array = model.predict(predictors) * 100
            
            # Set to -1 the probabilities of having a flash flood report where there is no rainfall (to distinguish where the model gives 0 probabilities but there is rain)
            ind_tp0 = np.where(tp_cat_mask == 0)[0] 
            ff_pred_array[ind_tp0] = -1

            # # Computing the shap values for each prediction
            # shap = explainer(predictors)
            # shap_vals = shap.values

            # Encoding the predictions and the shap values in grib
            template = mask_vals * 0
            template[mask_index] = ff_pred_array[:,0]
            ff_pred_grib = mv.set_values(mask, template)

            # shap_vals_grib = None
            # for ind in range(shap_vals.shape[1]):
            #       template = mask_vals * 0
            #       template[mask_index] = shap_vals[:,ind,0]
            #       shap_vals_grib = mv.merge(shap_vals_grib, mv.set_values(mask, template))
            
            # Saving the grib files
            MainDirOUT = Git_Repo + "/" + DirOUT + "/" + Specification_PDT + "_" + Years_Train
            if not os.path.exists(MainDirOUT):
                  os.makedirs(MainDirOUT)
            FileOUT_prob = MainDirOUT + "/Prob_RepFF_" +  TheDateTime.strftime("%Y%m%d") + "_" + TheDateTime.strftime("%H") + ".grib"
            FileOUT_shap = MainDirOUT + "/Shap_Vals_" +  TheDateTime.strftime("%Y%m%d") + "_" + TheDateTime.strftime("%H") + ".grib"
            mv.write(FileOUT_prob, ff_pred_grib)
            # mv.write(FileOUT_shap, shap_vals_grib)
            
      TheDate = TheDate + timedelta(days=1)