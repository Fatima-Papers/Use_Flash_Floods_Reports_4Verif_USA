import os
import shutil
import numpy as np

#############################################################################################################################################
# CODE DESCRIPTION
# Retrieve_Analysis_ERA5_ecPoint_tp_climate.sh retrieves from disk the 12-hourly rainfall climatology computed from ERA5-ecPoint.  
# The rainfall climatology was computed using the code in the following GitHub repository:
# https://github.com/FatimaPillosu/RainThr_4FlashFloodFC_ecPointERA5
# The grib file was retrieved from:
# /ec/vol/ecpoint_dev/mofp/Papers_2_Write/RainThr_4FlashFloodFC_ecPointERA5/Data/Compute/03_ClimateG_12h/ERA5_ecPoint/Climate_ERA5_ecPoint_12h.grib
# The computed percentiles have been extracted from the file:
# /ec/vol/ecpoint_dev/mofp/Papers_2_Write/RainThr_4FlashFloodFC_ecPointERA5/Scripts/Processed/02_Compute_ClimateSA.py
# Runtime: the code takes up to few seconds to run in series.

# INPUT PARAMETERS DESCRIPTION
# Git_Repo (string): repository's local path.
# FileIN (string): full path of the file containing the rainfall climatology to retrieve.
# DirOUT (string): relative path of the directory containing the rainfall climatology and the computed percentiles.

# INPUT PARAMETERS
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/RainThr_4FlashFloodFC_ecPointERA5/Data/Compute/03_ClimateG_12h/ERA5_ecPoint/Climate_ERA5_ecPoint_12h.grib"
DirOUT="Data/Raw/Analysis/ERA5_ecPoint/tp_climate"
#############################################################################################################################################

# Setting output directory
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
    os.makedirs(MainDirOUT)

# Copying rainfall climatology
FileOUT_climate = MainDirOUT + "/tp_climate_12h_ERA5_ecPoint.grib"
shutil.copyfile(FileIN, FileOUT_climate)
    
# Creating and saving the array with the percentiles computed
percs = np.append(np.arange(1,100), np.array([99.8, 99.9, 99.95, 99.98, 99.99, 99.995, 99.998]))
FileOUT_percs = MainDirOUT + "/percs.npy"
np.save(FileOUT_percs, percs)