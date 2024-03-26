import os
import sys
from datetime import datetime, timedelta
import pandas as pd
import metview as mv

##########################################################################
# CODE DESCRIPTION
# 16_Compute_Gridded_AccRepFF.py creates the gridded accumulated flash flood reports 
# based on the point accumulated ones.
# Runtime: the code takes up to 3 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year (year, in YYYY format): year to consider.
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Git_Repo (string): repository's local path
# FileIN_Mask (string): relative path where the USA's mask is stored.
# DirIN (string): relative path of the file containing the flash flood reports.
# DirOUT (string): relative path where to store the plot 

# INPUT PARAMETERS
Year = int(sys.argv[1])
Acc = 12
Disc_Acc = 12
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
DirIN = "Data/Compute/14_Point_AccRepFF"
DirOUT = "Data/Compute/16_Gridded_AccRepFF"
##########################################################################

# Reading the mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)

# Creating gridded accumulated flash flood reports
print("Creating gridded accumulated flash flood reports")
DateTime_Start_S = datetime(Year,1,1,0)
DateTime_Start_F = datetime(Year,12,31,12)

DateTime_Start = DateTime_Start_S
while DateTime_Start <= DateTime_Start_F:

      DateTime_Final = DateTime_Start + timedelta(hours=Acc)

      print(" - Post-processing date-time: " + DateTime_Start.strftime("%Y%m%d%H"))
      
      # Initializing the gridded field where to store the flash flood reports
      ff_grid = mv.values((mask == 1) * 0)

      # Reading the point accumulated flash flood reports
      FileIN = Git_Repo + "/" + DirIN + "/" + DateTime_Start.strftime("%Y") + "/" + DateTime_Start.strftime("%Y%m%d") + "/FlashFloodRep_" + DateTime_Start.strftime("%Y%m%d%H") + ".csv"
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
      MainDirOUT = Git_Repo + "/" + DirOUT + "/" + DateTime_Start.strftime("%Y") + "/" + DateTime_Start.strftime("%Y%m%d") 
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      FileOUT = MainDirOUT + "/FlashFloodRep_" + DateTime_Start.strftime("%Y%m%d%H") + ".grib"
      mv.write(FileOUT, ff_grid)
      
      DateTime_Start = DateTime_Start + timedelta(hours=Disc_Acc)