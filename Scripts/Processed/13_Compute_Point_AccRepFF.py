import os
from datetime import datetime, timedelta
import pandas as pd

##############################################################################################################################################
# CODE DESCRIPTION
# 07_Compute_Point_Accumulated_RepFF.py creates the accumulated flash flood reports over the same rainfall accumulation periods.
# Runtime: the code takes up to 30 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# DateTime_Start_S (date and time): start date (first three numbers) and time (fourth number) for the analysis period (representing the beginning of the accumulation period).
# DateTime_Start_F (date and time): final date (first three numbers) and time (fourth number) for the analysis period (representing the beginning of the accumulation period).
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Git_Repo (string): repository's local path
# FileIN (string): relative path of the file containing the flash flood reports.
# DirOUT (string): relative path where to store the plot 

# INPUT PARAMETERS
DateTime_Start_S = datetime(1996,1,1,0)
DateTime_Start_F = datetime(2023,12,31,12)
Acc = 12
Disc_Acc = 12
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN = "Data/Compute/05_Extract_NOAA_Rep/FlashFloodRep.csv"
DirOUT = "Data/Compute/07_Point_Accumulated_RepFF"
##############################################################################################################################################


# Reading the flash flood reports
ff = pd.read_csv(Git_Repo + "/" + FileIN)

# Converting the date from string to datetime object
ff["BEGIN_DATE_TIME_UTC"] = pd.to_datetime(ff["BEGIN_DATE_TIME_UTC"])
ff["END_DATE_TIME_UTC"] = pd.to_datetime(ff["END_DATE_TIME_UTC"])

# Post-processing the flash flood reports
TheDateTime_Start = DateTime_Start_S
while TheDateTime_Start <= DateTime_Start_F:
      
      # Select the flash flood reports for a specific accumulation period
      TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)
      print("Accumulating flood reports occurred between " + TheDateTime_Start.strftime("%Y-%m-%d") + " (included) and " + TheDateTime_Final.strftime("%Y-%m-%d") + " (excluded)")
      filtered_ff = ff[(ff["BEGIN_DATE_TIME_UTC"] >= TheDateTime_Start) & (ff["END_DATE_TIME_UTC"] < TheDateTime_Final)]
      filtered_ff = filtered_ff.reset_index(drop=True)  # to reset the indexes of the new dataframe

      # Saving the filtered files
      filtered_ff_size = len(filtered_ff)
      if filtered_ff_size != 0:
            print(" - Saving " + str(filtered_ff_size) + " reports for " + TheDateTime_Final.strftime("%Y%m%d%H"))
            MainDirOUT = Git_Repo + "/" + DirOUT + "/" + TheDateTime_Final.strftime("%Y") + "/" + TheDateTime_Final.strftime("%Y%m%d")
            if not os.path.exists(MainDirOUT):
                  os.makedirs(MainDirOUT)
            FileOUT = MainDirOUT + "/FlashFloodRep_" + TheDateTime_Final.strftime("%Y%m%d%H") + ".csv"
            filtered_ff.to_csv(FileOUT, index=False)
      else: 
            print(" - No reports to save")
      
      TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)