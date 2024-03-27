#!/bin/bash

#SBATCH --job-name=Compute_ClassRP_Year
#SBATCH --output=LogATOS/Compute_ClassRP_Year-%J.out
#SBATCH --error=LogATOS/Compute_ClassRP_Year-%J.out
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=2-00:00:00
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
Year=${1}

python3 07_Compute_ClassRP_AccTP.py ${Year}