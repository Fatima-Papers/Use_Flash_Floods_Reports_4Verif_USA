#!/bin/bash

#SBATCH --job-name=Grid_AccRepFF
#SBATCH --output=LogATOS/Grid_AccRepFF-%J.out
#SBATCH --error=LogATOS/Grid_AccRepFF-%J.out
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=2-00:00:00
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
Year=${1}

python3 19_Compute_Grid_AccRepFF.py ${Year}