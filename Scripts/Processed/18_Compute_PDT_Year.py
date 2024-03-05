import os
import sys
from datetime import datetime, timedelta
import numpy as np
import metview as mv

##############################################################################
# CODE DESCRIPTION
# 18_Compute_PDT_Year.py computes the training datasrt (Point Data Table) for a specific year.
# Runtime: the code takes up to 90 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year (integer, in YYYY format): year to consider.
# Acc (integer, in hours): accumulation period.
# Git_Repo (string): repository's local path
# FileIN_Mask (string): relative path where the USA's mask is stored.
# FileIN_slor (string): relative path of the file containing the slope of the sub-grid orography.
# FileIN_stdor (string): relative path of the file containing the standard deviation of the sub-grid orography.
# DirIN_RainThr (string): relative path of the directory containing the rainfall thresholds.
# DirIN_Rain (string): relative path of the directory containing the ecPoint-ERA5 rainfal reanalysis.
# DirIN_SS (string): relative path of the directory containing the percentage of the soil moisture.
# DirIN_PD (string): relative path of the directory containing the population density.
# DirIN_FF (string): relative path of the directory containing the accumulated gridded flood reports.
# DirOUT (string): relative path containing the point data table.

# INPUT PARAMETERS
Year = int(sys.argv[1])
Acc = 12
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
FileIN_slor = "Data/Raw/Analysis/ENS_9km/slor/slor.grib"
FileIN_stdor = "Data/Raw/Analysis/ENS_9km/sdor/sdor.grib"
DirIN_RainThr = "Data/Raw/Analysis/ERA5_ecPoint/tp_climate"
DirIN_Rain = "Data/Raw/Analysis/ERA5_ecPoint/tp"
DirIN_SS = "Data/Compute/07_Percentage_Soil_Saturation"
DirIN_PD = "Data/Compute/10_PopDens_Regrid"
DirIN_FF = "Data/Compute/16_Gridded_AccRepFF"
DirOUT = "Data/Compute/18_PDT_Year"
##############################################################################

# Reading mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask_lats = mv.latitudes(mask)
mask_lons = mv.longitudes(mask)
mask_vals = mv.values(mask)
mask_index = np.where(mask_vals == 1)[0]
mask_lats = mask_lats[mask_index]
mask_lons = mask_lons[mask_index]

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

# Reading the variables that change with the dates
Date_S = datetime(Year,1,1,0)
Date_F = datetime(Year,12,31,0)
pdt = np.array([])

TheDate = Date_S
while TheDate <= Date_F:

      for EndPeriod in range(0+Acc, 24+1, Acc):

            DateTime_Final = TheDate + timedelta(hours=EndPeriod)
            print(TheDate, EndPeriod)
            print("Creating point data table for: " + DateTime_Final.strftime("%Y%m%d%H"))

            # Reading population density and extracting the nearest values to the mask grid-points 
            if DateTime_Final < datetime(2005,1,1,0):
                  YearPD = 2000
            elif DateTime_Final >= datetime(2005,1,1,0) and DateTime_Final < datetime(2010,1,1,0):
                  YearPD = 2005
            elif DateTime_Final >= datetime(2010,1,1,0) and DateTime_Final < datetime(2015,1,1,0):
                  YearPD = 2010   
            elif DateTime_Final >= datetime(2015,1,1,0) and DateTime_Final < datetime(2020,1,1,0):
                  YearPD = 2015
            else:
                  YearPD = 2020
            pd = mv.read(Git_Repo + "/" + DirIN_PD + "/" + str(YearPD) + "/PopDens_N320_" + str(YearPD) + ".grib2")
            pd_mask = mv.nearest_gridpoint(pd, mask_lats, mask_lons).reshape(-1, 1)

            # Reading the flash flood reports, rainfall and soil moisture, and extracting the nearest values to the mask grid-points 
            FileIN_FF = Git_Repo + "/" + DirIN_FF + "/" + DateTime_Final.strftime("%Y") + "/" + DateTime_Final.strftime("%Y%m%d") + "/FlashFloodRep_" + DateTime_Final.strftime("%Y%m%d%H") + ".grib"
            FileIN_Rain = Git_Repo + "/" + DirIN_Rain + "/" + TheDate.strftime("%Y%m") + "/Pt_BC_PERC_" + TheDate.strftime("%Y%m%d") + "_" + str(EndPeriod) + ".grib2"
            
            DateTime_ss = DateTime_Final - timedelta(hours=Acc) - timedelta(days=1) # selecting the soil saturation percentage for an antecedent period of time compared to when the rainfall fell (i.e., 24 hours)
            FileIN_SS = Git_Repo + "/" + DirIN_SS + "/" + DateTime_ss.strftime("%Y") + "/" + DateTime_ss.strftime("%Y%m%d") + "/soil_saturation_perc_" + DateTime_ss.strftime("%Y%m%d%H") + ".grib"

            # Building the point data table for the considered date
            if os.path.exists(FileIN_FF) and os.path.exists(FileIN_SS) and os.path.exists(FileIN_Rain):
                  
                  ss = mv.read(FileIN_SS)
                  ss_mask = mv.nearest_gridpoint(ss, mask_lats, mask_lons).reshape(-1, 1)

                  ff = mv.values(mv.read(FileIN_FF))
                  ff_mask = ff[mask_index].reshape(-1, 1)

                  tp = mv.values(mv.read(FileIN_Rain))
                  tp_mask = tp[:,mask_index].T

                  # Building the point data table
                  pdt_temp = np.concatenate((ff_mask, slor_mask, stdor_mask, pd_mask, ss_mask, rain_thr_mask_all, tp_mask), axis=1)

                  # Building the point data table for all the dates
                  if len(pdt) == 0:
                        pdt = pdt_temp
                  else:
                        pdt = np.vstack((pdt,pdt_temp))
                        
      TheDate = TheDate + timedelta(days=1)

# Saving the final point data table
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
      os.makedirs(MainDirOUT)
np.save(MainDirOUT + "/pdt_" + str(Year), pdt)