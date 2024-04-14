import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

########################################################################################################
# CODE DESCRIPTION
# 22_Plot_Timeseries_Point_Grid_AccRepFF.py plots the daily timeseries per year of the counts of point and gridded 
# accumulated flash flood reports.
# Runtime: The code takes up to 10 minutes to run in serial mode.

# INPUT PARAMETERS DESCRIPTION
# Year_S (year, in YYYY format): start year to consider.
# Year_F (year, in YYYY format): final year to consider.
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation periods to consider.
# Git_Repo (string): repository's local path.
# DirIN_Grid_AccRepFF (string): relative path of the directory containing the accumulated point flash flood reports per grid-box.
# DirOUT (string): relative path containing the timeseries plots. 

# INPUT PARAMETERS
Year_S = 2005
Year_F = 2023
Acc = 12
Disc_Acc = 12
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN_Grid_AccRepFF = "Data/Compute/19_Grid_AccRepFF"
DirOUT = "Data/Plot/22_Timeseries_Point_Grid_AccRepFF"
########################################################################################################


# Plotting the daily timeseries per year of the counts of point and gridded accumulated flash flood reports
print()
print("Plotting the daily timeseries of the counts of point and gridded accumulated flash flood reports for:")
for Year in range(Year_S, Year_F+1):

      print(" - " + str(Year))

      # Defining the accumulation periods to consider
      TheDateTime_Start_S = datetime(Year,1,1,0)
      TheDateTime_Start_F = datetime(Year,12,31,24-Disc_Acc)
      
      # Initializing the variables that will contain the count of point and gridded accumulated flash flood reports
      Dates_all = []
      Count_Point_AccRepFF_all = []
      Count_Grid_AccRepFF_all = []

      # Computing the counts of point and gridded accumulated flash flood reports per accumulation period
      TheDateTime_Start = TheDateTime_Start_S
      while TheDateTime_Start <= TheDateTime_Start_F:

            TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)
            Dates_all.append(TheDateTime_Final)
            
            # Reading the point and gridded accumulated flash flood reports
            FileIN_AccRepFF = Git_Repo + "/" + DirIN_Grid_AccRepFF + "/" + TheDateTime_Final.strftime("%Y") + "/" + TheDateTime_Final.strftime("%Y%m%d") + "/Grid_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d%H") + ".grib"
            Point_AccRepFF_grib = mv.read(FileIN_AccRepFF)
            Grid_AccRepFF_grib = (Point_AccRepFF_grib > 0)

            # Defining the counts of point and gridded accumulated flash flood reports 
            Count_Point_AccRepFF_accper = np.nansum(mv.values(Point_AccRepFF_grib))
            Count_Grid_AccRepFF_accper = np.nansum(mv.values(Grid_AccRepFF_grib))
            Count_Point_AccRepFF_all.append(Count_Point_AccRepFF_accper)
            Count_Grid_AccRepFF_all.append(Count_Grid_AccRepFF_accper)

            TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)
      
      # Plot the histogram with the counts
      fig, ax = plt.subplots(figsize=(25, 8))
      rects1 = ax.bar(Dates_all, Count_Point_AccRepFF_all, 0.5, color="black", align='center', label="Point")
      rects2 = ax.bar(Dates_all, Count_Grid_AccRepFF_all, 0.5, color="red", align='center', label="Grid")
      ax.xaxis.set_major_locator(mdates.MonthLocator())
      ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
      plt.xticks(rotation=30)
      ax.set_xlabel("End of " + str(Acc) + "-h accumulation periods", fontsize=16, labelpad = 15)
      ax.set_ylabel("Counts", fontsize=16, labelpad = 10)
      ax.set_title("Count of point and gridded accumulated flash flood reports in " + str(Year), fontsize=18, pad=15, weight = "bold")
      ax.legend(fontsize=14)
      ax.tick_params(axis='both', which='major', labelsize=16)

      # Save the plot
      MainDirOUT = Git_Repo + "/" + DirOUT
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      FileOUT = MainDirOUT + "/Timeseries_Point_Grid_AccRepFF_" + str(Year) + ".png"
      plt.savefig(FileOUT, format="jpeg", bbox_inches="tight", dpi=1000)