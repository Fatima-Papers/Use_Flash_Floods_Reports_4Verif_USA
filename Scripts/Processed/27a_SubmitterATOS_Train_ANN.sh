#!/bin/bash

#SBATCH --job-name=Train_ANN
#SBATCH --output=LogATOS/Train_ANN-%J.out
#SBATCH --error=LogATOS/Train_ANN-%J.out
#SBATCH --cpus-per-task=64
#SBATCH --mem=128G
#SBATCH --time=2-00:00:00
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
Git_Repo=${1}
FileIN=${2}
DirOUT=${3}

python3 27_Compute_Train_ANN.py ${Git_Repo} ${FileIN} ${DirOUT}