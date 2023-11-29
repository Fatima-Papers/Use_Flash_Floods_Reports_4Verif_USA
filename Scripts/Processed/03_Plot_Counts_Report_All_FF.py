import os
import numpy as np
import matplotlib.pyplot as plt

##########################################################################
# CODE DESCRIPTION
# 03_Plot_Counts_Report_All_FF.py plots the counts of reports, all and only flash floods. 
# Runtime: negligible.

# INPUT PARAMETERS DESCRIPTION
# Git_Repo (string): repository's local path
# DirIN (string): relative path where USA's mask can be found
# DirOUT (string): relative path where to store the plot 

# INPUT PARAMETERS
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Compute/02_Extract_NOAA_Reports"
DirOUT = "Data/Compute/03_Counts_Report_All_FF"
##########################################################################

# Read the data to plot
MainDirIN = Git_Repo + "/" + DirIN
years_rep = np.load(MainDirIN + "/years_rep.npy")
num_rep_all = np.load(MainDirIN + "/num_rep_all.npy")
num_rep_ff = np.load(MainDirIN + "/num_rep_ff.npy")
print(years_rep)
print(num_rep_all)
print(num_rep_ff)
exit()

# Plot the counts
fig, ax = plt.subplots()
index = np.arange(len(years_rep))
bar_width = 0.4
opacity = 0.8

rects1 = ax.bar(years_rep, num_rep_all, bar_width, alpha=opacity, color='b', label="num_rep_all")
rects2 = ax.bar(years_rep, num_rep_ff, bar_width, alpha=opacity, color='r', label="num_rep_ff")

ax.set_xlabel("Years")
ax.set_ylabel("Counts")
ax.set_title("Count per year of all reports and only flash floods reports")
#ax.set_xticks(index)
#ax.set_xticklabels(('A', 'B', 'C', 'D', 'E'))
ax.legend()

plt.show()