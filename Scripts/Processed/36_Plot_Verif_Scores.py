import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv
import matplotlib.pyplot as plt


##################################################################################################################
# CODE DESCRIPTION
# 36_Plot_Verif_Scores.py computes the contingency tables for specific accumulation periods.  
# Runtime: the script can take up to 10 hours to compute in serial.

# INPUT PARAMETERS DESCRIPTION
# TheDateTime_Start_S (date): start date of the beginning accumulation period to consider.
# TheDateTime_Start_F (date): final date of the beginning accumulation period to consider.
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# Git_Repo (string): repository's local path.
# DirIN_FC (string): relative path of the directory containg the ANN predictions for the probabilities of having a flash flood event in a grid-box.
# DirIN_OBS (string): relative path of the directory containing the gridded accumulated flash flood reports per grid-box. 
# DirOUT (string): relative path of the directory containing the contingency tables. 

# INPUT PARAMETERS
TheDateTime_Start_S = datetime(2021, 1, 1, 0)
TheDateTime_Start_F = datetime(2023, 12, 31, 12)
Acc = 12
Disc_Acc = 12
Thr_list = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,2,3,4,5,6,7,8,9,10]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
DirIN_FC= "Data/Compute/28_Prob_AccRepFF/AllFF_2005_2020/NoPD"
DirIN_OBS = "Data/Compute/19_Grid_AccRepFF"
DirOUT = "Data/Plot/36_Plot_Verif_Scores/AllFF_2005_2020/NoPD"
##################################################################################################################


# Reading domain's mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask_vals = mv.values(mask)
mask_index = np.where(mask_vals == 1)[0]

# Reading the fields with the reported and predicted flash flood events per grid-box
TheDateTime_Start = TheDateTime_Start_S
fc = np.array([])
obs = np.array([])
while TheDateTime_Start <= TheDateTime_Start_F:
      TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)
      print(" - on " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC")
      FileIN_FC = Git_Repo + "/" + DirIN_FC + "/Prob_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      FileIN_OBS = Git_Repo + "/" + DirIN_OBS + "/" + TheDateTime_Final.strftime("%Y") + "/" + TheDateTime_Final.strftime("%Y%m%d") + "/Grid_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d%H") + ".grib"
      fc = np.concatenate((fc, mv.values(mv.read(FileIN_FC))[mask_index]))
      obs = np.concatenate((obs, mv.values(mv.read(FileIN_OBS))[mask_index]))
      TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)
fc[fc == -1] = 0 # set to zero the probabilities of having a flash flood event in those grid-boxes with zero rainfall
ind_no_NaN = np.where(fc >= 0)[0] # remove the NaN
fc = fc[ind_no_NaN]
obs = obs[ind_no_NaN]

# Initializing the variables that will stored the considered scores
hr = []
far = []
bias = []
pss = []
ets = []

# Computing the scores to consider
print()
for Thr in Thr_list:

      # Creating the contingency table
      print("Computing the contingency table for prob >= " + str(Thr))
      h = np.where((obs>0) & (fc>=Thr))[0].shape[0]
      m = np.where((obs>0) & (fc<Thr))[0].shape[0]
      fa = np.where((obs==0) & (fc>=Thr))[0].shape[0]
      cn = np.where((obs==0) & (fc<Thr))[0].shape[0]

      # Computing the scores
      total = h + m + fa + cn
      h_chance = (h + fa) * (h + m) / total
      hr.append( h / (h + m) )
      far.append( fa / (fa + cn) )
      bias.append( (h + fa) / (h + m) )
      pss.append( (h/(h+m)) - (fa/(fa+cn)) )
      ets.append((h - h_chance) / (h + m + fa - h_chance))

# Plotting the considered scores
fig, axs = plt.subplots(2,2, figsize=(14, 10))
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, hspace=0.3, wspace=0.2)

#fig.suptitle("Scores for flash flood predictions exceeding a certain probability threshold (Prob_Thr)")

axs[0,0].plot(Thr_list, bias, "o-", color="#E0115F", linewidth=2, markersize=4) # Bias
axs[0,0]. plot([0,10.1], [1,1], color="#36454F", linewidth=1)
axs[0,0].set_title("Bias")
axs[0,0].set_xlabel("Prob_Thr [%]")
axs[0,0].set_ylabel("Bias [-]")
axs[0,0].set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
axs[0,0].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
axs[0,0].set_xlim([0,10.1])

hr.insert(0, 1) # Roc curve
hr.append(0)
far.insert(0, 1)
far.append(0)
axs[0,1].plot(far, hr, "o-", color="#E0115F", linewidth=2, markersize=4)
axs[0,1].plot([-0.01,1.01], [-0.01,1.01], color="#36454F")
axs[0,1].set_title("ROC curve")
axs[0,1].set_xlabel("False Alarm Rate [-]")
axs[0,1].set_ylabel("Hit Rate [-]")
axs[0,1].set_xlim([-0.01,1.01])
axs[0,1].set_ylim([-0.01,1.01])
axs[0,1].set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
axs[0,1].set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])

axs[1,0].plot(Thr_list, pss, "o-", color="#E0115F", linewidth=2, markersize=4) # Pierce skill score
axs[1,0].set_title("Pierce Skill Score, PSS")
axs[1,0].set_xlabel("Prob_Thr [%]")
axs[1,0].set_ylabel("PSS [-]")
axs[1,0].set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
axs[1,0].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
axs[1,0].set_xlim([0,10.1])

axs[1,1].plot(Thr_list, ets, "o-", color="#E0115F", linewidth=2, markersize=4) # Equitable threat score
axs[1,1].set_title("Equitable threat score, ETS")
axs[1,1].set_xlabel("Prob_Thr [%]")
axs[1,1].set_ylabel("ETS [-]")
axs[1,1].set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
axs[1,1].set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
axs[1,1].set_xlim([0,10.1])

MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
      os.makedirs(MainDirOUT)
FileOUT = MainDirOUT + "/Verif_Scores.jpeg"
plt.savefig(FileOUT, format="jpeg", bbox_inches="tight", dpi=1000)