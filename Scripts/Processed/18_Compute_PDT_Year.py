import os
import sys
from datetime import datetime, timedelta
import numpy as np
import metview as mv

###########################################################################
# CODE DESCRIPTION
# 09_Compute_PDT_Year.py computes the point data table for a specific year.
# Runtime: the code takes up to 30 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year (integer, in YYYY format): year to consider.
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Git_Repo (string): repository's local path
# FileIN_Mask (string): relative path of the mask for which to extract the population density.
# DirIN (string): relative path containing the raw GHS_POP population density.
# DirOUT (string): relative path containing the extracted GHS_POP population density.

# INPUT PARAMETERS
Year = int(sys.argv[1])
Acc = 12
Disc_Acc = 12
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
FileIN_slor = "Data/Raw/Analysis/ENS_9km/slor/slor.grib"
FileIN_stdor = "Data/Raw/Analysis/ENS_9km/sdor/sdor.grib"
DirIN_RainThr = "Data/Raw/Analysis/ERA5_ecPoint/tp_climate"
DirIN_FF = "Data/Compute/03b_Gridded_Accumulated_RepFF"
DirIN_SS = "Data/Compute/05_Percentage_Soil_Saturation"
DirIN_Rain = "Data/Raw/Analysis/ERA5_ecPoint/tp"
DirOUT = "Data/Compute/09_PDT_Year"
###########################################################################

# Reading mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask_lats = mv.latitudes(mask)
mask_lons = mv.longitudes(mask)
mask_vals = mv.values(mask)
mask_index = np.where(mask_vals == 1)[0]
mask_lats = mask_lats[mask_index]
mask_lons = mask_lons[mask_index]
mask_vals = mask_vals[mask_index]

# Reading slor and extracting the nearest values to the mask grid-points 
slor = mv.read(Git_Repo + "/" + FileIN_slor)
slor_mask = mv.nearest_gridpoint(slor, mask_lats, mask_lons).reshape(-1, 1)

# Reading sdor and extracting the nearest values to the mask grid-points 
stdor = mv.read(Git_Repo + "/" + FileIN_stdor)
stdor_mask = mv.nearest_gridpoint(stdor, mask_lats, mask_lons).reshape(-1, 1)

# Reading the rainfall thresholds and extracting the values for the mask grid-points
tp_climate = mv.read(Git_Repo + "/" + DirIN_RainThr + "/tp_climate_12h_ERA5_ecPoint.grib")
percs = np.load(Git_Repo + "/" + DirIN_RainThr + "/percs_computed_4_tp_climate.npy")
rain_thr_mask_all = []
for perc in [99.8, 99.9, 99.95, 99.98, 99.99]:
      perc_index = np.where(percs == perc)[0]
      rain_thr = mv.values(tp_climate[perc_index])
      rain_thr_mask = rain_thr[mask_index]
      rain_thr_mask_all.append(rain_thr_mask)
rain_thr_mask_all = np.array(rain_thr_mask_all).T

# Building the point data table
DateTime_Start_S = datetime(Year,1,1,0)
DateTime_Start_F = datetime(Year,12,31,0)
pdt = np.array([])

DateTime_Start = DateTime_Start_S
while DateTime_Start <= DateTime_Start_F:

      DateTime_Final = DateTime_Start + timedelta(hours=Acc)
      print("Creating point data table for: " + DateTime_Final.strftime("%Y%m%d%H"))

      # Reading the variables that change with the dates
      FileIN_FF = Git_Repo + "/" + DirIN_FF + "/" + DateTime_Final.strftime("%Y") + "/" + DateTime_Final.strftime("%Y%m%d") + "/FlashFloodRep_" + DateTime_Final.strftime("%Y%m%d%H") + ".grib"
      FileIN_SS = Git_Repo + "/" + DirIN_SS + "/" + DateTime_Final.strftime("%Y") + "/" + DateTime_Final.strftime("%Y%m%d") + "/soil_saturation_perc_" + DateTime_Final.strftime("%Y%m%d%H") + ".grib"
      FileIN_Rain = Git_Repo + "/" + DirIN_Rain + "/Pt_BC_PERC/" + DateTime_Final.strftime("%Y%m") + "/Pt_BC_PERC_" + DateTime_Final.strftime("%Y%m%d") + "_" + DateTime_Final.strftime("%H") + ".grib2"

      # Building the point data table for the considered date
      if os.path.exists(FileIN_FF) and os.path.exists(FileIN_SS) and os.path.exists(FileIN_Rain):
            
            ss = mv.read(FileIN_SS)
            ss_mask = mv.nearest_gridpoint(ss, mask_lats, mask_lons).reshape(-1, 1)

            ff = mv.values(mv.read(FileIN_FF))
            ff_mask = ff[mask_index].reshape(-1, 1)

            tp = mv.values(mv.read(FileIN_Rain))
            tp_mask = tp[:,mask_index].T

            pdt_temp = np.concatenate((ff_mask, slor_mask, stdor_mask, ss_mask, rain_thr_mask_all, tp_mask), axis=1)
           
            # Building the point data table for all the dates
            if DateTime_Start == DateTime_Start_S:
                  pdt = pdt_temp
            else:
                  pdt = np.vstack((pdt,pdt_temp))

      DateTime_Start = DateTime_Start + timedelta(hours=Disc_Acc)

# Removing any nan in in the dataset
ind_no_nan = np.where(~np.isnan(pdt[:,3]))[0]
pdt = pdt[ind_no_nan,:]

# Saving the final point data table
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
      os.makedirs(MainDirOUT)
np.save(MainDirOUT + "/pdt_" + str(Year), pdt)