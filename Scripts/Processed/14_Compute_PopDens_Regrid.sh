#!/bin/bash

#SBATCH --job-name=PopDens_Regrid
#SBATCH --output=LogATOS/PopDens_Regrid-%J.out
#SBATCH --error=LogATOS/PopDens_Regrid-%J.out
#SBATCH --cpus-per-task=32
#SBATCH --mem=128G
#SBATCH --time=2-00:00:00
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

#############################################################################################
# CODE DESCRIPTION
# 14_Compute_PopDens_Regrid.py regrids the original NASA's population density (at different resolutions) to the 
# required grid resolution.
# Runtime: the code can take up to 10 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year (integer, in YYYY format): year to consider.
# Grid_Raw (string): grid of NASA's raw dataset.
# Grid_New (string): new grid to consider.
# Interpolation_type (string): type of interpolation.
# Interpolation_stats (string): statistic to compute during the interpolation.
# Git_Repo (string): repository's local path.
# DirIN (string): relative path of the directory containing NASA's raw population density.
# DirOUT (string): relative path of  the directory containing the extracted raw and interpolated population density.

# INPUT PARAMETERS
Year=${1}
Grid_Raw="30_sec"
Grid_New="N320"
Interpolation_type="grid-box-statistics"
Interpolation_stats="maximum"
Git_Repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN="Data/Compute/13_PopDens_Convert_tiff2grib_RawRes"
DirOUT="Data/Compute/14_PopDens_Regrid"
#############################################################################################

# Loading the needed libraries for the regrid
module load ecmwf-toolbox/new

# Providing the right setting to encode high-resolution lat/lon coordinates
FileIN="${Git_Repo}/${DirIN}/${Year}/PopDens_${Grid_Raw}_${Year}.grib2"
FileOUT="${Git_Repo}/${DirIN}/${Year}/PopDens_${Grid_Raw}_${Year}-fixed.grib2"
grib_set -s basicAngleOfTheInitialProductionDomain=1,subdivisionsOfBasicAngle=240,iDirectionIncrement=2,jDirectionIncrement=2,latitudeOfFirstGridPoint=21599,longitudeOfFirstGridPoint=43201,latitudeOfLastGridPoint=-21599,longitudeOfLastGridPoint=43199 ${FileIN} ${FileOUT}

# Regrid the original population density data to the required grid
mkdir -p "${Git_Repo}/${DirOUT}/${Grid_New}"
FileIN="${Git_Repo}/${DirIN}/${Year}/PopDens_${Grid_Raw}_${Year}-fixed.grib2"
FileOUT="${Git_Repo}/${DirOUT}/${Grid_New}/PopDens_${Year}.grib2"
MIR_DEBUB=1 mir ${FileIN} ${FileOUT} --grid=${Grid_New} --interpolation ${Interpolation_type} --interpolation-statistics ${Interpolation_stats}