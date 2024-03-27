#!/bin/bash

#SBATCH --job-name=Compute_Ratio_Year
#SBATCH --output=LogATOS/Compute_Ratio_Year-%J.out
#SBATCH --error=LogATOS/Compute_Ratio_Year-%J.out
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=2-00:00:00
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
Year=${1}

python3 09_Compute_Ratio_Extreme_Mean_AccTP.py ${Year}