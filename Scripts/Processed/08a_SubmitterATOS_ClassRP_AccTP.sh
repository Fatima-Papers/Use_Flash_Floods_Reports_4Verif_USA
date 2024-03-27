#!/bin/bash

#SBATCH --job-name=Plot_ClassRP_Year
#SBATCH --output=LogATOS/Plot_ClassRP_Year-%J.out
#SBATCH --error=LogATOS/Plot_ClassRP_Year-%J.out
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=2-00:00:00
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
Year=${1}

python3 08_Plot_ClassRP_AccTP.py ${Year}