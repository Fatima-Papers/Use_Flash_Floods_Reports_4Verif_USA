#!/bin/bash

# General inputs
Name1="AllFF"
Name2="NoPD"
Name3="2005_2020"

Year_S=2024
Year_F=2024
echo "Computing the flash flood probabilities for:"
for Year in $(seq $Year_S $Year_F); do
      echo " - $Year"
      DirIN="Data/Compute/42_Prob_AccRepFF_Global/${Name1}_${Name3}/${Name2}"
      DirOUT="Data/Plot/43_Prob_AccRepFF_Global/${Name1}_${Name3}/${Name2}"
      sbatch 43a_SubmitterATOS_Prob_AccRepFF_Global.sh ${Year} ${DirIN} ${DirOUT}
done