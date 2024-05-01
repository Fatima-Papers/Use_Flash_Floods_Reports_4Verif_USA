#!/bin/bash

#SBATCH --job-name=Plot_Prob_AccRepFF_Global
#SBATCH --output=LogATOS/Plot_Prob_AccRepFF_Global-%J.out
#SBATCH --error=LogATOS/Plot_Prob_AccRepFF_Global-%J.out
#SBATCH --cpus-per-task=64
#SBATCH --mem=128G
#SBATCH --time=2-00:00:00
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
Year=${1}
DirIN=${2}
DirOUT=${3}

python3 43_Plot_Prob_AccRepFF_Global.py ${Year} ${DirIN} ${DirOUT}