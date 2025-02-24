#!/bin/bash

##########################################################################
# CODE DESCRIPTION
# Retrieve_Analysis_ERA5_ecPoint_tp.sh retrieves from disk the 12-hourly rainfall from 
# ERA5-ecPoint.  
# Runtime: the code can take up to 12 hours to run in series.

# INPUT PARAMETERS DESCRIPTION
# YearS (date, in YYYY format): start year to retrieve.
# YearF (date, in YYYY format): final year to retrieve.
# Acc (integer, in hours): forecast accumulation period.                            
# Git_Repo (string): repository's local path.
# DirIN (string): full path containing the forecasts to retrieve.
# DirOUT (string): relative path containing the retrieved forecasts.

# INPUT PARAMETERS
YearS=2023
YearF=2023
Acc=12
ExpVer="0005"
Code_Cal_Ver="Code2.0.0_Cal1.0.0"
Git_Repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN="/ec/vol/ecpoint/mofp/forecasts/SemiOper/ECMWF_ERA5"
DirOUT="Data/Raw/Analysis/ERA5_ecPoint/tp"
##########################################################################

# Setting general variables
AccSTR=$(printf %03d ${Acc})

# Setting output directory
DirOUT_temp=${Git_Repo}/${DirOUT}
mkdir -p ${DirOUT_temp}/Pt_BC_PERC
mkdir -p ${DirOUT_temp}/Grid_BC_VALS

# Retrieving the ERA5_ecPoint data
for Year in $(seq ${YearS} ${YearF}); do
    echo "Retrieving ERA5_ecPoint for ${Year}"
    cp -r ${DirIN}/${ExpVer}/Rainfall/${AccSTR}/${Code_Cal_Ver}/Pt_BC_PERC/${Year}* ${DirOUT_temp}/Pt_BC_PERC
    cp -r ${DirIN}/${ExpVer}/Rainfall/${AccSTR}/${Code_Cal_Ver}/Grid_BC_VALS/${Year}* ${DirOUT_temp}/Grid_BC_VALS
done