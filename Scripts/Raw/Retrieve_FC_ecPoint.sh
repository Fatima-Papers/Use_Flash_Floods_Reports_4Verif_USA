#!/bin/bash

#########################################################################################################
# CODE DESCRIPTION
# Retrieve_FC_ecPoint.sh retrieves ecPoint-Rainfall forecasts from ECFS. Files contain global rainfall forecasts for the considered 
# accumulation period, ending at the time step indicated in the file name.
# Runtime: negligible.

# INPUT PARAMETERS DESCRIPTION
# BaseDateS (date, in YYYYMMDD format): start forecast's basedate to retrieve.
# BaseDateF (date, in YYYYMMDD format): final forecast's basedate to retrieve.
# BaseTime (time, in H format, in UTC time): forecast's basetime to retrieve .
# Acc (number, in H format, in hours): forecasts' accumulation period.
# CodeVers (string): version of the code that was used to compute the forecasts.
#                    Available code versions are  listed in the following webpage:
#                    https://confluence.ecmwf.int/display/EVAL/Forecasts+Code
# CalVers (string): version of the calibration that was used to compute the forecasts.
#                   Available calibration versions are listed in the following webpage:
#                   https://confluence.ecmwf.int/display/EVAL/1.+ecPoint-Rainfall%3A+Developed+or+Under-Development+Calibrations
# Git_Repo (string): repository's local path.
# DirIN (string): full path of the ECFS directory containing the forecasts to retrieve.
# DirOUT (string): relative path containing the retrieved forecasts.

# INPUT PARAMETERS
BaseDateS=20220101
BaseDateF=20221231
BaseTime=0
Acc=12
CodeVers="2.0.0"
CalVers="1.1.0"
Git_Repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN="ec:/ecpoint/forecasts/Oper/ECMWF_ENS/Rainfall"
DirOUT="Data/Raw/FC/ecPoint"
#########################################################################################################


# Setting general variables
BaseDateS=$(date -d ${BaseDateS} +%Y%m%d)
BaseDateF=$(date -d ${BaseDateF} +%Y%m%d)
BaseTimeSTR=$(printf %02d ${BaseTime})
AccSTR=$(printf %03d ${Acc})

# Setting output directory
MainDirOUT=${Git_Repo}/${DirOUT}
mkdir -p ${MainDirOUT}

# Retrieving forecasts from ECFS
BaseDate=${BaseDateS}
while [[ ${BaseDate} -le ${BaseDateF} ]]; do
    echo " "
    echo "Retrieving forecast for ${BaseDate}"
    ecfsdir ${DirIN}/${AccSTR}/Code${CodeVers}_Cal${CalVers}/${BaseDate}${BaseTimeSTR} ${MainDirOUT}/${BaseDate}${BaseTimeSTR}
    BaseDate=$(date -d"${BaseDate} + 1 day" +"%Y%m%d")
done