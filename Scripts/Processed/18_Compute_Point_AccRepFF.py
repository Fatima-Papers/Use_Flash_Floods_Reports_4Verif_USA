import os
from datetime import datetime, timedelta
import pandas as pd

##################################################################################
# CODE DESCRIPTION
# 18_Compute_Point_AccRepFF.py creates the point accumulated flash flood reports over the same 
# rainfall accumulation periods.
# Runtime: the code takes up to 5 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year_S (integer): start year to consider.
# Year_F (integer): final year to consider.
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Git_Repo (string): repository's local path.
# FileIN (string): relative path of the file containing the flash flood reports.
# DirOUT (string): relative path of the directory containing the point accumulated flash flood reports.

# INPUT PARAMETERS
Year_S = 2005
Year_F = 2023
Acc = 12
Disc_Acc = 12
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN = "Data/Compute/16_Extract_NOAA_RepFF/RepFF.csv"
DirOUT = "Data/Compute/18_Point_AccRepFF"
##################################################################################

# Defining the accumulation periods to consider
TheDateTime_Start_S = datetime(Year_S,1,1,0)
TheDateTime_Start_F = datetime(Year_F,12,31,24-Disc_Acc)

# Reading the flash flood reports
ff = pd.read_csv(Git_Repo + "/" + FileIN)

# Converting the date from string to datetime object
ff["BEGIN_DATE_TIME"] = pd.to_datetime(ff["BEGIN_DATE_TIME"])
ff["END_DATE_TIME"] = pd.to_datetime(ff["END_DATE_TIME"])

# Accumulating the point flash flood reports
TheDateTime_Start = TheDateTime_Start_S
while TheDateTime_Start <= TheDateTime_Start_F:
      
      print()
      TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)
      print("Accumulating point flood reports between " + TheDateTime_Start.strftime("%Y-%m-%d") + " at " + TheDateTime_Start.strftime("%H") + " UTC and " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC")
      
      # Select the flash flood reports for the specific accumulation period
      filtered_ff = ff[(ff["BEGIN_DATE_TIME"] >= TheDateTime_Start) & (ff["BEGIN_DATE_TIME"] < TheDateTime_Final)]
      filtered_ff = filtered_ff.reset_index(drop=True)  # to reset the indexes of the new dataframe

      # Saving the filtered files
      filtered_ff_size = len(filtered_ff)
      if filtered_ff_size != 0:
            print(" - Saving " + str(filtered_ff_size) + " reports")
            MainDirOUT = Git_Repo + "/" + DirOUT + "/" + TheDateTime_Final.strftime("%Y") + "/" + TheDateTime_Final.strftime("%Y%m%d")
            if not os.path.exists(MainDirOUT):
                  os.makedirs(MainDirOUT)
            FileOUT = MainDirOUT + "/Point_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d%H") + ".csv"
            filtered_ff.to_csv(FileOUT, index=False)
      else: 
            print(" - No reports to save")
      
      TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)