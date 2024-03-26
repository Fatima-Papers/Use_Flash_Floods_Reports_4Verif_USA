import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv
import matplotlib.pyplot as plt

#################################################################################################
# CODE DESCRIPTION
# 29_Plot_Doughnut_Chart_repFF.py creates a doughnut chart of the distribution of accumulated gridded flash flood 
# reports in the north-west (NW), north-east(NE), south-west (Sw) and south-east (SE) of the US.
# Runtime: the script can take up to 1 to 10 minutes to run in serial depending on how many years are considered to 
# build the cart.

# INPUT PARAMETERS DESCRIPTION
# DateTime_Final_S (date and time): start date (first three numbers) and time (fourth number) for the considered period (representing the end of the accumulation period).
# DateTime_Final_F (date and time): final date (first three numbers) and time (fourth number) for the considered period (representing the end of the accumulation period).
# Disc_Acc (integer, in hours): discretization for the accumulation periods to consider.
# North_South_LatBoundary (integer, from -90 to +90): value of the latitude boundary that separates north from south.
# West_East_LonBoundary (integer, from -180 to +180): value of the longitude boundary that separates west from east.
# Git_Repo (string): repository's local path.
# DirIN (string): relative path of the directory containg the accumulated gridded flash flood reports.
# DirOUT (string): relative path of the directory containing the doughnut chart.

# INPUT PARAMETERS
DateTime_Final_S = datetime(2021,1,1,12)
DateTime_Final_F = datetime(2022,1,1,0)
Disc_Acc = 12
North_South_LatBoundary = 38
West_East_LonBoundary = -100
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Compute/16_Gridded_AccRepFF"
DirOUT = "Data/Plot/29_Doughnut_Chart_repFF"
#################################################################################################

print()
print("Creating a doughnut chart of the counts of flash flood events in the US between " + DateTime_Final_S.strftime("%Y%m%d") + " and " + DateTime_Final_F.strftime("%Y%m%d"))
print("Reading reports for:") 

# Adding up the number of flood reports observed in the considered period
Grid_AccRepFF_Total = 0
TheDateTime_Final = DateTime_Final_S
while TheDateTime_Final <= DateTime_Final_F:
      print(" - " + TheDateTime_Final.strftime("%Y%m%d%H"))
      Grid_AccRepFF_Period = mv.read(Git_Repo + "/" + DirIN + "/" + TheDateTime_Final.strftime("%Y") + "/" + TheDateTime_Final.strftime("%Y%m%d") + "/FlashFloodRep_" + TheDateTime_Final.strftime("%Y%m%d%H") + ".grib")
      Grid_AccRepFF_Total = Grid_AccRepFF_Total + Grid_AccRepFF_Period
      TheDateTime_Final = TheDateTime_Final + timedelta(hours=Disc_Acc)

# Defining the count of accumulated gridded flash flood reports in four regions of US (i.e. NW, NE, SW, and SE)
lats = mv.latitudes(Grid_AccRepFF_Total)
lons = mv.longitudes(Grid_AccRepFF_Total) - 360
mask_nw = np.where((lats >= North_South_LatBoundary) & (lons <= West_East_LonBoundary))[0]
mask_ne = np.where((lats >= North_South_LatBoundary) & (lons > West_East_LonBoundary))[0]
mask_sw = np.where((lats < North_South_LatBoundary) & (lons <= West_East_LonBoundary))[0]
mask_se = np.where((lats < North_South_LatBoundary) & (lons > West_East_LonBoundary))[0]
Grid_AccRepFF_Total_vec = mv.values(Grid_AccRepFF_Total)
Grid_AccRepFF_Total_nw = np.nansum(Grid_AccRepFF_Total_vec[mask_nw])
Grid_AccRepFF_Total_ne = np.nansum(Grid_AccRepFF_Total_vec[mask_ne])
Grid_AccRepFF_Total_sw = np.nansum(Grid_AccRepFF_Total_vec[mask_sw])
Grid_AccRepFF_Total_se = np.nansum(Grid_AccRepFF_Total_vec[mask_se])

# Creating the doughnut chart
Labels = ["NW", "NE", "SW", "SE"]
Values = [Grid_AccRepFF_Total_nw, Grid_AccRepFF_Total_ne, Grid_AccRepFF_Total_sw, Grid_AccRepFF_Total_se]
Colours = ["#9A617F", "#F3734D", "#ECA220", "#B4BB3B"]
Explode = (0.01, 0.01, 0.01, 0.01)

plt.pie(Values, colors=Colours, labels=Labels, explode=Explode, startangle=90, pctdistance=0.85)

total_values_sum = int(sum(Values))
centre_circle = plt.Circle((0, 0), 0.50, fc='white', linewidth=0)
plt.text(0, 0, f'Total Reports\n{total_values_sum}', ha='center', va='center', fontsize=14)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.axis('equal')

plt.show()