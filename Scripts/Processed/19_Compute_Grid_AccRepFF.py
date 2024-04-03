import os
import sys
from datetime import datetime, timedelta
import pandas as pd
import metview as mv

###################################################################################
# CODE DESCRIPTION
# 19_Compute_Grid_AccRepFF.py computes the gridded accumulated flash flood reports 
# based on the point accumulated ones.
# Runtime: the code takes up to 3 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year (year, in YYYY format): year to consider.
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation periods to consider.
# Git_Repo (string): repository's local path.
# FileIN_Mask (string): relative path of the file containing the domain's mask.
# DirIN (string): relative path of the directory containing the point accumulated flash flood reports.
# DirOUT (string): relative path of the directory containing the gridded accumulated flash flood reports.

# INPUT PARAMETERS
Year = int(sys.argv[1])
Acc = 12
Disc_Acc = 12
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
DirIN = "Data/Compute/18_Point_AccRepFF"
DirOUT = "Data/Compute/19_Grid_AccRepFF"
###################################################################################

# Reading the mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)

# Defining the accumulation periods to consider
TheDateTime_Start_S = datetime(Year,1,1,0)
TheDateTime_Start_F = datetime(Year,12,31,24-Disc_Acc)

# Creating gridded accumulated flash flood reports
print()
print("Computing the gridded accumulated flash flood reports for the " + str(Acc) + "-hourly period ending:")
TheDateTime_Start = TheDateTime_Start_S
while TheDateTime_Start <= TheDateTime_Start_F:

      TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)
      print(" - on " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC")

      # Initializing the gridded field where to store the flash flood reports
      ff_grid = mv.values((mask == 1) * 0)

      # Reading the point accumulated flash flood reports
      FileIN = Git_Repo + "/" + DirIN + "/" + TheDateTime_Final.strftime("%Y") + "/" + TheDateTime_Final.strftime("%Y%m%d") + "/Point_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d%H") + ".csv"
      if os.path.exists(FileIN):
            ff = pd.read_csv(FileIN)
            len_ff = len(ff)
            for ind in range(len_ff):
                  lat_ff = ff["AREA_AFFECTED_CENTRE_LAT"].iloc[ind]
                  lon_ff = ff["AREA_AFFECTED_CENTRE_LON"].iloc[ind]
                  info = mv.nearest_gridpoint_info(mask, lat_ff, lon_ff)
                  if info[0] is not None: # there is not point that falls within the domain mask
                        index_ff_grid = int(info[0]["index"])
                        ff_grid[index_ff_grid] = ff_grid[index_ff_grid] + 1
      else:
            print("      Accumulation period with no flash flood reports.")

      # Converting the gridded field with flash flood reports into grib
      ff_grid = mv.set_values(mask, ff_grid)

      # Saving grib with gridded accumulated flash flood reports
      MainDirOUT = Git_Repo + "/" + DirOUT + "/" + TheDateTime_Final.strftime("%Y") + "/" + TheDateTime_Final.strftime("%Y%m%d") 
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      FileOUT = MainDirOUT + "/Grid_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d%H") + ".grib"
      mv.write(FileOUT, ff_grid)
      
      TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)