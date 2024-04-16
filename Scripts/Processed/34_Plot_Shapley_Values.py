import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

#############################################################################################################
# CODE DESCRIPTION
# 34_Plot_Shapley_Values.py plots the distribution of shapley values according to the correspondent predictors.
# Runtime: the script can take up to 15 minutes to compute in serial.

# INPUT PARAMETERS DESCRIPTION
# Year (integer, in YYYY format): year to consider.
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Git_Repo (string): repository's local path.
# FileIN_Mask (string): relative path of the file containing the domain's mask.
# FileIN_StdOrog (string): relative path of the file containing the standard deviation of the sub-grid orography.
# DirIN_ClassRP (string): relative path of the directory containing the return period class for the extreme ERA5-ecPoint rainfall analysis.
# DirIN_RatioEM (string): relative path of the directory containing the ratio between extreme and mean ERA5-ecPoint rainfall analysis.
# DirIN_PercSS (string): relative path of the directory containing the percentage of soil saturation.
# DirIN_LAI (string): relative path of the directory containing the leaf area index.
# DirIN_PD (string): relative path of the directory containing the regridded population density.
# DirIN (string): relative path of the directory containg the ANN's flash flood predictions.
# DirOUT (string): relative path of the directory containing the probabilities of having a flash flood event in a given grid-box.

# INPUT PARAMETERS
Year = 2021
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
DirIN = "Data/Compute/33_Compute_Shapley_Values/AllFF_2005_2020/AllPred"
DirOUT = "Data/Plot/34_Shapley_Values/AllFF_2005_2020/AllPred"
#############################################################################################################


# Reading domain's mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask_vals = mv.values(mask)
mask_index = np.where(mask_vals == 1)[0]

# Reading the shapley and predictors values
TheDateTime_Start_S = datetime(Year, 1, 1, 0)
TheDateTime_Start_F = datetime(Year, 12, 31, 0)
TheDateTime_Start = TheDateTime_Start_S
while TheDateTime_Start <= TheDateTime_Start_F:

      TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)
      print(" - on " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC")

      FileIN = Git_Repo + "/" + DirIN + "/ShapVal_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      shap_temp = mv.values(mv.read(FileIN))[:,mask_index]

      FileIN_StdOrog_1 = Git_Repo + "/" + FileIN_StdOrog
      stdorog_temp = mv.values(mv.read(FileIN_StdOrog_1))[mask_index]

      FileIN_CalssRP = Git_Repo + "/" + DirIN_ClassRP + "/" + TheDateTime_Final.strftime("%Y%m") + "/ClassRP_12h_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      classRP_temp = mv.values(mv.read(FileIN_CalssRP))[mask_index]

      FileIN_RatioEM = Git_Repo + "/" + DirIN_RatioEM + "/" + TheDateTime_Final.strftime("%Y%m") + "/Ratio_12h_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      ratioEM_temp = mv.values(mv.read(FileIN_RatioEM))[mask_index]

      FileIN_PercSS = Git_Repo + "/" + DirIN_PercSS + "/" + TheDateTime_Final.strftime("%Y") + "/" + TheDateTime_Final.strftime("%Y%m%d")  + "/soil_saturation_perc_" + TheDateTime_Final.strftime("%Y%m%d%H") + ".grib"
      percSS_temp = mv.values(mv.read(FileIN_PercSS))[mask_index]

      FileIN_LAI = Git_Repo + "/" + DirIN_LAI + "/lai_" + TheDateTime_Final.strftime("%m%d") + ".grib"
      lai_temp = mv.values(mv.read(FileIN_LAI))[mask_index]

      FileIN_PD = Git_Repo + "/" + DirIN_PD + "/PopDens_2020.grib2"
      pd_temp = mv.values(mv.read(FileIN_PD))[mask_index]

      if TheDateTime_Start == TheDateTime_Start_S:
            shap = shap_temp
            stdorog = stdorog_temp
            classRP = classRP_temp
            ratioEM = ratioEM_temp
            percSS = percSS_temp
            lai = lai_temp
            pd = pd_temp
      else:
            shap = np.concatenate((shap, shap_temp), axis=1)
            stdorog = np.concatenate((stdorog, stdorog_temp))
            classRP = np.concatenate((classRP, classRP_temp))
            ratioEM = np.concatenate((ratioEM, ratioEM_temp))
            percSS = np.concatenate((percSS, percSS_temp))
            lai = np.concatenate((lai, lai_temp))
            pd = np.concatenate((pd, pd_temp))
      
      TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)

ind_no_NaN = ~np.isnan(shap[0])
shap = shap[:, ind_no_NaN]
stdorog = stdorog[ind_no_NaN]
classRP = classRP[ind_no_NaN]
ratioEM = ratioEM[ind_no_NaN]
percSS = percSS[ind_no_NaN]
lai = lai[ind_no_NaN]
pd = pd[ind_no_NaN]

# Creating and saving the shapley values plots
indices = np.arange(len(shap[1]))
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
      os.makedirs(MainDirOUT)

boundaries = [0, 50, 100, 200, 500, 1000]
norm = mcolors.BoundaryNorm(boundaries, ncolors=plt.cm.plasma.N, clip=True)
plt.scatter(shap[0]*100, indices, s=0.1, c=stdorog, cmap="plasma", norm=norm)
plt.title("Standard Deviation of Orography")
plt.xlabel("Probability [%]")
plt.yticks([])
sm = plt.cm.ScalarMappable(cmap="plasma", norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ticks=boundaries)
cbar.set_label("StdOrog")
FileOUT = MainDirOUT + "/StdOrog.png"
plt.savefig(FileOUT, format="jpeg", bbox_inches="tight", dpi=1000)
plt.close()

boundaries = [0, 1, 2, 5, 10, 20, 100]
norm = mcolors.BoundaryNorm(boundaries, ncolors=plt.cm.plasma.N, clip=True)
plt.scatter(shap[1]*100, indices, s=0.1, c=classRP, cmap="plasma", norm=norm)
plt.title("Return Period of Extreme Rainfall")
plt.xlabel("Probability [%]")
plt.yticks([])
sm = plt.cm.ScalarMappable(cmap="plasma", norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ticks=boundaries)
cbar.set_label("ClassRP")
FileOUT = MainDirOUT + "/ClassRP.png"
plt.savefig(FileOUT, format="jpeg", bbox_inches="tight", dpi=1000)
plt.close()

boundaries = [0, 1, 2, 5, 10, 20, 100, 1000]
norm = mcolors.BoundaryNorm(boundaries, ncolors=plt.cm.plasma.N, clip=True)
plt.scatter(shap[2]*100, indices, s=0.1, c=ratioEM, cmap="plasma", norm=norm)
plt.title("Ratio Extreme-Mean Rainfall")
plt.xlabel("Probability [%]")
plt.yticks([])
sm = plt.cm.ScalarMappable(cmap="plasma", norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ticks=boundaries)
cbar.set_label("RatioEM")
FileOUT = MainDirOUT + "/RatioEM.png"
plt.savefig(FileOUT, format="jpeg", bbox_inches="tight", dpi=1000)
plt.close()

boundaries = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
norm = mcolors.BoundaryNorm(boundaries, ncolors=plt.cm.plasma.N, clip=True)
plt.scatter(shap[3]*100, indices, s=0.1, c=percSS, cmap="plasma", norm=norm)
plt.title("Soil Saturation Percentage")
plt.xlabel("Probability [%]")
plt.yticks([])
sm = plt.cm.ScalarMappable(cmap="plasma", norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ticks=boundaries)
cbar.set_label("PercSS")
FileOUT = MainDirOUT + "/PercSS.png"
plt.savefig(FileOUT, format="jpeg", bbox_inches="tight", dpi=1000)
plt.close()

boundaries = [0, 1, 2, 3, 4, 5, 6, 7]
norm = mcolors.BoundaryNorm(boundaries, ncolors=plt.cm.plasma.N, clip=True)
plt.scatter(shap[4]*100, indices, s=0.1, c=lai, cmap="plasma", norm=norm)
plt.title("Leaf Area Index")
plt.xlabel("Probability [%]")
plt.yticks([])
sm = plt.cm.ScalarMappable(cmap="plasma", norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ticks=boundaries)
cbar.set_label("LAI")
FileOUT = MainDirOUT + "/LAI.png"
plt.savefig(FileOUT, format="jpeg", bbox_inches="tight", dpi=1000)
plt.close()

boundaries = [0, 100, 500, 1000, 2000, 5000, 10000, 100000]
norm = mcolors.BoundaryNorm(boundaries, ncolors=plt.cm.plasma.N, clip=True)
plt.scatter(shap[5]*100, indices, s=0.1, c=pd, cmap="plasma", norm=norm)
plt.title("Population Density")
plt.xlabel("Probability [%]")
plt.yticks([])
sm = plt.cm.ScalarMappable(cmap="plasma", norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ticks=boundaries)
cbar.set_label("PD")
FileOUT = MainDirOUT + "/PD.png"
plt.savefig(FileOUT, format="jpeg", bbox_inches="tight", dpi=1000)
plt.close()