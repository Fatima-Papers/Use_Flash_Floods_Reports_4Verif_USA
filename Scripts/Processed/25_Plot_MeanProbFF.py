import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv
import matplotlib.pyplot as plt

###########################################################################
# CODE DESCRIPTION
# 25_Plot_MeanProbFF.py create a bar plot of the mean probabilities of having a flash flood 
# event using different training datasets.
# Runtime: the script can take up to 10 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# DateTime_Final_S (date and time): start date (first three numbers) and time (fourth number) for the analysis period (representing the end of the accumulation period).
# DateTime_Final_F (date and time): final date (first three numbers) and time (fourth number) for the analysis period (representing the end of the accumulation period).
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Years_Train (string): years covered in the training dataset.
# Specification_PDT (string): specification of the dataset (PDT) used  for training.
# xTick_Label_list (string): name to use int he plot for the considered PDTs.
# Git_Repo (string): repository's local path.
# FileIN_Mask (string): relative path where the USA's mask is stored.
# DirIN_ML (string): relative path of the directory containg the probabilities predictions.
# DirOUT (string): relative path containing the bar plots.

# INPUT PARAMETERS
DateTime_Final_S = datetime(2021,1,1,12)
DateTime_Final_F = datetime(2022,1,1,0)
Disc_Acc = 12
Years_Train = "2005_2020"
Type_Predictors = "NoPopDens"
Specification_PDT_list = ["AllRepFF", "NoEastFF", "NoEastGP", "NoWestFF", "NoWestGP"]
xTick_Label_list = ["All RepFF\nFull Domain", "Full Domain\nOnly West RepFF", "Only West Domain", "Full domain\nOnly East RepFF", "Only East Domain"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
DirIN = "Data/Compute/21_Predict_RepFF"
DirOUT = "Data/Plot/25_MeanProbFF"
#############################################################################


# Reading domain's mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask_lats = mv.latitudes(mask)
mask_lons = mv.longitudes(mask)
mask_vals = mv.values(mask)
mask_index = np.where(mask_vals == 1)[0]
mask_lats = mask_lats[mask_index]
mask_lons = mask_lons[mask_index] - 360
ind_lons_west = np.where(mask_lons < -100)[0]
ind_lons_east = np.where(mask_lons >= -100)[0]

#Initializing the variables that will contain the means
Num_Periods = ((DateTime_Final_F - DateTime_Final_S).days + 1 ) * (24/Disc_Acc)
Num_PDT = len(Specification_PDT_list)
MeanProbFF_east = np.zeros((int(Num_Periods), int(Num_PDT)))
MeanProbFF_west = np.zeros((int(Num_Periods), int(Num_PDT)))

# Reading the predictions of flash flood events
for ind_PDT in range(Num_PDT):

      Specification_PDT = Specification_PDT_list[ind_PDT]
      print("Considering the PDT '" + Specification_PDT + "_" + Type_Predictors + "' and reading predictions for:")
      
      ind_day = 0
      TheDateTime_Final = DateTime_Final_S
      while TheDateTime_Final <= DateTime_Final_F:
            
            print(" - " + TheDateTime_Final.strftime("%Y%m%d%H"))

            FileIN = Git_Repo + "/" + DirIN + "/" + Specification_PDT + "_" + Type_Predictors + "_" + Years_Train + "/Prob_RepFF_" +  TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
            prob_repFF = mv.read(FileIN)
            prob_repFF = (prob_repFF == -1) * 0 + (prob_repFF != -1) * prob_repFF
            prob_repFF_mask = mv.nearest_gridpoint(prob_repFF, mask_lats, mask_lons)
            prob_repFF_east = prob_repFF_mask[ind_lons_east]
            prob_repFF_west = prob_repFF_mask[ind_lons_west]
            MeanProbFF_east[ind_day, ind_PDT] = np.nanmean(prob_repFF_east)
            MeanProbFF_west[ind_day, ind_PDT] = np.nanmean(prob_repFF_west)

            ind_day = ind_day + 1
            TheDateTime_Final = TheDateTime_Final + timedelta(hours=Disc_Acc)

# Computing the mean probabilities over all days in the verification period
MeanProbFF_east = np.nanmean(MeanProbFF_east, axis=0)
MeanProbFF_west = np.nanmean(MeanProbFF_west, axis=0)

# Creating andf saving the bar plots of the mean probabilities
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
      os.makedirs(MainDirOUT)

fig, ax = plt.subplots(figsize=(8, 10))
plt.bar(xTick_Label_list, MeanProbFF_east, color="red")
plt.title("Probability of having flash flood events\n in Eastern USA considering different training datasets", weight="bold", pad=5)
plt.xlabel("Training datasets")
plt.ylabel("Probability [%]")
plt.xticks(rotation=30)
plt.ylim((0, 0.07))
FileOUT = MainDirOUT + "/MeanProbFF_East_" +  Type_Predictors + ".png"
plt.savefig(FileOUT, dpi=1000)
plt.close()

fig, ax = plt.subplots(figsize=(8, 10))
plt.bar(xTick_Label_list, MeanProbFF_west, color="red")
plt.title("Probability of having flash flood events\n in Western USA considering different training datasets", weight="bold", pad=5)
plt.xlabel("Training datasets")
plt.ylabel("Probability [%]")
plt.xticks(rotation=30)
plt.ylim((0, 0.07))
FileOUT = MainDirOUT + "/MeanProbFF_West_" +  Type_Predictors + ".png"
plt.savefig(FileOUT, dpi=1000)
plt.close()