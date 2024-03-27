import os
import sys
from datetime import datetime, timedelta
import numpy as np
import metview as mv

#######################################################################################
# CODE DESCRIPTION
# 07_Compute_ClassRP_AccTP.py computes the return period class for the 99th percentile of accumulated 
# rainfall from ERA5-ecPoint.
# Runtime: the code takes up to 90 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year (integer, in YYYY format): year to consider.
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Perc (float, from 0 to 100): percentile to consider for the rainfall analysis.
# YearRP_list (list of integers): list of the considered rainfall thresholds expressed as return period in years.
# Perc_Climate_list (list of floats): list of percentiles corresponding to the considered return periods.
# Git_Repo (string): repository's local path.
# DirIN_Climate (string): relative path of the directory containing the rainfall thresholds.
# DirIN_Analaysis (string): relative path of the directory containing the ERA5-ecPoint rainfall analaysis.
# DirOUT (string): relative path of the directory containing the class for the 99th percentile.

# INPUT PARAMETERS
Year = int(sys.argv[1])
Acc = 12
Disc_Acc = 12
Perc = 99
YearRP_list = [1, 2, 5, 10, 20]
Perc_Climate_list = [99.9, 99.95, 99.98, 99.99, 99.995]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN_Climate = "Data/Raw/Analysis/ERA5_ecPoint/tp_climate"
DirIN_Analaysis = "Data/Raw/Analysis/ERA5_ecPoint/tp"
DirOUT = "Data/Compute/07_ClassRP_AccTP"
#######################################################################################


# Reading the rainfall climatology
print()
print("Reading the climatology of " + str() + "-hourly rainfall")
climate_tp = mv.read(Git_Repo + "/" + DirIN_Climate + "/tp_climate_" + f"{Acc:02}" + "h_ERA5_ecPoint.grib")
climate_percs = np.load(Git_Repo + "/" + DirIN_Climate + "/percs.npy")


# Computing the return period class for the 99th percentile of accumulated rainfall from ERA5-ecPoint.
print()
print("Computing the return period class for the 99th percentile of  " + str() + "-hourly rainfall from ERA5-ecPoint, ending:")

Date_S = datetime(Year,1,1,0)
Date_F = datetime(Year,12,31,0)

TheDate = Date_S
while TheDate <= Date_F:

      for EndPeriod in range(0+Acc, 24+1, Acc):

            TheDateTime_Final = TheDate + timedelta(hours=EndPeriod)
            print(" - on " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC")

            # Reading the rainfall analysis
            tp = mv.read(Git_Repo + "/" + DirIN_Analaysis + "/Pt_BC_PERC/" + TheDate.strftime("%Y%m") + "/Pt_BC_PERC_" + TheDate.strftime("%Y%m%d") + "_" + str(EndPeriod) + ".grib2")
            tp_perc = mv.values(tp[Perc-1])

            # Determining the return period classes
            classRP = np.zeros(len(tp_perc)) # initializing the variable that will contain the RP classes
            for ind_RP in range(len(YearRP_list)):
                  
                  if ind_RP < len(YearRP_list)-1:
                        YearRP = YearRP_list[ind_RP] 
                        Perc_Climate_l = Perc_Climate_list[ind_RP] 
                        Perc_Climate_h = Perc_Climate_list[ind_RP+1] 
                        ind_perc_l = np.where(climate_percs == Perc_Climate_l)[0][0] 
                        ind_perc_h = np.where(climate_percs == Perc_Climate_h)[0][0] 
                        climate_perc_l = mv.values(climate_tp[ind_perc_l])
                        climate_perc_h = mv.values(climate_tp[ind_perc_h])
                        classRP = classRP + ( ((tp_perc >= climate_perc_l) & (tp_perc < climate_perc_h)) * YearRP )
                  elif ind_RP == len(YearRP_list)-1:
                        YearRP = YearRP_list[ind_RP] 
                        Perc_Climate = Perc_Climate_list[ind_RP] 
                        ind_perc = np.where(climate_percs == Perc_Climate)[0][0] 
                        climate_perc = mv.values(climate_tp[ind_perc])
                        classRP = classRP + ( (tp_perc >= climate_perc ) * YearRP )
            classRP = mv.set_values(tp[0], classRP)

            # Saving the return period classes
            DirOUT_temp = Git_Repo + "/" + DirOUT + "/" + TheDateTime_Final.strftime("%Y%m")
            if not os.path.exists(DirOUT_temp):
                  os.makedirs(DirOUT_temp)
            FileOUT = DirOUT_temp + "/ClassRP_" + str(Acc) + "h_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
            mv.write(FileOUT, classRP)

      TheDate = TheDate + timedelta(days=1)