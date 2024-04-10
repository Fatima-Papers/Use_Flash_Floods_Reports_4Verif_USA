#!/bin/bash

#SBATCH --job-name=Combine_PDT
#SBATCH --output=LogATOS/Combine_PDT-%J.out
#SBATCH --error=LogATOS/Combine_PDT-%J.out
#SBATCH --cpus-per-task=64
#SBATCH --mem=128G
#SBATCH --time=2-00:00:00
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
Year_S=${1}
Year_F=${2}
Type_ReductionFF=${3}
Name_Region=${4}
North_South_LatBoundary=${5}
West_East_LonBoundary=${6}
NamePred=${7}
Pred2Keep=${8}
Perc_RedFF_list=${9}
Repetitions_RedFF=${10}
Git_Repo=${11}
FileIN_Mask=${12}
DirIN=${13}
DirOUT=${14}

python3 26_Compute_Combine_PDT.py ${Year_S} ${Year_F} ${Type_ReductionFF} ${Name_Region} ${North_South_LatBoundary} ${West_East_LonBoundary} ${NamePred} ${Pred2Keep} ${Perc_RedFF_list} ${Repetitions_RedFF} ${Git_Repo} ${FileIN_Mask} ${DirIN} ${DirOUT}