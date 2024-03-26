import os
from datetime import datetime, timedelta
import metview as mv

##########################################################################
# CODE DESCRIPTION
# Retrieve_Analysis_ERA5_lai.py retrieves from MARS the raw datasets needed to compute 
# the leaf area index. The fields change every day, but they are the same every year.
# Runtime: the code takes up to 10 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Git_Repo (string): repository's local path.
# DirOUT (string): relative path containing the computed leaf area index.

# INPUT PARAMETERS
Git_Repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirOUT="Data/Raw/Analysis/ERA5/lai"
##########################################################################

# Setting output directory
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
    os.makedirs(MainDirOUT)


# Computing the "overall" lai values (including low and high vegetation)
print()
print("Computing the lai values for:")
DateS = datetime(1940,1,1)
DateF = datetime(1940,12,31)
TheDate = DateS
while TheDate <= DateF:

      print(" - " + TheDate.strftime("%m-%d"))

      # Retrieving from Mars the cover and lai for low and high vegetation
      lai_lv = mv.retrieve(
            class_ = "ea",
            date = TheDate.strftime("%Y-%m-%d"),
            expver = 1,
            levtype = "sfc",
            param = "66.128",
            stream = "oper",
            time = "00:00:00",
            type = "an"
            )

      lai_hv = mv.retrieve(
            class_ = "ea",
            date = TheDate.strftime("%Y-%m-%d"),
            expver = 1,
            levtype = "sfc",
            param = "67.128",
            stream = "oper",
            time = "00:00:00",
            type = "an"
            )

      cvl = mv.retrieve(
            class_ = "ea",
            date = TheDate.strftime("%Y-%m-%d"),
            expver = 1,
            levtype = "sfc",
            param = "27.128",
            stream = "oper",
            time = "00:00:00",
            type = "an"
            )

      cvh = mv.retrieve(
            class_ = "ea",
            date = TheDate.strftime("%Y-%m-%d"),
            expver = 1,
            levtype = "sfc",
            param = "28.128",
            stream = "oper",
            time = "00:00:00",
            type = "an"
            )
      
      # Computing the "overall" lai values
      lai = lai_lv * cvl + lai_hv * cvh

      # Saving the "overall" lai values
      FileOUT = MainDirOUT + "/lai_" + TheDate.strftime("%m%d") + ".grib"
      mv.write(FileOUT, lai)

      TheDate = TheDate + timedelta(days=1)