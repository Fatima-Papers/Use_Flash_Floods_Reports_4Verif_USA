#!/bin/bash

##########################################################################
# CODE DESCRIPTION
# Retrieve_Analysis_ERA5_sdfor.sh retrieves from MARS the standard deviation of the 
# sub-gridscale orography from ERA5 (31 km resolution). The field is static.
# Runtime: the code takes few seconds to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Git_Repo (string): repository's local path.
# FileOUT (string): relative path of the file containing the slope of sub-gridscale orography.

# INPUT PARAMETERS
Git_Repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileOUT="Data/Raw/Analysis/ERA5/sdor/sdor.grib"
##########################################################################

# Setting the output directory
DirOUT="${FileOUT%/*}"
FileNameOUT="${FileOUT##*/}"
MainDirOUT=${Git_Repo}/${DirOUT}
mkdir -p ${MainDirOUT}

# Retrieving the orography fields from MARS 
mars <<EOF

    retrieve,
        class=ea,
        date=19400101,
        expver=1,
        levtype=sfc,
        param=160.128,
        step=0,
        stream=oper,
        time=0,
        type=an,
        target="${MainDirOUT}/${FileNameOUT}"

EOF