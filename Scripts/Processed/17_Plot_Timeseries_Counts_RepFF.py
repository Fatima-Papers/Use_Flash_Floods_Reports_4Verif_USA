import os
import numpy as np
import matplotlib.pyplot as plt

###########################################################################
# CODE DESCRIPTION
# 17_Plot_Timeseries_Counts_RepFF.py plots the yearly timeseries of the counts of flood 
# reports in the NOAA database, comparing the counts of all reports and only flash flood 
# ones. 
# Runtime: negligible.

# INPUT PARAMETERS DESCRIPTION
# Git_Repo (string): repository's local path.
# DirIN (string): relative path of the directory containing the flash flood reports.
# DirOUT (string): relative path of the directory containing the timeseries plot.

# INPUT PARAMETERS
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Compute/16_Extract_NOAA_RepFF"
DirOUT = "Data/Plot/17_Timeseries_Counts_RepFF"
###########################################################################

# Read the data to plot
MainDirIN = Git_Repo + "/" + DirIN
years_rep = np.load(MainDirIN + "/Years.npy")
num_rep_all = np.load(MainDirIN + "/Counts_RepALL.npy")
num_rep_ff = np.load(MainDirIN + "/Counts_RepFF.npy")
num_rep_ff_withCoord = np.load(MainDirIN + "/Counts_RepFF_withCoord.npy")

# Plot the counts
fig, ax = plt.subplots(figsize=(10, 8))
index = np.arange(len(years_rep))
bar_width = 0.7
opacity = 1

rects1 = ax.bar(years_rep, num_rep_all, bar_width, alpha=opacity, color="gainsboro", align='center', label="All flood types")
rects2 = ax.bar(years_rep, num_rep_ff, bar_width, alpha=opacity, color="maroon", align='center', label="Only flash floods")
rects3 = ax.bar(years_rep, num_rep_ff_withCoord, bar_width, alpha=opacity, color="red", align='center', label="Only flash floods with lat/lon coordinates")

ax.set_xlabel("Years", fontsize=16, labelpad = 10)
ax.set_ylabel("Counts", fontsize=16, labelpad = 10)
ax.set_title("Count of flood reports per year", fontsize=18, pad=15, weight = "bold")
ax.legend(fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=16)

# Saving the plots
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
    os.makedirs(MainDirOUT)
FileOUT = MainDirOUT + "/Timeseries_Counts_RepFF.jpeg" 
plt.savefig(FileOUT, format="jpeg", bbox_inches="tight", dpi=2500)