import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv
import matplotlib.pyplot as plt

#################################################################################################
# CODE DESCRIPTION
# 20_Plot_Doughnut_Chart_Point_AccRepFF_PerGrid.py plots a doughnut chart of the distribution of the accumulated  
# point flash flood reports per grid-box in the north-west (NW), north-east(NE), south-west (SW) and south-east (SE) of 
# the US.
# Runtime: the script takes up to 10 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year_S (integer): start year to consider.
# Year_F (integer): final year to consider.
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation periods to consider.
# North_South_LatBoundary (integer, from -90 to +90): value of the latitude boundary that separates north from south.
# West_East_LonBoundary (integer, from -180 to +180): value of the longitude boundary that separates west from east.
# Git_Repo (string): repository's local path.
# DirIN (string): relative path of the directory containing the accumulated point flash flood reports per grid-box.
# DirOUT (string): relative path of the directory containing the doughnut chart.

# INPUT PARAMETERS
Year_S = 2005
Year_F= 2023
Acc = 12
Disc_Acc = 12
North_South_LatBoundary = 38
West_East_LonBoundary = -100
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Compute/19_Grid_AccRepFF"
DirOUT = "Data/Plot/20_Doughnut_Chart_Point_AccRepFF_PerGrid"
#################################################################################################


print()
print("Plotting the doughnut chart of the distribution of the accumulated gridded flash flood reports in the north-west (NW), north-east(NE), south-west (SW) and south-east (SE) of the US")

# Defining the accumulation periods to consider
TheDateTime_Start_S = datetime(Year_S,1,1,0)
TheDateTime_Start_F = datetime(Year_F,12,31,24-Disc_Acc)

# Initializing the variable that will store the absolute frequency of accumulated gridded flash flood reports per grid-box within the considered period
AbsFreq_Grid_AccRepFF = 0

# Adding up the number of accumulated gridded flash flood reports observed within the considered period
print()
print("Computing the relative frequency of " + str(Acc) + "-hourly gridded flash flood reports in each grid-box of the domain between " + str(Year_S) + " and " + str(Year_F))
print("Adding the reports in the period ending:")
TheDateTime_Start = TheDateTime_Start_S
while TheDateTime_Start <= TheDateTime_Start_F:
      TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)
      print(" - on " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC")
      FileIN_Grid_AccRepFF_SinglePer = Git_Repo + "/" + DirIN + "/" + TheDateTime_Final.strftime("%Y") + "/" + TheDateTime_Final.strftime("%Y%m%d") + "/Grid_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d%H") + ".grib"
      Grid_AccRepFF_SinglePer = mv.read(FileIN_Grid_AccRepFF_SinglePer)
      AbsFreq_Grid_AccRepFF = AbsFreq_Grid_AccRepFF + Grid_AccRepFF_SinglePer
      TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)

# Defining the count of accumulated gridded flash flood reports in four regions of US (i.e. NW, NE, SW, and SE)
lats = mv.latitudes(AbsFreq_Grid_AccRepFF)
lons = mv.longitudes(AbsFreq_Grid_AccRepFF) - 360
mask_nw = np.where((lats >= North_South_LatBoundary) & (lons <= West_East_LonBoundary))[0]
mask_ne = np.where((lats >= North_South_LatBoundary) & (lons > West_East_LonBoundary))[0]
mask_sw = np.where((lats < North_South_LatBoundary) & (lons <= West_East_LonBoundary))[0]
mask_se = np.where((lats < North_South_LatBoundary) & (lons > West_East_LonBoundary))[0]
AbsFreq_Grid_AccRepFF_vec = mv.values(AbsFreq_Grid_AccRepFF)
AbsFreq_Grid_AccRepFF_nw = np.nansum(AbsFreq_Grid_AccRepFF_vec[mask_nw])
AbsFreq_Grid_AccRepFF_ne = np.nansum(AbsFreq_Grid_AccRepFF_vec[mask_ne])
AbsFreq_Grid_AccRepFF_sw = np.nansum(AbsFreq_Grid_AccRepFF_vec[mask_sw])
AbsFreq_Grid_AccRepFF_se = np.nansum(AbsFreq_Grid_AccRepFF_vec[mask_se])

# Creating the doughnut chart
Labels = ["NW", "SW", "SE", "NE"]
Values = [AbsFreq_Grid_AccRepFF_nw, AbsFreq_Grid_AccRepFF_sw, AbsFreq_Grid_AccRepFF_se, AbsFreq_Grid_AccRepFF_ne]
Colours = ["#EEA320", "#B4BC3D", "#00A4DC", "#1CB8A6"]
Explode = (0.01, 0.01, 0.01, 0.01)

Sum_Values = sum(Values)
Perc_Values = Values/Sum_Values*100
print()
print("Total number of accumulated gridded flash flood reports in the US = " + str(int(Sum_Values)))
print("Percentages per regions:")
for i in range(len(Perc_Values)):
      print(Labels[i] + " = " + str(np.round(Perc_Values[i], decimals=1)) + "%")

plt.pie(Values, colors=Colours, labels=Labels, startangle=90, pctdistance=0.85, explode=Explode, textprops={'fontsize': 16})
centre_circle = plt.Circle((0, 0), 0.50, color='white', linewidth=0)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.axis('equal')
plt.text(0, 0, f'Total\n{int(Sum_Values)}', ha='center', va='center', fontsize=16)

# Saving the doughnut chart
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
    os.makedirs(MainDirOUT)
FileOUT = MainDirOUT + "/Doughnut_Chart_Point_AccRepFF_PerGrid.jpeg" 
plt.savefig(FileOUT, format="jpeg", bbox_inches="tight", dpi=5000)