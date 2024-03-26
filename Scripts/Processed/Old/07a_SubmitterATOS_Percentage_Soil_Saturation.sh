#!/bin/bash

#SBATCH --job-name=Compute_Perc_Soil_Sat_Year
#SBATCH --output=LogATOS/Compute_Perc_Soil_Sat_Year-%J.out
#SBATCH --error=LogATOS/Compute_Perc_Soil_Sat_Year-%J.out
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=2-00:00:00
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
Year=${1}

python3 07_Compute_Percentage_Soil_Saturation.py ${Year}