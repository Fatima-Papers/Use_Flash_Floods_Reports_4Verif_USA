#!/bin/bash

#SBATCH --job-name=Compute_Prob_AccRepFF
#SBATCH --output=LogATOS/Compute_Prob_AccRepFF-%J.out
#SBATCH --error=LogATOS/Compute_Prob_AccRepFF-%J.out
#SBATCH --cpus-per-task=64
#SBATCH --mem=128G
#SBATCH --time=2-00:00:00
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
Year=${1}
DirIN_ANN=${2}
DirOUT=${3}

python3 28_Compute_Prob_AccRepFF.py ${Year} ${DirIN_ANN} ${DirOUT}