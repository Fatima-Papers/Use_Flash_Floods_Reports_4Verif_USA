#!/bin/bash

##########################################################################
# CODE DESCRIPTION
# Retrieve_Analysis_ERA5_Land_swvl.sh retrieves from MARS the volumetric soil water 
# from ERA5-Land (9 km resolution).
# Runtime: the code takes up tp 24 hours to run in serial.

# INPUT PARAMETERS DESCRIPTION
# YearS (year, in YYYY format): start year to retrieve.
# YearF (year, in YYYY format): final year to retrieve.
# TimeS (integer, from 0 to 23, in UTC time): start time to retrieve. 
# TimeF (integer, from 0 to 23, in UTC time): final time to retrieve. 
# DiscTime (integer, in hours): discretization of the times to retrieve.
# Git_Repo (string): repository's local path.
# DirOUT (string): relative path containing the retrieved forecasts.

# INPUT PARAMETERS
YearS=1996
YearF=2022
TimeS=0
TimeF=23
DiscTime=1
Git_Repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirOUT="Data/Raw/Analysis/ERA5_Land"
##########################################################################


# Retrieveing the soil moisture from ERA5-LAND
for Year in $(seq ${YearS} ${YearF}); do

      for Month in 01 02 03 04 05 06 07 08 09 10 11 12; do
      
            DirDB_Temp="${Git_Repo}/${DirOUT}/TempDir"
            mkdir -p ${DirDB_Temp}

mars <<EOF
      retrieve,
            class=l5,
            date=${Year}${Month}01/to/${Year}${Month}31,
            expver=1,
            levtype=sfc,
            param=39.128/40.128/41.128,
            stream=oper,
            time=${TimeS}/to/${TimeF}/by/${DiscTime},
            type=an,
            target="${DirDB_Temp}/{shortName}_[date]_[time].grib"
EOF

            echo " "
            echo "Creating the database..."
            for FileName in `ls ${DirDB_Temp}`; do    
                  
                  ParamShortName="$(cut -d'_' -f1 <<<"$FileName")"
                  ParamDate="$(cut -d'_' -f2 <<<"$FileName")"
                  ParamTime_Extension="$(cut -d'_' -f3 <<<"$FileName")"    
                  ParamTime="$(cut -d'.' -f1 <<<"$ParamTime_Extension")"  
                  let ParamTime=${ParamTime}/100
                  ParamTime=$(printf "%02d" ${ParamTime})
                  
                  TempDir="${Git_Repo}/${DirOUT}/${ParamShortName}/${Year}/${ParamDate}"
                  mkdir -p ${TempDir}
                  mv "${DirDB_Temp}/${FileName}" "${TempDir}/${ParamShortName}_${ParamDate}_${ParamTime}.grib"

            done

            rm -rf ${DirDB_Temp}

            TheDate=$(date -d"${TheDate} + 1 day" +"%Y%m%d")

      done

done