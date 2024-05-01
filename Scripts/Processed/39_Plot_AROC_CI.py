import os
import numpy as np
import matplotlib.pyplot as plt

##########################################################################################
# CODE DESCRIPTION
# 39_Plot_AROC_CI.py plots AROC and confidence intervals (CI).
# Note: runtime negligible.

# INPUT PARAMETERS DESCRIPTION
# Acc (number, in hours): rainfall accumulation to consider.
# EFFCI_list (list of integers, from 1 to 10): list of EFFCI indexes to consider.
# MagnitudeInPerc_Rain_Event_FR_list (list of integers, from 0 to 100): list of magnitudes, in 
#     percentiles, of rainfall events that can potentially conduct to flash floods.
# CL (integer from 0 to 100, in percent): confidence level for the definition of the confidence intervals.
# RegionName_list (list of strings): list of names for the domain's regions.
# SystemFC_list (list of strings): list of names of forecasting systems to consider.
# Colour_SystemFC_list (list of strings): colours used to plot the AROC values for different forecasting systems.
# Git_repo (string): repository's local path.
# DirIN (string): relative path containing the real and boostrapped AROC values.
# DirOUT (string):  relative path of the directory containing the plots of the real and boostrapped AROC values.

# INPUT PARAMETERS
Acc = 12
Perc_VRT = 99.9
CL = 95
SystemFC = "ecPoint"
ROC_list = ["True", "Pseudo_0.1", "Pseudo_1", "Pseudo_2", "Pseudo_3", "Pseudo_4", "Pseudo_5"]
Colour_ROC_List = ["black", "magenta", "blue", "red", "green", "brown", "cyan"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Compute/38_AROC_BS"
DirOUT = "Data/Plot/39_AROC_BS"
##########################################################################################

# Setting the figure
fig, ax = plt.subplots(figsize=(14, 10))

for ind in range(len(ROC_list)):

      ROC = ROC_list[ind]
      Colour_ROC = Colour_ROC_List[ind]

      # Reading the steps computed, and the original and bootstrapped AROC values
      FileIN = Git_Repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/AROC_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(Perc_VRT) + "_" + ROC + ".npy"
      StepF = np.load(FileIN)[:,0].astype(int)
      aroc_real = np.load(FileIN)[:,1]
      #aroc_BS = np.load(FileIN)[:,2:]

      # # Computing the confidence intervals from the bootstrapped AROC values
      # alpha = 100 - CL # significance level (in %)
      # CI_lower = np.nanpercentile(aroc_BS, alpha/2, axis=1)
      # CI_upper = np.nanpercentile(aroc_BS, 100 - (alpha/2), axis=1)

      # Plotting the AROC values
      ax.plot(StepF, aroc_real, "o-", color=Colour_ROC, label=ROC, linewidth=3)
      #ax.fill_between(StepF, CI_lower, CI_upper, color=Colour_SystemFC, alpha=0.2, edgecolor="none")

      # Setting the plot metadata
      ax.plot([StepF[0], StepF[-1]], [0.5, 0.5], "-", color="grey", linewidth=2)
      DiscStep = ((StepF[-1] - StepF[0]) / (len(StepF)-1))
      #ax.set_title("Area Under the ROC curve\n" + r"EFFCI>=" + str(EFFCI) + ", VRT>=tp(" + str(MagnitudeInPerc_Rain_Event_FR) + "th percentile), Region=" +  RegionName + ", CL=" + str(CL) + "%", fontsize=20, pad=40, color="#333333", weight="bold")
      ax.set_xlabel("Step ad the end of the " + str(Acc) + "-hourly accumulation period [hours]", fontsize=20, labelpad=10, color="#333333")
      ax.set_ylabel("AROC [-]", fontsize=20, labelpad=10, color="#333333")
      ax.set_xlim([StepF[0]-1, StepF[-1]+1])
      ax.set_ylim([0.4,1])
      ax.set_xticks(np.arange(StepF[0], (StepF[-1]+1), DiscStep))
      ax.set_yticks(np.arange(0.4,1.1, 0.1))
      ax.xaxis.set_tick_params(labelsize=20, rotation=90, color="#333333")
      ax.yaxis.set_tick_params(labelsize=20, color="#333333")
      ax.legend(loc="upper center",  bbox_to_anchor=(0.5, 1.08), ncol=2, fontsize=20, frameon=False)
      ax.grid()

# Saving the plot
DirOUT_temp= Git_Repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
FileNameOUT_temp = "AROC_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(Perc_VRT) + ".jpeg"
if not os.path.exists(DirOUT_temp):
      os.makedirs(DirOUT_temp)
plt.savefig(DirOUT_temp + "/" + FileNameOUT_temp)
plt.close() 