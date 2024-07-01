import os
from datetime import datetime, timedelta
import numpy as np
import random
import metview as mv
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch


##################################################################################################################
# CODE DESCRIPTION
# 36_Plot_Verif_Scores.py computes the contingency tables for specific accumulation periods.  
# Runtime: the script can take up to 10 hours to compute in serial.

# INPUT PARAMETERS DESCRIPTION
# TheDateTime_Start_S (date): start date of the beginning accumulation period to consider.
# TheDateTime_Start_F (date): final date of the beginning accumulation period to consider.
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Num_BS (integer): number of bootstrapping repetitions.
# CL (integer, from 0 to 100, in %): confidence level for the error bars.
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
Num_BS = 1000
CL = 99
Thr_list = [0.1, 0.3, 0.5, 0.7, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
DirIN_FC= "Data/Compute/28_Prob_AccRepFF/AllFF_2005_2020/NoPD"
DirIN_OBS = "Data/Compute/19_Grid_AccRepFF"
DirOUT = "Data/Plot/36_Plot_Verif_Scores/AllFF_2005_2020/NoPD"
##################################################################################################################


# CUSTOM FUNCTIONS

# Generating the list of original dates within the verification period
def generate_date_list_with_hours(start, end, list_start_accper):
      delta = end - start
      date_list = []
      for i in range(delta.days + 1):
            day = start + timedelta(days=i)
            for start_accper in list_start_accper:
                  date_list.append(day.replace(hour=start_accper))
      return date_list

def random_dates_list(start, end, list_start_accper):
      num_days = (end - start).days
      random_dates = []
      for _ in range(num_days):
            random_days = random.randint(0, num_days)
            random_hour = random.choice(list_start_accper)
            random_date = start + timedelta(days=random_days, hours=random_hour)
            random_dates.append(random_date)
      return random_dates
###################################################################


# Setting the main output directory
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
      os.makedirs(MainDirOUT)

# Initializing the variables that will stored the bootsrapped contingency tables
h_bs = np.zeros((len(Thr_list), (Num_BS+1)))
m_bs = np.zeros((len(Thr_list), (Num_BS+1)))
fa_bs = np.zeros((len(Thr_list), (Num_BS+1))) 
cn_bs = np.zeros((len(Thr_list), (Num_BS+1)))

# Assessing how many accumulation periods are considered per day
List_Start_AccPer = integer_list = list(range(0, 24, Disc_Acc))
Num_Days = (TheDateTime_Start_F - TheDateTime_Start_S).days + 1

# Reading domain's mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask_vals = mv.values(mask)
mask_index = np.where(mask_vals == 1)[0]
Num_GP = mask_index.shape[0]

# Computing the bootstrapped verification scores for the considered verification period
print("Computing the bootstrapped verification scores for the verification period between " + TheDateTime_Start_S.strftime("%Y-%m-%d %H UTC") + " and " + TheDateTime_Start_F.strftime("%Y-%m-%d %H UTC"))
for ind_BS in range(Num_BS+1):

      print(" - Bootstrap n. " + str(ind_BS) + "/" + str(Num_BS))

      if ind_BS == 0: # original dates
            TheDateTime_Start_list = generate_date_list_with_hours(TheDateTime_Start_S, TheDateTime_Start_F, List_Start_AccPer)
      else: # bootstrapped dates
            TheDateTime_Start_list = random_dates_list(TheDateTime_Start_S, TheDateTime_Start_F, List_Start_AccPer)

      # Reading the fields with the reported and predicted flash flood events per grid-box
      fc = np.array([])
      obs = np.array([])
      for TheDateTime_Start in TheDateTime_Start_list:
            TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)
            FileIN_FC = Git_Repo + "/" + DirIN_FC + "/Prob_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
            FileIN_OBS = Git_Repo + "/" + DirIN_OBS + "/" + TheDateTime_Final.strftime("%Y") + "/" + TheDateTime_Final.strftime("%Y%m%d") + "/Grid_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d%H") + ".grib"
            fc = np.concatenate((fc, mv.values(mv.read(FileIN_FC))[mask_index]))
            obs = np.concatenate((obs, mv.values(mv.read(FileIN_OBS))[mask_index]))
            TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)
      fc[fc == -1] = 0 # set to zero the probabilities of having a flash flood event in those grid-boxes with zero rainfall
      ind_no_NaN = np.where(fc >= 0)[0] # remove the NaN
      fc = fc[ind_no_NaN]
      obs = obs[ind_no_NaN]

      # Computing the bootstrapped contingency tables
      h = []
      m = []
      fa = []
      cn = []
      for ind_Thr in range(len(Thr_list)):
            Thr = Thr_list[ind_Thr]
            h.append(np.where((obs>0) & (fc>=Thr))[0].shape[0])
            m.append(np.where((obs>0) & (fc<Thr))[0].shape[0])
            fa.append(np.where((obs==0) & (fc>=Thr))[0].shape[0])
            cn.append(np.where((obs==0) & (fc<Thr))[0].shape[0])

      # Storing the bootstrapped contingency tables
      h_bs[:, ind_BS] = h
      m_bs[:, ind_BS] = m
      fa_bs[:, ind_BS] = fa
      cn_bs[:, ind_BS] = cn

# Printing on screen the contingency table
Tot_NumGB_Verif_Per = (h_bs + m_bs + fa_bs + cn_bs)[0]
print("Total n. of grid-boxes in the verification period:", Tot_NumGB_Verif_Per)
print()
print("Hits:")
print(h_bs / Tot_NumGB_Verif_Per * 100)
print()
print("Misses:")
print(m_bs / Tot_NumGB_Verif_Per * 100)
print()
print("False alarms:")
print(fa_bs / Tot_NumGB_Verif_Per * 100)
print()
print("Correct negatives:")
print(cn_bs / Tot_NumGB_Verif_Per * 100)

# Computing the verification scores
print()
print("Computing the verification scores")
total_bs = h_bs + m_bs + fa_bs + cn_bs
h_chance_bs = (h_bs + fa_bs) * (h_bs + m_bs) / total_bs
hr_bs = h_bs / (h_bs + m_bs) 
far_bs = fa_bs / (fa_bs + cn_bs)
bias_bs =  (h_bs + fa_bs) / (h_bs + m_bs)
pss_bs = (h_bs / (h_bs + m_bs)) - (fa_bs / (fa_bs + cn_bs))
ets_bs = (h_bs - h_chance_bs) / (h_bs + m_bs + fa_bs - h_chance_bs)

# Plotting and saving the verification scores
print()
print("Plotting and saving the verification scores")


###########
# Roc curve #
###########

plt.figure(figsize=(6,6))

far = far_bs[:,0]
hr = hr_bs[:,0]
far = np.insert(far, 0, 1)
hr = np.insert(hr, 0, 1)
far = np.append(far, 0)
hr = np.append(hr, 0)

far_lower_error = np.percentile(far_bs[:,1:], (100-CL)/2, axis = 1)
hr_lower_error = np.percentile(hr_bs[:,1:], (100-CL)/2, axis = 1)
far_lower_error = np.insert(far_lower_error, 0, 1)
hr_lower_error = np.insert(hr_lower_error, 0, 1)
far_lower_error = np.append(far_lower_error, 0)
hr_lower_error = np.append(hr_lower_error, 0)

far_upper_error = np.percentile(far_bs[:,1:], (100 - (100-CL)/2), axis = 1)
hr_upper_error = np.percentile(hr_bs[:,1:], (100 - (100-CL)/2), axis = 1)
far_upper_error = np.insert(far_upper_error, 0, 1)
hr_upper_error = np.insert(hr_upper_error, 0, 1)
far_upper_error = np.append(far_upper_error, 0)
hr_upper_error = np.append(hr_upper_error, 0)

vertices = np.concatenate([np.column_stack([far_lower_error, hr_lower_error]), np.column_stack([far_upper_error, hr_upper_error])[::-1]])
codes = np.concatenate([np.full(far_lower_error.shape, Path.LINETO), np.full(far_upper_error.shape, Path.LINETO)])
codes[0] = Path.MOVETO
codes[len(far_lower_error)] = Path.MOVETO
path = Path(vertices, codes)
patch = PathPatch(path, facecolor="#E0115F", alpha=0.25, edgecolor='none')

plt.plot(far, hr, "o-", color="#E0115F", linewidth=1, markersize=2)

ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tick_params(left=False, right=False, top=False, bottom=False)
ax.tick_params(axis="x", colors="#36454F")
ax.tick_params(axis="y", colors="#36454F")

plt.xlim([-0.005, 1])
ax.set_xticks(np.arange(0, 1.1, 0.1))
plt.ylim([-0.005,1])
ax.set_yticks(np.arange(0, 1.1, 0.1))
plt.plot([0,1], [0,1], "-", color="#2F11F5", linewidth=0.5)

ax.add_patch(patch)

plt.grid(color='grey', linewidth=0.5)

FileOUT = MainDirOUT + "/roc.jpeg"
plt.savefig(FileOUT, format="jpeg", bbox_inches="tight", dpi=1000)
plt.close()


###############
# Frequency Bias #
###############

var = bias_bs
VarName = "bias"

lower_error = np.percentile(var[:,1:], (100-CL)/2, axis = 1)
upper_error = np.percentile(var[:,1:], (100 - (100-CL)/2), axis = 1)

plt.figure(figsize=(6,6))
plt.plot(Thr_list, var[:,0], "o-", color="#E0115F", linewidth=1, markersize=2)
plt.fill_between(Thr_list, lower_error, upper_error, color="#E0115F", alpha=0.25, edgecolor="none")

ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_color("#36454F")
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tick_params(left=False, right=False, top=False)
ax.tick_params(axis="x", colors="#36454F")
ax.tick_params(axis="y", colors="#36454F")

plt.xlim([-0.1, np.max(Thr_list) + 0.1])
ax.set_xticks(np.arange(0, np.max(Thr_list) + 1))

ax.set_ylim(bottom=-20)
plt.plot([-0.1,np.max(Thr_list) + 0.1], [1,1], "-", color="#2F11F5", linewidth=0.5)
plt.plot([-0.1,np.max(Thr_list) + 0.1], [0,0], "-", color="#2F11F5", linewidth=0.5)

plt.grid(axis="y", color="silver", linewidth=0.5)

FileOUT = MainDirOUT + "/" + VarName + ".jpeg"
plt.savefig(FileOUT, format="jpeg", bbox_inches="tight", dpi=1000)
plt.close()


#################
# Peirce's skill score #
#################

var = pss_bs
VarName = "pss"

lower_error = np.percentile(var[:,1:], (100-CL)/2, axis = 1)
upper_error = np.percentile(var[:,1:], (100 - (100-CL)/2), axis = 1)

plt.figure(figsize=(6,6))
plt.plot(Thr_list, var[:,0], "o-", color="#E0115F", linewidth=1, markersize=2)
plt.fill_between(Thr_list, lower_error, upper_error, color="#E0115F", alpha=0.25, edgecolor="none")

ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_color("#36454F")
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tick_params(left=False, right=False, top=False)
ax.tick_params(axis="x", colors="#36454F")
ax.tick_params(axis="y", colors="#36454F")

plt.xlim([-0.1, np.max(Thr_list) + 0.1])
ax.set_xticks(np.arange(0, np.max(Thr_list) + 1))

plt.ylim([-1.2,1.1])
ax.set_yticks(np.arange(-0.9, 1, 0.2))
plt.plot([-0.1,np.max(Thr_list) + 0.1], [1,1], "-", color="#2F11F5", linewidth=0.5)
plt.plot([-0.1,np.max(Thr_list) + 0.1], [0,0], "-", color="#2F11F5", linewidth=0.5)
plt.plot([-0.1,np.max(Thr_list) + 0.1], [-1,-1], "-", color="#2F11F5", linewidth=0.5)

plt.grid(axis="y", color="silver", linewidth=0.5)

FileOUT = MainDirOUT + "/" + VarName + ".jpeg"
plt.savefig(FileOUT, format="jpeg", bbox_inches="tight", dpi=1000)
plt.close()


#####################
# Equitable threat score #
#####################

var = ets_bs
VarName = "ets"

lower_error = np.percentile(var[:,1:], (100-CL)/2, axis = 1)
upper_error = np.percentile(var[:,1:], (100 - (100-CL)/2), axis = 1)

plt.figure(figsize=(6,6))
plt.plot(Thr_list, var[:,0], "o-", color="#E0115F", linewidth=1, markersize=2)
plt.fill_between(Thr_list, lower_error, upper_error, color="#E0115F", alpha=0.25, edgecolor="none")

ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_color("#36454F")
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tick_params(left=False, right=False, top=False)
ax.tick_params(axis="x", colors="#36454F")
ax.tick_params(axis="y", colors="#36454F")

plt.xlim([-0.1, np.max(Thr_list) + 0.1])
ax.set_xticks(np.arange(0, np.max(Thr_list) + 1))

plt.ylim([-0.49,1])
ax.set_yticks(np.arange(-0.3, 1.1, 0.2))
plt.plot([-0.1,np.max(Thr_list) + 0.1], [1,1], "-", color="#2F11F5", linewidth=0.5)
plt.plot([-0.1,np.max(Thr_list) + 0.1], [0,0], "-", color="#2F11F5", linewidth=0.5)
plt.plot([-0.1,np.max(Thr_list) + 0.1], [-1/3,-1/3], "-", color="#2F11F5", linewidth=0.5)

plt.grid(axis="y", color="silver", linewidth=0.5)

FileOUT = MainDirOUT + "/" + VarName + ".jpeg"
plt.savefig(FileOUT, format="jpeg", bbox_inches="tight", dpi=1000)
plt.close()