import os
import sys
from datetime import datetime, timedelta
import numpy as np
import metview as mv

#############################################################################################################
# CODE DESCRIPTION
# 25_Compute_PDT_Year.py computes the training dataset (Point Data Table) for a specific year.
# Runtime: the code takes up to 5 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year (integer, in YYYY format): year to consider.
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Git_Repo (string): repository's local path
# FileIN_Mask (string): relative path of the file containing the domain's mask.
# FileIN_StdOrog (string): relative path of the file containing the standard deviation of the sub-grid orography.
# DirIN_ClassRP (string): relative path of the directory containing the return period class for the extreme ERA5-ecPoint rainfall analysis.
# DirIN_RatioEM (string): relative path of the directory containing the ratio between extreme and mean ERA5-ecPoint rainfall analysis.
# DirIN_PercSS (string): relative path of the directory containing the percentage of soil saturation.
# DirIN_LAI (string): relative path of the directory containing the leaf area index.
# DirIN_PD (string): relative path of the directory containing the regridded population density.
# DirIN_FF (string): relative path of the directory containing the accumulated gridded flash flood reports.
# DirOUT (string): relative path containing the point data table for the considered year. 

# INPUT PARAMETERS
Year = int(sys.argv[1])
Acc = 12
Disc_Acc = 12
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
FileIN_StdOrog = "Data/Raw/Analysis/ERA5/sdor/sdor.grib"
DirIN_ClassRP = "Data/Compute/07_ClassRP_AccTP"
DirIN_RatioEM = "Data/Compute/09_Ratio_Extreme_Mean_AccTP"
DirIN_PercSS = "Data/Compute/11_Percentage_Soil_Saturation"
DirIN_LAI = "Data/Raw/Analysis/ERA5/lai"
DirIN_PD = "Data/Compute/14_PopDens_Regrid/N320"
DirIN_FF = "Data/Compute/19_Grid_AccRepFF"
DirOUT = "Data/Compute/25_PDT_Year"
#############################################################################################################

print()
print("Computing the training dataset (Point Data Table) for: " + str(Year))

# Defining the accumulation periods to consider
TheDateTime_S = datetime(Year, 1, 1, 0)
TheDateTime_F = datetime(Year, 12, 31, 24-Disc_Acc)

# Reading the domain's mask
mask = mv.values(mv.read(Git_Repo + "/" + FileIN_Mask))
ind_mask = np.where(mask ==1)[0]

# Reading the stdor values within the considered domain
stdor = mv.values(mv.read(Git_Repo + "/" + FileIN_StdOrog))[ind_mask].reshape(-1, 1)

# Reading the predictor values that change over different accumulation periods
print("Considering the " + str(Acc) + "-h accumulation period ending:")

pdt = np.array([]) # initialize the variable that will contain the pdt

TheDateTime_Start_S = datetime(Year, 1, 1, 0)
TheDateTime_Start_F = datetime(Year, 12, 31, 24-Disc_Acc)
TheDateTime_Start = TheDateTime_Start_S
while TheDateTime_Start <= TheDateTime_Start_F:

      TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)
      TheDateTime_PercSS = TheDateTime_Start - timedelta(days=1) # selecting the soil saturation percentage for 1 day prior the considered accumulation period (to not correlate it with the rainfall)
      print(" - on " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC")

      # Defining the predictor's paths 
      if TheDateTime_Final >= datetime(2000,1,1,0) and TheDateTime_Final < datetime(2005,1,1,0):
            YearPD = 2000
      elif TheDateTime_Final >= datetime(2005,1,1,0) and TheDateTime_Final < datetime(2010,1,1,0):
            YearPD = 2005
      elif TheDateTime_Final >= datetime(2010,1,1,0) and TheDateTime_Final < datetime(2015,1,1,0):
            YearPD = 2010   
      elif TheDateTime_Final >= datetime(2015,1,1,0) and TheDateTime_Final < datetime(2020,1,1,0):
            YearPD = 2015
      elif TheDateTime_Final >= datetime(2020,1,1,0) and TheDateTime_Final < datetime(2025,1,1,0):
            YearPD = 2020
      else:
            print("ERROR! " + TheDateTime_Final.strftime("%Y-%m-%d") + " is out of the range of valid years (2000 to 2025) for the population density!")
            exit()
      File_ClassRP = Git_Repo + "/" + DirIN_ClassRP + "/" + TheDateTime_Final.strftime("%Y%m") + "/ClassRP_" + f"{Acc:02}" + "h_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      File_RatioEM = Git_Repo + "/" + DirIN_RatioEM + "/" + TheDateTime_Final.strftime("%Y%m") + "/Ratio_" + f"{Acc:02}" + "h_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      File_PercSS = Git_Repo + "/" + DirIN_PercSS + "/" + TheDateTime_PercSS.strftime("%Y") + "/" + TheDateTime_PercSS.strftime("%Y%m%d") + "/soil_saturation_perc_" + TheDateTime_PercSS.strftime("%Y%m%d%H") + ".grib"
      File_LAI = Git_Repo + "/" + DirIN_LAI  + "/lai_" + TheDateTime_Final.strftime("%m%d") + ".grib"
      File_PD = Git_Repo + "/" + DirIN_PD + "/PopDens_" + str(YearPD) + ".grib2"
      File_FF = Git_Repo + "/" + DirIN_FF + "/" + TheDateTime_Final.strftime("%Y") + "/" + TheDateTime_Final.strftime("%Y%m%d") + "/Grid_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d%H") + ".grib"

      if os.path.exists(File_ClassRP) and os.path.exists(File_RatioEM) and os.path.exists(File_PercSS) and os.path.exists(File_PD) and os.path.exists(File_FF):

            # Reading the return period class values within the considered domain
            ClassRP = mv.values(mv.read(File_ClassRP))[ind_mask].reshape(-1, 1)
            
            # Reading the ratios between extreme and mean rainfall within the considered domain
            RatioEM = mv.values(mv.read(File_RatioEM))[ind_mask].reshape(-1, 1)
            
            # Reading the percentage of soil saturation within the considered domain
            PercSS = mv.values(mv.read(File_PercSS))[ind_mask].reshape(-1, 1)
            
            # Reading the leaf area index values within the considered domain
            lai = mv.values(mv.read(File_LAI))[ind_mask].reshape(-1, 1)

            # Reading the population density values within the considered domain
            pd = mv.values(mv.read(File_PD))[ind_mask].reshape(-1, 1)
            
            # Reading the accumulated gridded flash flood reports within the considered domain
            ff = mv.values(mv.read(File_FF))[ind_mask].reshape(-1, 1)
            
            # Building the point data table
            pdt_temp = np.concatenate((ff, stdor, ClassRP, RatioEM, PercSS, lai, pd), axis=1)
            if len(pdt) == 0:
                  pdt = pdt_temp
            else:
                  pdt = np.vstack((pdt,pdt_temp))
                        
      TheDateTime_Start = TheDateTime_Start + timedelta(hours = Disc_Acc)

# Saving the final point data table
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
      os.makedirs(MainDirOUT)
np.save(MainDirOUT + "/pdt_" + str(Year), pdt)