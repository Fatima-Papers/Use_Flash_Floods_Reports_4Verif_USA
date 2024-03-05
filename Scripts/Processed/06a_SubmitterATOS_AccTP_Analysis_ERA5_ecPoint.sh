#!/bin/bash

#SBATCH --job-name=Plot_AccTP_Year
#SBATCH --output=LogATOS/Plot_AccTP_Year-%J.out
#SBATCH --error=LogATOS/Plot_AccTP_Year-%J.out
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=2-00:00:00
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
Year=${1}

python3 06_Plot_AccTP_Analysis_ERA5_ecPoint.py ${Year}