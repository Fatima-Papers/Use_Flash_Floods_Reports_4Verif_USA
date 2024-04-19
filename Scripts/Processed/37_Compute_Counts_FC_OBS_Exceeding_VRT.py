import os
import sys
from datetime import datetime, timedelta
import numpy as np
import metview as mv 

###############################################################################################
# CODE DESCRIPTION
# 37_Compute_Counts_FC_OBS_Exceeding_VRT.py computes the counts of ensemble members exceeding the 
# considered VRT. It also computes the number of flash flood events from true and pseudo (for different probability thresholds) reports.
# Note: the code can take up 2 days to run in serial. It is suggested to parallelize the computations for each step to 
# take the runtime down to 2 hours.

# INPUT PARAMETERS DESCRIPTION
# Year (integer, in format YYYY): year to consider in the processing.
# StepF (integer, in hours): final step of the accumulation periods to consider.
# Acc (number, in hours): rainfall accumulation to consider.
# Perc_VRT (integer, from 0 to 100): percentile that defines the verifying rainfall event to consider.
# SystemFC (string): name of the forecasting systems to consider.
# Git_Repo (string): repository's local path.
# FileIN_Mask (string): relative path of the file containing the domain's mask.
# DirIN_Climate_TP (string): relative path of the directory containing the rainfall climatology.
# DirIN_FC (string): relative path of the directory containing the rainfall forecasts.
# DirIN_Grid_AccRepFF (string): relative path of the directory containing the accumulated gridded flash flood reports.
# DirOUT (string): relative path of the directory containing the counts.

# NOTES ON THE VALUES FOR "Perc_VRT"
# The percentiles correspond roughly to the following return periods:
# 99.9th -> once in 1 years
# 99.95th -> once in 2 years
# 99.98th -> once in 5 years
# 99.99th -> once in 10 years
# 99.995th -> once in 20 years

# INPUT PARAMETERS
Year = 2022
StepF = int(sys.argv[1])
Acc = 12
Perc_VRT = 99.995
Prob_Thr_list = [0.1, 1, 2, 3, 4, 5]
SystemFC = "ecPoint"
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ENS/Mask.grib"
DirIN_Climate_TP = "Data/Raw/Analysis/ERA5_ecPoint/tp_climate"
DirIN_FC = "Data/Raw/FC"
DirIN_True_Grid_AccRepFF = "Data/Compute/19_Grid_AccRepFF"
DirIN_Pseudo_Grid_AccRepFF = "Data/Compute/28_Prob_AccRepFF/AllFF_2005_2020/AllPred"
DirOUT = "Data/Compute/37_Counts_FC_OBS_Exceeding_VRT"
###############################################################################################


# Defining  the range of forecasts' base dates to consider
BaseDateS = datetime(Year, 1, 1)
BaseDateF = datetime(Year, 12, 31)

# Reading domain's mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask_index = np.where(mv.values(mask) == 1)[0]
mask_lats = mv.latitudes(mask)[mask_index]
mask_lons = mv.longitudes(mask)[mask_index]

# Reading the VRT values for the domain of interest
climate_perc = np.load(Git_Repo + "/" + DirIN_Climate_TP + "/percs.npy")
Perc_VRT_ind = np.where(climate_perc == Perc_VRT)[0][0]
vrt = mv.read(Git_Repo + "/" + DirIN_Climate_TP + "/tp_climate_" + f"{Acc:02d}" + "h_ERA5_ecPoint.grib")[Perc_VRT_ind]
vrt_gridFC = mv.nearest_gridpoint(vrt,mask_lats, mask_lons)

# Computing the counts of forecasts and observations exceeding a VRT
BaseDate = BaseDateS
while BaseDate <= BaseDateF:
      
      print(" ")
      print(" - Reading " + SystemFC + ", StepF=" + str(StepF) + ", FC date: " + BaseDate.strftime("%Y-%m-%d") + " at " + BaseDate.strftime("%H") + " UTC")

      # Reading the rainfall forecasts for the considered date
      tp = [] # variable needed to asses whether the forecasts for the considered date exist
      if SystemFC == "ENS":
            # Note: converting the forecasts in accumulated rainfall over the considered period. Converting also their units from m to mm.
            StepS = StepF - Acc
            FileIN_FC_1 = Git_Repo + "/" + DirIN_FC + "/" + SystemFC + "/" + BaseDate.strftime("%Y%m%d%H") + "/tp_" + BaseDate.strftime("%Y%m%d") + "_" + BaseDate.strftime("%H") + "_" + f"{StepS:03d}" + ".grib"
            FileIN_FC_2 = Git_Repo + "/" + DirIN_FC + "/" + SystemFC + "/" + BaseDate.strftime("%Y%m%d%H") + "/tp_" + BaseDate.strftime("%Y%m%d") + "_" + BaseDate.strftime("%H") + "_" + f"{StepF:03d}" + ".grib"
            if os.path.isfile(FileIN_FC_1) and os.path.isfile(FileIN_FC_2):
                  tp1 = mv.read(FileIN_FC_1)
                  tp2 = mv.read(FileIN_FC_2)
                  tp = mv.values((tp2 - tp1) * 1000)[mask_index]
      elif SystemFC == "ecPoint":
            # Note: the forecasts are already accumulated over the considered period, and are already expressed in mm. The forecasts are stored in files whose name indicates the end of the accumulated period.
            FileIN_FC = Git_Repo + "/" + DirIN_FC + "/" + SystemFC + "/" + BaseDate.strftime("%Y%m%d%H") + "/Pt_BiasCorr_RainPERC/Pt_BC_PERC_" + f"{Acc:03d}" + "_" + BaseDate.strftime("%Y%m%d") + "_" + BaseDate.strftime("%H") + "_" + f"{StepF:03d}" + ".grib"
            if os.path.isfile(FileIN_FC):
                  tp = mv.values(mv.read(FileIN_FC))[:,mask_index]

      # Checking that the rainfall forecasts exist for the considered date. If not, they are not added in the 3d-array
      if len(tp) != 0:

            ValidTimeF = BaseDate + timedelta(hours=StepF)

            # Reading the true accumulated gridded flash flood reports
            FileIN_True_Grid_AccRepFF = Git_Repo + "/" + DirIN_True_Grid_AccRepFF + "/" + ValidTimeF.strftime("%Y") + "/" + ValidTimeF.strftime("%Y%m%d") + "/Grid_AccRepFF_" + ValidTimeF.strftime("%Y%m%d%H") + ".grib"
            True_Grid_AccRepFF = mv.read(FileIN_True_Grid_AccRepFF)
            True_Grid_AccRepFF_gridFC = mv.nearest_gridpoint(True_Grid_AccRepFF, mask_lats, mask_lons)

            # Reading the pseudo accumulated gridded flash flood reports
            Pseudo_Grid_AccRepFF_gridFC = np.empty((len(mask_lats), len(Prob_Thr_list)))
            FileIN_Pseudo_Grid_AccRepFF = Git_Repo + "/" + DirIN_Pseudo_Grid_AccRepFF + "/Prob_AccRepFF_" + ValidTimeF.strftime("%Y%m%d") + "_" + ValidTimeF.strftime("%H") + ".grib"
            for ind in range(len(Prob_Thr_list)):
                  Prob_Thr = Prob_Thr_list[ind]
                  Pseudo_Grid_AccRepFF = (mv.read(FileIN_Pseudo_Grid_AccRepFF) >= Prob_Thr)
                  Pseudo_Grid_AccRepFF_gridFC[:,ind] = mv.nearest_gridpoint(Pseudo_Grid_AccRepFF, mask_lats, mask_lons)

            # Counting the number of observed flash flood events
            count_true_obs = np.sum(True_Grid_AccRepFF_gridFC > 0)
            count_pseudo_obs = np.sum(Pseudo_Grid_AccRepFF_gridFC > 0, axis=0)

            # Computing the counts of forecasts exceeding the considered VRT
            count_fc_exceed_VRT = np.sum(tp >= vrt_gridFC)

            # Saving the counts
            count_fc_obs_exceed_VRT = np.hstack([count_fc_exceed_VRT, count_true_obs, count_pseudo_obs])
            print(count_fc_obs_exceed_VRT)

            DirOUT_temp= Git_Repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h/PercVRT_" + str(Perc_VRT) + "/" + SystemFC + "/" + f"{StepF:03d}" 
            FileNameOUT_temp = "Count_FC_OBS_" + f"{Acc:02d}" + "h_PercVRT_" + str(Perc_VRT) + "_" + SystemFC + "_" + BaseDate.strftime("%Y%m%d") + "_" + BaseDate.strftime("%H") + "_" + f"{StepF:03d}"
            if not os.path.exists(DirOUT_temp):
                  os.makedirs(DirOUT_temp)
            np.save(DirOUT_temp + "/" + FileNameOUT_temp, count_fc_obs_exceed_VRT)

      else:

            print("   - NOTE: the requested forecast is not present in the database.")

      BaseDate += timedelta(days=1)