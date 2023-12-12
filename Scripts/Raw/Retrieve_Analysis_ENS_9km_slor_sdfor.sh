#!/bin/bash

##########################################################################
# CODE DESCRIPTION
# Retrieve_Analysis_ENS_9km_slor_sdfor.sh retrieves from MARS the slope and the 
# standard deviation of the sub-gridscale orography from ECMWF ENS at 9km resolution. 
# The field is static.
# Runtime: the code takes few minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Git_Repo (string): repository's local path.
# FileOUT (string): relative path of the file containing the slope of sub-gridscale orography.

# INPUT PARAMETERS
Git_Repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileOUT_slor="Data/Raw/Analysis/ENS_9km/slor/slor.grib"
FileOUT_sdor="Data/Raw/Analysis/ENS_9km/sdor/sdor.grib"
##########################################################################

# Setting the output directory
DirOUT_slor="${FileOUT_slor%/*}"
FileNameOUT_slor="${FileOUT_slor##*/}"
MainDirOUT_slor=${Git_Repo}/${DirOUT_slor}
mkdir -p ${MainDirOUT_slor}

DirOUT_sdor="${FileOUT_sdor%/*}"
FileNameOUT_sdor="${FileOUT_sdor##*/}"
MainDirOUT_sdor=${Git_Repo}/${DirOUT_sdor}
mkdir -p ${MainDirOUT_sdor}

# Retrieving the orography fields from MARS 
mars <<EOF

    retrieve,
        class=od,
        date=0,
        expver=1,
        levtype=sfc,
        param=163.128,
        step=0,
        stream=enfo,
        time=0,
        type=cf,
        target="${MainDirOUT_slor}/${FileNameOUT_slor}"

    retrieve,
        param=160.128,
        target="${MainDirOUT_sdor}/${FileNameOUT_sdor}"

EOF