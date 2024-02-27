import os
from datetime import datetime, timedelta
import pandas as pd
import metview as mv

##############################################################################################################################################
# CODE DESCRIPTION
# 09_Compute_Gridded_Accumulated_RepFF.py creates the gridded accumulated flash flood reports based on the point accumulated ones.
# Runtime: the code takes up to 60 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# DateTime_Start_S (date and time): start date (first three numbers) and time (fourth number) for the analysis period (representing the beginning of the accumulation period).
# DateTime_Start_F (date and time): final date (first three numbers) and time (fourth number) for the analysis period (representing the beginning of the accumulation period).
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Git_Repo (string): repository's local path
# FileIN (string): relative path of the file containing the flash flood reports.
# DirOUT (string): relative path where to store the plot 

# INPUT PARAMETERS
DateTime_Start_S = datetime(1996,10,20,0)
DateTime_Start_F = datetime(2023,12,31,12)
Acc = 12
Disc_Acc = 12
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
DirIN = "Data/Compute/07_Point_Accumulated_RepFF"
DirOUT = "Data/Compute/09_Gridded_Accumulated_RepFF"
##############################################################################################################################################

# Reading the mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)

# Creating gridded accumulated flash flood reports
print("Creating gridded accumulated flash flood reports")
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