import os
import numpy as np
import matplotlib.pyplot as plt

###########################################################################
# CODE DESCRIPTION
# 13_Plot_Timeseries_Counts_FloodReports.py plots a timeseries of the counts of flood 
# reports, all and only flash floods and surface runoff. 
# Runtime: negligible.

# INPUT PARAMETERS DESCRIPTION
# Git_Repo (string): repository's local path
# DirIN (string): relative path where USA's mask can be found
# DirOUT (string): relative path where to store the plot 

# INPUT PARAMETERS
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Compute/12_Extract_NOAA_Rep"
DirOUT = "Data/Plot/13_Timeseries_Counts_FloodReports"
###########################################################################

# Read the data to plot
MainDirIN = Git_Repo + "/" + DirIN
years_rep = np.load(MainDirIN + "/years_rep.npy")
num_rep_all = np.load(MainDirIN + "/num_rep_all.npy")
num_rep_ff = np.load(MainDirIN + "/num_rep_ff.npy")

# Plot the counts
fig, ax = plt.subplots(figsize=(10, 8))
index = np.arange(len(years_rep))
bar_width = 0.7
opacity = 1

rects1 = ax.bar(years_rep, num_rep_all, bar_width, alpha=opacity, color="gainsboro", align='center', label="All flood types")
rects2 = ax.bar(years_rep, num_rep_ff, bar_width, alpha=opacity, color="red", align='center', label="Flash floods and surface runoff")

ax.set_xlabel("Years", fontsize=16, labelpad = 10)
ax.set_ylabel("Counts", fontsize=16, labelpad = 10)
ax.set_title("Count of flood reports", fontsize=18, pad=15, weight = "bold")
ax.legend(fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=16)

# Saving the plots
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
    os.makedirs(MainDirOUT)
FileOUT = MainDirOUT + "/Timeseries_Counts_FloodReports.jpeg" 
plt.savefig(FileOUT, format="jpeg")