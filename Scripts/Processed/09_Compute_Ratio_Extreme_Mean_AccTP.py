import os
import sys
from datetime import datetime, timedelta
import metview as mv

#######################################################################################################
# CODE DESCRIPTION
# 09_Compute_Ratio_Extreme_Mean_AccTP.py computes the ratio between the extreme and the mean ERA5-ecPoint rainfall 
# reanalysis in each grid-box. 
# Runtime: the code takes up to 60 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year (integer, in YYYY format): year to consider.
# Acc (integer, in hours): accumulation period.
# Git_Repo (string): repository's local path.
# DirIN (string): relative path of the directory containing the ERA5-ecPoint rainfall reanalysis.
# DirOUT (string): relative path of the directory containing the ratios between the extreme and the mean ERA5-ecPoint rainfall.

# INPUT PARAMETERS
Year = int(sys.argv[1])
Acc = 12
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Raw/Analysis/ERA5_ecPoint/tp"
DirOUT = "Data/Compute/09_Ratio_Extreme_Mean_AccTP"
#######################################################################################################

# Computing the ratio between the extreme and the mean point-rainfall ERA5-ecPoint reanalysis in each grid-box. 
print()
print("Computing the ratio between extreme and mean " + str() + "-hourly ERA5-ecPoint rainfall, ending:")

# Defining the period to consider
TheDate_S = datetime(Year,1,1)
TheDate_F = datetime(Year,12,31)

TheDate = TheDate_S
while TheDate <= TheDate_F:

      for EndPeriod in range(0+Acc, 24+1, Acc):

            TheDateTime_Final = TheDate + timedelta(hours=EndPeriod)
            print(" - on " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC")

            # Reading the ERA5-ecPoint rainfall reanalysis
            tp = mv.read(Git_Repo + "/" + DirIN + "/Pt_BC_PERC/" + TheDate.strftime("%Y%m") + "/Pt_BC_PERC_" + TheDate.strftime("%Y%m%d") + "_" + str(EndPeriod) + ".grib2")
            
            # Selecting the field containing the extreme rainfall and computing the field containing the average of all the point rainfall values
            tp_extreme = tp[-1] # extreme
            tp_mean = mv.sum(tp) / mv.count(tp) # mean

            # Computing the ratios
            ratio = tp_extreme / tp_mean
            
            # Saving the ratios
            DirOUT_temp = Git_Repo + "/" + DirOUT + "/" + TheDateTime_Final.strftime("%Y%m")
            if not os.path.exists(DirOUT_temp):
                  os.makedirs(DirOUT_temp)
            FileOUT = DirOUT_temp + "/Ratio_" + f"{Acc:02}" + "h_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
            mv.write(FileOUT, ratio)

      TheDate = TheDate + timedelta(days=1)