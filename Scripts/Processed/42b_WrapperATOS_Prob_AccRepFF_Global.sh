#!/bin/bash

Name1="AllFF"
Name2="NoPD"
Name3="2005_2020"

Year_S=2005
Year_F=2005
echo "Computing the flash flood probabilities for:"
for Year in $(seq $Year_S $Year_F); do
      echo " - $Year"
      DirIN_ANN="Data/Compute/27_Train_ANN/${Name1}_${Name3}/${Name2}"
      DirOUT="Data/Compute/42_Prob_AccRepFF_Global/${Name1}_${Name3}/${Name2}"
      sbatch 42a_SubmitterATOS_Prob_AccRepFF_Global.sh ${Year} ${DirIN_ANN} ${DirOUT}
done