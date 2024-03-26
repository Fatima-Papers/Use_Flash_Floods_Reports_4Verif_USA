#!/bin/bash

#SBATCH --job-name=PDT_Year
#SBATCH --output=LogATOS/PDT_Year-%J.out
#SBATCH --error=LogATOS/PDT_Year-%J.out
#SBATCH --cpus-per-task=64
#SBATCH --mem=128G
#SBATCH --time=2-00:00:00
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
Year=${1}

python3 18_Compute_PDT_Year.py ${Year}