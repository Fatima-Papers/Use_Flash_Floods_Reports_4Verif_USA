import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv
import tensorflow as tf
import shap
shap.initjs()

#############################################################################################################
# CODE DESCRIPTION
# 32_Compute_Shapley_Values.py computes the shapley values for the ANN predictions.
# Runtime: the script can take up to 10 hours to compute in serial.

# INPUT PARAMETERS DESCRIPTION
# Year (integer, in YYYY format): year to consider.
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# Git_Repo (string): repository's local path.
# FileIN_Mask (string): relative path of the file containing the domain's mask.
# FileIN_StdOrog (string): relative path of the file containing the standard deviation of the sub-grid orography.
# DirIN_ClassRP (string): relative path of the directory containing the return period class for the extreme ERA5-ecPoint rainfall analysis.
# DirIN_RatioEM (string): relative path of the directory containing the ratio between extreme and mean ERA5-ecPoint rainfall analysis.
# DirIN_PercSS (string): relative path of the directory containing the percentage of soil saturation.
# DirIN_LAI (string): relative path of the directory containing the leaf area index.
# DirIN_PD (string): relative path of the directory containing the regridded population density.
# DirIN_ANN (string): relative path of the directory containg the ANN's weights.
# DirOUT (string): relative path of the directory containing the probabilities of having a flash flood event in a given grid-box.

# INPUT PARAMETERS
Year = 2021
Acc = 12
Disc_Acc = 12
Mask_Domain = [22,-130,52,-60]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
FileIN_StdOrog = "Data/Raw/Analysis/ERA5/sdor/sdor.grib"
DirIN_ClassRP = "Data/Compute/07_ClassRP_AccTP"
DirIN_RatioEM = "Data/Compute/09_Ratio_Extreme_Mean_AccTP"
DirIN_PercSS = "Data/Compute/11_Percentage_Soil_Saturation"
DirIN_LAI = "Data/Raw/Analysis/ERA5/lai"
DirIN_PD = "Data/Compute/14_PopDens_Regrid/N320"
FileIN_PDT = "Data/Compute/26_Combine_PDT/AllFF/pdt_AllFF_NoPD_2005_2020.npy"
DirIN_ANN = "Data/Compute/27_Train_ANN/AllFF_2005_2020/NoPD"
DirOUT = "Data/Compute/32_Compute_Shapley_Values/AllFF_2005_2020/NoPD"
#############################################################################################################


# Importing the ANN model
if DirIN_ANN.split("/")[4] == "AllPred":
      Num_Pred = 6
else:
      Num_Pred = 5
model = tf.keras.Sequential([
      tf.keras.layers.InputLayer(input_shape=(Num_Pred,)),  # Input layer specifying the input shape
      tf.keras.layers.Dense(4, activation=tf.nn.relu),  # First hidden dense layer with ReLU activation
      tf.keras.layers.Dense(4, activation=tf.nn.relu),  # Second hidden dense layer with ReLU activation
      tf.keras.layers.Dense(2, activation=tf.nn.softmax)  # Output Dense layer with Softmax activation
      ])

FileIN = Git_Repo + "/" + DirIN_ANN + "/weights" 
model.load_weights(FileIN)

model.compile(
      optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3),
      loss = tf.keras.losses.CategoricalCrossentropy(),
      metrics = [tf.keras.metrics.CategoricalAccuracy(name = "accuracy")],
      )

# Creating explainer for the computation of shap values
train = np.load(Git_Repo + "/" + FileIN_PDT)
train = train[:,1:]
explainer = shap.Explainer(model, train)

# Reading domain's mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask_lats = mv.latitudes(mask)
mask_lons = mv.longitudes(mask)
mask_vals = mv.values(mask)
mask_index = np.where(mask_vals == 1)[0]
mask_lats = mask_lats[mask_index]
mask_lons = mask_lons[mask_index]

# Reading the stdor values within the considered domain
stdor = mv.values(mv.read(Git_Repo + "/" + FileIN_StdOrog))[mask_index].reshape(-1, 1)

# Reading the predictors that are time-dipendent
TheDateTime_Start_S = datetime(Year, 1, 1, 0)
TheDateTime_Start_F = datetime(Year, 12, 31, 12)
TheDateTime_Start = TheDateTime_Start_S
while TheDateTime_Start <= TheDateTime_Start_F:

      TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)
      TheDateTime_PercSS = TheDateTime_Start - timedelta(days=1) # selecting the soil saturation percentage for 1 day prior the considered accumulation period (to not correlate it with the rainfall)
      print(" - on " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC")

      if TheDateTime_Final >= datetime(2000,1,1,0) and TheDateTime_Final < datetime(2005,1,1,0):
            YearPD = 2000
      elif TheDateTime_Final >= datetime(2005,1,1,0) and TheDateTime_Final < datetime(2010,1,1,0):
            YearPD = 2005
      elif TheDateTime_Final >= datetime(2010,1,1,0) and TheDateTime_Final < datetime(2015,1,1,0):
            YearPD = 2010   
      elif TheDateTime_Final >= datetime(2015,1,1,0) and TheDateTime_Final < datetime(2020,1,1,0):
            YearPD = 2015
      elif TheDateTime_Final >= datetime(2020,1,1,0) and TheDateTime_Final < datetime(2025,1,1,0):
            YearPD = 2020
      else:
            print("ERROR! " + TheDateTime_Final.strftime("%Y-%m-%d") + " is out of the range of valid years (2000 to 2025) for the population density!")
            exit()
      
      # Reading the predictors 
      File_ClassRP = Git_Repo + "/" + DirIN_ClassRP + "/" + TheDateTime_Final.strftime("%Y%m") + "/ClassRP_" + f"{Acc:02}" + "h_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      ClassRP = mv.values(mv.read(File_ClassRP))[mask_index].reshape(-1, 1)
      
      File_RatioEM = Git_Repo + "/" + DirIN_RatioEM + "/" + TheDateTime_Final.strftime("%Y%m") + "/Ratio_" + f"{Acc:02}" + "h_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      RatioEM = mv.values(mv.read(File_RatioEM))[mask_index].reshape(-1, 1)
      
      File_PercSS = Git_Repo + "/" + DirIN_PercSS + "/" + TheDateTime_PercSS.strftime("%Y") + "/" + TheDateTime_PercSS.strftime("%Y%m%d") + "/soil_saturation_perc_" + TheDateTime_PercSS.strftime("%Y%m%d%H") + ".grib"
      PercSS = mv.values(mv.read(File_PercSS))[mask_index].reshape(-1, 1)
      
      File_LAI = Git_Repo + "/" + DirIN_LAI  + "/lai_" + TheDateTime_Final.strftime("%m%d") + ".grib"
      lai = mv.values(mv.read(File_LAI))[mask_index].reshape(-1, 1)

      File_PD = Git_Repo + "/" + DirIN_PD + "/PopDens_" + str(YearPD) + ".grib2"
      pd = mv.values(mv.read(File_PD))[mask_index].reshape(-1, 1)
     
      # Building the predictors' table
      if DirIN_ANN.split("/")[4] == "AllPred":
            predictors = np.concatenate((stdor, ClassRP, RatioEM, PercSS, lai,pd), axis=1)
      else:
            predictors = np.concatenate((stdor, ClassRP, RatioEM, PercSS, lai), axis=1)
      
      # Computing the shap values for each prediction
      shap = explainer(predictors)
      shap_vals = shap.values
      
      # Encoding the shapley values in grib
      shap_vals_grib = None
      for ind in range(shap_vals.shape[1]):
            template = mask_vals * 0
            template[mask_index] = shap_vals[:,ind,0]
            shap_vals_grib = mv.merge(shap_vals_grib, mv.set_values(mask, template))

      # Saving the grib files
      MainDirOUT = Git_Repo + "/" + DirOUT
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      FileOUT_prob = MainDirOUT + "/ShapVal_" +  TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      mv.write(FileOUT_prob, shap_vals_grib)

      TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)