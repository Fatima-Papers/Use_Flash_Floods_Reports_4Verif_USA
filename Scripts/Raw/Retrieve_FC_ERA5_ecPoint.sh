#!/bin/bash

##########################################################################
# CODE DESCRIPTION
# Retrieve_FC_ERA5_ecPoint retrieves the ERA5-ecPoint data for 12-hourly rainfall.  
# Runtime: the code can take up to 31 hours to run in series.

# INPUT PARAMETERS DESCRIPTION
# YearS (date, in YYYY format): start year to retrieve.
# YearF (date, in YYYY format): final year to retrieve.
# Acc (integer, in hours): forecast accumulation period.                            
# Git_Repo (string): repository's local path.
# DirIN (string): full path containing the forecasts to retrieve.
# DirOUT (string): relative path containing the retrieved forecasts.

# INPUT PARAMETERS
YearS=1950
YearF=2020
Acc=12
Git_Repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN="/ec/vol/highlander/ERA5_ecPoint_70yr"
DirOUT="Data/Raw/FC/ERA_ecPoint"
##########################################################################

# Setting general variables
AccSTR=$(printf %02d ${Acc})

# Setting output directory
DirOUT_temp=${Git_Repo}/${DirOUT}
mkdir -p ${DirOUT_temp}/Pt_BC_PERC
mkdir -p ${DirOUT_temp}/WT

# Retrieving the ERA5_ecPoint data
for Year in $(seq ${YearS} ${YearF}); do
    echo "Retrieving ERA5_ecPoint for ${Year}"
    cp -r ${DirIN}/Rainfall_${AccSTR}h/Pt_BC_PERC/${Year}* ${DirOUT_temp}/Pt_BC_PERC
    cp -r ${DirIN}/Rainfall_${AccSTR}h/WT/${Year}* ${DirOUT_temp}/WT
done