import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import metview as mv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#######################################################################################
# CODE DESCRIPTION
# 17_Plot_Timeseries_Point_Gridded_AccRepFF.py plots a timeseries of the point and accumulated reports 
# over a specific accumulation period.
# Runtime: The code takes up to 5 minutes to run in serial mode.

# INPUT PARAMETERS DESCRIPTION
# YearS (year, in YYYY format): start year for the analysis period.
# YearF (year, in YYYY format): final year for the analysis period.
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Git_Repo (string): repository's local path.
# DirIN_Point_AccRepFF (string): relative path where the accumulated point flood reports are stored.
# DirIN_Gridded_AccRepFF (string): relative path where the accumulated gridded flood reports are stored.
# DirOUT (string): relative path where to store the timeseries plot. 

# INPUT PARAMETERS
YearS = 2005
YearF = 2023
Acc = 12
Disc_Acc = 12
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN_Point_AccRepFF = "Data/Compute/14_Point_AccRepFF"
DirIN_Grid_AccRepFF = "Data/Compute/16_Gridded_AccRepFF"
DirOUT = "Data/Plot/17_Timeseries_Point_Gridded_AccRepFF"
#######################################################################################

# Plotting the timeseries of the point and accumulated reports for specific accumulation periods
print("Plotting the timeseries of the point and accumulated reports for specific accumulation periods for:")
for Year in range(YearS, YearF+1):

      print(" - " + str(Year))

      DateTime_Start_S = datetime(Year,1,1,0)
      if Year != YearF:
            DateTime_Start_F = datetime(Year,12,31,12)
      else:
            DateTime_Start_F = datetime(Year,12,30,12)

      dates = []
      Counts_Point_AccRepFF = []
      Counts_Grid_AccRepFF = []

      TheDateTime_Start = DateTime_Start_S
      while TheDateTime_Start <= DateTime_Start_F:

            TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)
            dates.append(TheDateTime_Final)
            
            # Reading the reports 
            FileIN_Grid_AccRepFF = Git_Repo + "/" + DirIN_Grid_AccRepFF + "/" + TheDateTime_Final.strftime("%Y") + "/" + TheDateTime_Final.strftime("%Y%m%d") + "/FlashFloodRep_" + TheDateTime_Final.strftime("%Y%m%d%H") + ".grib"
            Grid_AccRepFF = mv.values(mv.read(FileIN_Grid_AccRepFF))
            Num_Grid_AccRepFF = np.nansum(Grid_AccRepFF>0)
            
            if Num_Grid_AccRepFF == 0:

                  Counts_Point_AccRepFF.append(0)
                  Counts_Grid_AccRepFF.append(0)

            else:
                  
                  FileIN_Point_AccRepFF = Git_Repo + "/" + DirIN_Point_AccRepFF + "/" + TheDateTime_Final.strftime("%Y") + "/" + TheDateTime_Final.strftime("%Y%m%d") + "/FlashFloodRep_" + TheDateTime_Final.strftime("%Y%m%d%H") + ".csv"
                  ff = pd.read_csv(FileIN_Point_AccRepFF)

                  Counts_Point_AccRepFF.append(Num_Grid_AccRepFF)
                  Counts_Grid_AccRepFF.append(len(ff))

            TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)
      
      # Plot the histogram with the counts
      fig, ax = plt.subplots(figsize=(10, 8))
      rects1 = ax.bar(dates, Counts_Point_AccRepFF, 0.5, color="black", align='center', label="Point_AccRepFF")
      rects2 = ax.bar(dates, Counts_Grid_AccRepFF, 0.5, color="red", align='center', label="Grid_AccRepFF")
      ax.xaxis.set_major_locator(mdates.MonthLocator())
      ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
      plt.xticks(rotation=30)
      ax.set_xlabel("Dates", fontsize=16, labelpad = 10)
      ax.set_ylabel("Counts", fontsize=16, labelpad = 10)
      ax.set_title("Count of flood reports in " + str(Year), fontsize=18, pad=15, weight = "bold")
      ax.legend(fontsize=14)
      ax.tick_params(axis='both', which='major', labelsize=16)

      # Save the plot
      MainDirOUT = Git_Repo + "/" + DirOUT
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      FileOUT = MainDirOUT + "/Timeseries_Point_Gridded_AccRepFF_" + str(Year) + ".png"
      plt.savefig(FileOUT, dpi=1000)