#!/bin/bash

#SBATCH --job-name=Counts_FC_OBS_Exceeding_VRT
#SBATCH --output=LogATOS/Counts_FC_OBS_Exceeding_VRT-%J.out
#SBATCH --error=LogATOS/Counts_FC_OBS_Exceeding_VRT-%J.out
#SBATCH --cpus-per-task=64
#SBATCH --mem=128G
#SBATCH --time=2-00:00:00
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
StepF=${1}

python3 37_Compute_Counts_FC_OBS_Exceeding_VRT.py ${StepF} 