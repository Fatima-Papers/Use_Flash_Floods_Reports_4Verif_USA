import os
import sys
from datetime import datetime, timedelta
import numpy as np
import metview as mv
import tensorflow as tf

#############################################################################################################
# CODE DESCRIPTION
# 42_Compute_Prob_AccRepFF_Global.py computes the global probabilities of having a flash flood event in a given grid-box using the 
# ANN model.
# Runtime: the script can take up to 2 hours and 30 minutes to compute in serial.

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
Year = int(sys.argv[1])
Acc = 12
Disc_Acc = 12
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
FileIN_StdOrog = "Data/Raw/Analysis/ERA5/sdor/sdor.grib"
DirIN_ClassRP = "Data/Compute/07_ClassRP_AccTP"
DirIN_RatioEM = "Data/Compute/09_Ratio_Extreme_Mean_AccTP"
DirIN_PercSS = "Data/Compute/11_Percentage_Soil_Saturation"
DirIN_LAI = "Data/Raw/Analysis/ERA5/lai"
DirIN_PD = "Data/Compute/14_PopDens_Regrid/N320"
DirIN_ANN = sys.argv[2]
DirOUT = sys.argv[3]
############################################################################################################


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

# Reading domain's mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)

# Reading the stdor values within the considered domain
stdor = mv.values(mv.read(Git_Repo + "/" + FileIN_StdOrog)).reshape(-1, 1)

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
      ClassRP = mv.values(mv.read(File_ClassRP)).reshape(-1, 1)
      
      File_RatioEM = Git_Repo + "/" + DirIN_RatioEM + "/" + TheDateTime_Final.strftime("%Y%m") + "/Ratio_" + f"{Acc:02}" + "h_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      RatioEM = mv.values(mv.read(File_RatioEM)).reshape(-1, 1)
      
      File_PercSS = Git_Repo + "/" + DirIN_PercSS + "/" + TheDateTime_PercSS.strftime("%Y") + "/" + TheDateTime_PercSS.strftime("%Y%m%d") + "/soil_saturation_perc_" + TheDateTime_PercSS.strftime("%Y%m%d%H") + ".grib"
      PercSS = mv.values(mv.read(File_PercSS)).reshape(-1, 1)
      
      File_LAI = Git_Repo + "/" + DirIN_LAI  + "/lai_" + TheDateTime_Final.strftime("%m%d") + ".grib"
      lai = mv.values(mv.read(File_LAI)).reshape(-1, 1)

      File_PD = Git_Repo + "/" + DirIN_PD + "/PopDens_" + str(YearPD) + ".grib2"
      pd = mv.values(mv.read(File_PD)).reshape(-1, 1)
     
      # Building the predictors' table
      if DirIN_ANN.split("/")[4] == "AllPred":
            predictors = np.concatenate((stdor, ClassRP, RatioEM, PercSS, lai,pd), axis=1)
      else:
            predictors = np.concatenate((stdor, ClassRP, RatioEM, PercSS, lai), axis=1)
      
      # Create the predictions
      ff_pred_array = model.predict(predictors) * 100

      # Set to zero the probabilities of having a flash flood report where there is no rainfall
      ind_tp0 = np.where(ClassRP == 0)[0] 
      ff_pred_array[ind_tp0] = -1
      
      # Encoding the predictions in grib
      ff_pred_grib = mv.set_values(mask, ff_pred_array[:,0])

      # Saving the grib files
      MainDirOUT = Git_Repo + "/" + DirOUT
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      FileOUT_prob = MainDirOUT + "/Prob_AccRepFF_" +  TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      mv.write(FileOUT_prob, ff_pred_grib)

      TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)