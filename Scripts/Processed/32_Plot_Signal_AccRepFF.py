import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv
import matplotlib.pyplot as plt


#########################################################################################
# CODE DESCRIPTION
# 31_Plot_Distribution_Prob_AccRepFF creates a dumbell plot with the number of grid-boxes exceeding the 
# climatological average probability of having a flash flood event in a grid-box in different training datasets 
# compared to the full training dataset.
# Runtime: the script can take up to 5 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year (integer, in YYYY format): year to consider.
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Git_Repo (string): repository's local path.
# FileIN_Mask (string): relative path of the file containing the domain's mask.
# DirIN (string): relative path of the directory containg the probabilities.
# DirOUT (string): relative path of the directory containg the distribution plots.

# INPUT PARAMETERS
Year = 2021
Acc = 12
Disc_Acc = 12
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
DirIN = "Data/Compute"
DirOUT = "Data/Plot/32_Signal_AccRepFF"
################################################################


# Defining MainDirIN and MainDirOUT
MainDirIN = Git_Repo + "/" + DirIN
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
      os.makedirs(MainDirOUT)

# Defining the analysis period to consider
TheDateTime_Start_S = datetime(Year, 1, 1, 0)
TheDateTime_Start_F = datetime(Year, 12, 31, 12)

# Reading the number of grid-boxes in the domain
mask = mv.values(mv.read(Git_Repo + "/" + FileIN_Mask))
NumGP_mask = np.where(mask == 1)[0].shape[0]

# Computing the climatological average probabilities of having a flash flood event in a grid-box
print("Computing the climatological average probabilities of having a flash flood event in a grid-box")
NumGP_Tot = 0
NumDays = 0
TheDateTime_Start = TheDateTime_Start_S
while TheDateTime_Start <= TheDateTime_Start_F:
      TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)
      print(" - on " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC")
      FileIN = MainDirIN + "/19_Grid_AccRepFF/" + TheDateTime_Final.strftime("%Y") + "/" + TheDateTime_Final.strftime("%Y%m%d") + "/Grid_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d%H") + ".grib"
      Grid_AccRepFF = mv.values(mv.read(FileIN))
      NumGP_Tot = NumGP_Tot  + np.where(Grid_AccRepFF > 0)[0].shape[0]
      NumDays = NumDays + 1
      TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)
ClimAv_Grid_AccRepFF = NumGP_Tot / NumGP_mask / NumDays * 100

# Initializing the variable that will store the number of grid-boxes exceeding the climatological average probability of having a flash flood event in a grid-box
NumGP_AllFF = []
NumGP_RedRnd_10 = []
NumGP_RedRnd_50 = []
NumGP_RedRnd_90 = []
NumGP_NoEastGP = []
NumGP_NoWestGP = []
NumGP_NoSouthGP = []
NumGP_NoNorthGP = []
NumGP_NoEastFF = []
NumGP_NoWestFF = []
NumGP_NoSouthFF = []
NumGP_NoNorthFF = []

# Computing the number of grid-boxes with probabilities greater than the climatological average probability of having a flash flood event in a grid-box
TheDateTime_Start = TheDateTime_Start_S
while TheDateTime_Start <= TheDateTime_Start_F:

      TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)
      print(" - on " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC")

      # Reading the probabilities
      FileIN_AllFF = MainDirIN + "/28_Prob_AccRepFF/AllFF_2005_2020/AllPred/Prob_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      FileIN_RedRdnFF_90 = MainDirIN + "/29_Prob_AccRepFF_Mean_RedRndFF/RedRndFF_2005_2020/AllPred/90/Mean/Prob_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      FileIN_RedRdnFF_50 = MainDirIN + "/29_Prob_AccRepFF_Mean_RedRndFF/RedRndFF_2005_2020/AllPred/50/Mean/Prob_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      FileIN_RedRdnFF_10 = MainDirIN + "/29_Prob_AccRepFF_Mean_RedRndFF/RedRndFF_2005_2020/AllPred/10/Mean/Prob_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      FileIN_NoEastGP = MainDirIN + "/28_Prob_AccRepFF/NoEastGP_2005_2020/AllPred/Prob_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      FileIN_NoWestGP = MainDirIN + "/28_Prob_AccRepFF/NoWestGP_2005_2020/AllPred/Prob_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      FileIN_NoSouthGP = MainDirIN + "/28_Prob_AccRepFF/NoSouthGP_2005_2020/AllPred/Prob_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      FileIN_NoNorthGP = MainDirIN + "/28_Prob_AccRepFF/NoNorthGP_2005_2020/AllPred/Prob_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      FileIN_NoEastFF = MainDirIN + "/28_Prob_AccRepFF/NoEastFF_2005_2020/AllPred/Prob_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      FileIN_NoWestFF = MainDirIN + "/28_Prob_AccRepFF/NoWestFF_2005_2020/AllPred/Prob_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      FileIN_NoSouthFF = MainDirIN + "/28_Prob_AccRepFF/NoSouthFF_2005_2020/AllPred/Prob_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      FileIN_NoNorthFF = MainDirIN + "/28_Prob_AccRepFF/NoNorthFF_2005_2020/AllPred/Prob_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      
      AllFF = mv.bitmap(mv.read(FileIN_AllFF), -1)
      RedRnd_90 = mv.bitmap(mv.read(FileIN_RedRdnFF_90), -1)
      RedRnd_50 = mv.bitmap(mv.read(FileIN_RedRdnFF_50), -1)
      RedRnd_10 = mv.bitmap(mv.read(FileIN_RedRdnFF_10), -1)
      NoEastGP = mv.bitmap(mv.read(FileIN_NoEastGP), -1)
      NoWestGP = mv.bitmap(mv.read(FileIN_NoWestGP), -1)
      NoSouthGP = mv.bitmap(mv.read(FileIN_NoSouthGP), -1)
      NoNorthGP = mv.bitmap(mv.read(FileIN_NoNorthGP), -1)
      NoEastFF = mv.bitmap(mv.read(FileIN_NoEastFF), -1)
      NoWestFF = mv.bitmap(mv.read(FileIN_NoWestFF), -1)
      NoSouthFF = mv.bitmap(mv.read(FileIN_NoSouthFF), -1)
      NoNorthFF = mv.bitmap(mv.read(FileIN_NoNorthFF), -1)
      
      # Computing how many grid-boxes have probabilities greater than the climatological average probability of having a flash flood event in a grid-box
      temp = (AllFF >= ClimAv_Grid_AccRepFF)
      NumGP_AllFF.append(np.nansum(mv.values(temp)))
      
      temp = (RedRnd_90 >= ClimAv_Grid_AccRepFF)
      NumGP_RedRnd_90.append(np.nansum(mv.values(temp)))

      temp = (RedRnd_50 >= ClimAv_Grid_AccRepFF)
      NumGP_RedRnd_50.append(np.nansum(mv.values(temp)))
      
      temp = (RedRnd_10 >= ClimAv_Grid_AccRepFF)
      NumGP_RedRnd_10.append(np.nansum(mv.values(temp)))
      
      temp = (NoEastGP > ClimAv_Grid_AccRepFF)
      NumGP_NoEastGP.append(np.nansum(mv.values(temp)))

      temp = (NoWestGP >= ClimAv_Grid_AccRepFF)
      NumGP_NoWestGP.append(np.nansum(mv.values(temp)))
      
      temp = (NoSouthGP >= ClimAv_Grid_AccRepFF)
      NumGP_NoSouthGP.append(np.nansum(mv.values(temp)))

      temp = (NoNorthGP >= ClimAv_Grid_AccRepFF)
      NumGP_NoNorthGP.append(np.nansum(mv.values(temp)))

      temp = (NoEastFF >= ClimAv_Grid_AccRepFF)
      NumGP_NoEastFF.append(np.nansum(mv.values(temp)))

      temp = (NoWestFF >= ClimAv_Grid_AccRepFF)
      NumGP_NoWestFF.append(np.nansum(mv.values(temp)))
      
      temp = (NoSouthFF >= ClimAv_Grid_AccRepFF)
      NumGP_NoSouthFF.append(np.nansum(mv.values(temp)))

      temp = (NoNorthFF >= ClimAv_Grid_AccRepFF)
      NumGP_NoNorthFF.append(np.nansum(mv.values(temp)))

      TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)

# Creating the arrays to create the dumbell plot
NumGP = np.array([np.sum(NumGP_NoNorthFF),
      np.sum(NumGP_NoSouthFF), 
      np.sum(NumGP_NoWestFF), 
      np.sum(NumGP_NoEastFF), 
      np.sum(NumGP_NoNorthGP),
      np.sum(NumGP_NoSouthGP), 
      np.sum(NumGP_NoWestGP), 
      np.sum(NumGP_NoEastGP), 
      np.sum(NumGP_RedRnd_90), 
      np.sum(NumGP_RedRnd_50),
      np.sum(NumGP_RedRnd_10)])

NumGP_comp = np.ones(len(NumGP)) * np.sum(NumGP_AllFF)

Colours_List = ["saddlebrown", "saddlebrown", "saddlebrown", "saddlebrown", "teal", "teal", "teal", "teal", "darkmagenta", "darkmagenta", "darkmagenta"]

TrainPDT_List = [
      "NoNorthFF",
      "NoSouthFF", 
      "NoWestFF", 
      "NoEastFF", 
      "NoNorthGP",
      "NoSouthGP", 
      "NoWestGP", 
      "NoEastGP",
      "RedRndFF_90",
      "RedRndFF_50",
      "RedRndFF_10"] 

Perc_NumGP = NumGP / np.sum(NumGP_AllFF) * 100
print(Perc_NumGP)

# Creating the dumbel plot
fig, ax = plt.subplots(figsize=(10,6), facecolor = "white")
ax.grid(which="major", axis='both', color='#758D99', alpha=0.6, zorder=1)
ax.spines[['top','right','bottom']].set_visible(False)

ax.hlines(y=np.arange(len(NumGP)), xmin=NumGP, xmax=NumGP_comp, color='#758D99', zorder=2, linewidth=2, label='_nolegend_', alpha=.8)
ax.scatter(NumGP, TrainPDT_List, label="Different Training Datasets", s=60, color=Colours_List, zorder=3)
ax.scatter(NumGP_comp, TrainPDT_List, label="AllFF", s=60, color="darkgrey", zorder=3)

plt.title("N. of grid-boxes exceeding the climatological average probability (=" + str(np.round(ClimAv_Grid_AccRepFF,decimals=2)) + "%) of having a flash flood event in a grid-box")
plt.xlabel("N. of grid-boxes")

# Save the dumbell plot
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
      os.makedirs(MainDirOUT)
FileOUT = MainDirOUT + "/Signal_AccRepFF" + str(Year) + ".png"
plt.savefig(FileOUT, format="jpeg", bbox_inches="tight", dpi=1000)