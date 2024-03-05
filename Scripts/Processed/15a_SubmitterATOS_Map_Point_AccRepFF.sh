#!/bin/bash

#SBATCH --job-name=Map_Point_AccRepFF
#SBATCH --output=LogATOS/Map_Point_AccRepFF-%J.out
#SBATCH --error=LogATOS/Map_Point_AccRepFF-%J.out
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=2-00:00:00
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
Year=${1}

python3 15_Plot_Map_Point_AccRepFF.py ${Year}