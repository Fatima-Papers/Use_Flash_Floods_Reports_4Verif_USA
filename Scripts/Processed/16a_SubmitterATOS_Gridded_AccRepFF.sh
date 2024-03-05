#!/bin/bash

#SBATCH --job-name=Gridded_AccRepFF
#SBATCH --output=LogATOS/Gridded_AccRepFF-%J.out
#SBATCH --error=LogATOS/Gridded_AccRepFF-%J.out
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=2-00:00:00
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
Year=${1}

python3 16_Compute_Gridded_AccRepFF.py ${Year}