import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv
import matplotlib.pyplot as plt


#########################################################################################
# CODE DESCRIPTION
# 31_Plot_Distribution_Prob_AccRepFF plots the distribution of probabilities of having a flash flood event in 
# each grid-box from different training datasets.
# Runtime: the script can take up to 1 hour to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year (integer, in YYYY format): year to consider.
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Train_Period (string): name of the train period to consider. 
# Predictors (string): name of the set of predictors to consider.
# TrainPDT_List (list of strings): list of the names of training datasets (PDTs) to consider.
# PercRed_list (list of integers): percentages of flash flood reductions to consider when TrainPDT="RedRndFF".
# Colours_List (list of strings): list of colour names to assign to each single violin plots.
# Git_Repo (string): repository's local path.
# FileIN_Mask (string): relative path of the file containing the domain's mask.
# DirIN (string): relative path of the directory containg the probabilities.
# DirOUT (string): relative path of the directory containg the distribution plots.

# INPUT PARAMETERS
Year = 2021
Acc = 12
Disc_Acc = 12
Train_Period = "2005_2020" 
Predictors = "AllPred"
TrainPDT_List = ["NoNorthFF", "NoSouthFF", "NoWestFF", "NoEastFF", "NoNorthGP", "NoSouthGP", "NoWestGP", "NoEastGP", "RedRndFF", "AllFF"] 
PercRed_list = [90,50,10]
Colours_List = ["saddlebrown", "saddlebrown", "saddlebrown", "saddlebrown", "teal", "teal", "teal", "teal", "darkmagenta", "darkmagenta", "darkmagenta", "darkgrey"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
DirIN = "Data/Compute"
DirOUT = "Data/Plot/31_Distribution_Prob_AccRepFF"
#########################################################################################


# Defining the analysis period to consider
TheDateTime_Start_S = datetime(Year, 1, 1, 0)
TheDateTime_Start_F = datetime(Year, 12, 31, 12)

# Reading the domain's mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask_vals = mv.values(mask)
ind_mask = np.where(mask_vals>0)[0]

# Reading the probabilities for each day in the analysis period, for all the considered training datasets
Prob_AccRepFF = []
Name_PDT = []
for TrainPDT in TrainPDT_List:

      if TrainPDT == "RedRndFF":

            DirIN_temp1 = DirIN + "/29_Prob_AccRepFF_Mean_RedRndFF/" + TrainPDT + "_" + Train_Period + "/" + Predictors
            
            for PercRed in PercRed_list:

                  print("Considering the following training dataset: " + TrainPDT + "_" + str(PercRed) + "_" + Train_Period + "/" + Predictors)
                  DirIN_temp = DirIN_temp1 + "/" + str(PercRed) + "/Mean/"
                  Name_PDT.append(TrainPDT + "_" + str(PercRed) + "_" + Predictors)
                  
                  Prob_AccRepFF_SinglePDT = np.array([])
                  
                  TheDateTime_Start = TheDateTime_Start_S
                  while TheDateTime_Start <= TheDateTime_Start_F:

                        TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)
                        print(" - on " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC")
                  
                        FileIN = Git_Repo + "/" + DirIN_temp + "/Prob_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
                        Prob_AccRepFF_SinglePer = mv.values(mv.read(FileIN))[ind_mask]
                        ind_FF = np.where(Prob_AccRepFF_SinglePer>0)[0]
                        Prob_AccRepFF_SinglePDT = np.concatenate((Prob_AccRepFF_SinglePDT, Prob_AccRepFF_SinglePer[ind_FF]))

                        TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)
                  
                  Prob_AccRepFF.append(Prob_AccRepFF_SinglePDT)

      else:
            
            print("Considering the following training dataset: " + TrainPDT + "_" + Train_Period + "/" + Predictors)
            DirIN_temp = DirIN + "/28_Prob_AccRepFF/" + TrainPDT + "_" + Train_Period + "/" + Predictors
            Name_PDT.append(TrainPDT + "_" + Predictors)

            Prob_AccRepFF_SinglePDT = np.array([])
            
            TheDateTime_Start = TheDateTime_Start_S
            while TheDateTime_Start <= TheDateTime_Start_F:

                  TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)
                  print(" - on " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC")
            
                  FileIN = Git_Repo + "/" + DirIN_temp + "/Prob_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
                  Prob_AccRepFF_SinglePer = mv.values(mv.read(FileIN))[ind_mask]
                  ind_FF = np.where(Prob_AccRepFF_SinglePer>0)[0]
                  Prob_AccRepFF_SinglePDT = np.concatenate((Prob_AccRepFF_SinglePDT, Prob_AccRepFF_SinglePer[ind_FF]))
                  
                  TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)

            Prob_AccRepFF.append(Prob_AccRepFF_SinglePDT)

# Plotting the distribution of probabilities for each training dataset
fig, ax = plt.subplots(figsize = (8,10))

violin_parts = ax.violinplot(Prob_AccRepFF, showmedians=True, showextrema=True, vert=False)
ax.set_xlabel("Probability [%]")
ax.set_ylabel("Training datasets")
ax.set_title("Distribution of the probabilities of having a flash flood event at a grid-box")
ax.set_yticks(np.arange(1, len(Name_PDT)+1))
ax.set_yticklabels(Name_PDT)

for partname in ('cbars','cmins','cmaxes', 'cmedians'):
    vp = violin_parts[partname]
    vp.set_edgecolor("dimgrey")
    vp.set_linewidth(1)

for vp, colour in zip(violin_parts['bodies'], Colours_List):
    vp.set_facecolor(colour)
    vp.set_edgecolor("white")
    vp.set_linewidth(1)
    vp.set_alpha(0.5)

# Saving the plot
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
      os.makedirs(MainDirOUT)
FileOUT = MainDirOUT + "/Distribution_Prob_AccRepFF" + str(Year) + ".png"
plt.savefig(FileOUT, format="jpeg", bbox_inches="tight", dpi=1000)