import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv
import tensorflow as tf

#############################################################################
# CODE DESCRIPTION
# 21_Compute_Predict_RepFF.py predicts the occurrence of flash floods events.
# Runtime: up to 25 minutes when training the model over 20 years of reports.

# INPUT PARAMETERS DESCRIPTION
# DateTime_Start_S (date and time): start date (first three numbers) and time (fourth number) for the analysis period (representing the beginning of the accumulation period).
# DateTime_Start_F (date and time): final date (first three numbers) and time (fourth number) for the analysis period (representing the beginning of the accumulation period).
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
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
# DirIN_PD (string): relative path of the directory containg the population density.
# DirIN_ML (string): relative path of the directory containg the weights for the ML model.
# DirOUT (string): relative path containing the ML predictions.

# INPUT PARAMETERS
Date_S = datetime(2020,4,13)
Date_F = datetime(2020,4,13)
Acc = 12
Disc_Acc = 12
Mask_Domain = [22,-130,52,-60]
Years_Train = "1996_2020"
Specification_PDT = "AllRepFF_NoPopDens"
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
FileIN_slor = "Data/Raw/Analysis/ENS_9km/slor/slor.grib"
FileIN_stdor = "Data/Raw/Analysis/ENS_9km/sdor/sdor.grib"
DirIN_RainThr = "Data/Raw/Analysis/ERA5_ecPoint/tp_climate"
DirIN_Rain = "Data/Raw/Analysis/ERA5_ecPoint/tp"
DirIN_SS = "Data/Compute/07_Percentage_Soil_Saturation"
DirIN_PD = "Data/Compute/10_PopDens_Regrid"
DirIN_ML = "Data/Compute/20_TrainML"
DirOUT = "Data/Compute/21_Predict_RepFF"
#############################################################################

# Import the ML model
model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(3,)),  # Input layer specifying the input shape
    tf.keras.layers.Dense(4, activation=tf.nn.relu),  # Single hidden dense layer with ReLU activation
    tf.keras.layers.Dense(2, activation=tf.nn.softmax)  # Output Dense layer with Softmax activation
    ])

FileIN = Git_Repo + "/" + DirIN_ML + "/" + Specification_PDT + "_" + Years_Train + "/weights"
model.load_weights(FileIN)

model.compile(
    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss = tf.keras.losses.CategoricalCrossentropy(),
    metrics = [tf.keras.metrics.CategoricalAccuracy(name = "accuracy")],
    )

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
                  
            # Reading population density and extracting the nearest values to the mask grid-points 
            if TheDateTime < datetime(2005,1,1,0):
                  YearPD = 2000
            elif TheDateTime >= datetime(2005,1,1,0) and TheDateTime < datetime(2010,1,1,0):
                  YearPD = 2005
            elif TheDateTime >= datetime(2010,1,1,0) and TheDateTime < datetime(2015,1,1,0):
                  YearPD = 2010   
            elif TheDateTime >= datetime(2015,1,1,0) and TheDateTime < datetime(2020,1,1,0):
                  YearPD = 2015
            else:
                  YearPD = 2020
            pd = mv.read(Git_Repo + "/" + DirIN_PD + "/" + str(YearPD) + "/PopDens_N320_" + str(YearPD) + ".grib2")
            pd_mask = mv.nearest_gridpoint(pd, mask_lats, mask_lons).reshape(-1, 1)

            # Building the predictors' table
            predictors = np.concatenate((tp_cat_mask, ss_mask, slor_mask), axis=1)
            
            # Creating the predictions
            ff_pred_array = model.predict(predictors)
            
            # Encoding the predictions in grib
            template = mask_vals * 0
            template[mask_index] = ff_pred_array[:,0]
            ff_pred_grib = mv.set_values(mask, template)

            # Plotting the predictions
            ValidityDateS = TheDateTime - timedelta(hours=Acc)
            DayVS = ValidityDateS.strftime("%d")
            MonthVS = ValidityDateS.strftime("%B")
            YearVS = ValidityDateS.strftime("%Y")
            TimeVS = ValidityDateS.strftime("%H")
            ValidityDateF = TheDateTime
            DayVF = ValidityDateF.strftime("%d")
            MonthVF = ValidityDateF.strftime("%B")
            YearVF = ValidityDateF.strftime("%Y")
            TimeVF = ValidityDateF.strftime("%H")
            title_plot1 = "Probabilities of observing a flash flood event"
            title_plot2 = "VT: " + DayVS + " " + MonthVS + " " + YearVS + " " + TimeVS + " UTC - " + DayVF + " " + MonthVF + " " + YearVF + " " + TimeVF  + " UTC"          

            coastlines = mv.mcoast(
                  map_coastline_colour = "charcoal",
                  map_coastline_thickness = 1,
                  map_coastline_resolution = "high",
                  map_coastline_sea_shade = "on",
                  map_coastline_sea_shade_colour = "RGB(0.7398,0.9465,0.943)",
                  map_boundaries = "on",
                  map_boundaries_colour = "charcoal",
                  map_boundaries_thickness = 1,
                  map_grid_latitude_increment = 5,
                  map_grid_longitude_increment = 10,
                  map_label_right = "off",
                  map_label_top = "off",
                  map_label_colour = "charcoal",
                  map_grid_thickness = 1,
                  map_grid_colour = "charcoal",
                  map_label_height = 0.5
                  )

            geo_view = mv.geoview(
                  map_projection = "epsg:3857",
                  map_area_definition = "corners",
                  area = Mask_Domain,
                  coastlines = coastlines
                  )

            contouring = mv.mcont(
                  legend = "on", 
                  contour = "off",
                  contour_level_selection_type = "level_list",
                  contour_level_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
                  contour_label = "off",
                  contour_shade = "on",
                  contour_shade_technique = "grid_shading",
                  contour_shade_colour_method = "list",
                  contour_shade_colour_list = [
                        "rgb(0.9,0.9,0.9)", 
                        "rgb(0.8,0.8,0.8)",
                        "rgb(0.7,0.7,0.7)",
                        "rgb(0.6,0.6,0.6)",
                        "rgb(0.5,0.5,0.5)",
                        "rgb(0.6,0.6,0.6)",
                        "rgb(0.9622,0.5437,0.5437)",
                        "rgb(0.9837,0.1849,0.1849)",
                        "rgb(0.8398,0.05435,0.05435)",
                        "rgb(0.6734,0.02464,0.02464)",]
                  )

            legend = mv.mlegend(
                  legend_text_colour = "charcoal",
                  legend_text_font_size = 0.5,
                  )

            title = mv.mtext(
                  text_line_count = 3,
                  text_line_1 = title_plot1,
                  text_line_2 = title_plot2,
                  text_line_3 = " ",
                  text_colour = "charcoal",
                  text_font_size = 0.75
                  )

            mv.plot(geo_view, ff_pred_grib, contouring, legend, title)

      TheDate = TheDate + timedelta(days=1)