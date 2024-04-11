#!/bin/bash

# General inputs
Year=2021
Name3="2005_2020"

# # Submitting the first batch of jobs
# Name1_list=("AllFF" "NoNorthFF" "NoNorthGP" "NoSouthFF" "NoSouthGP" "NoWestFF" "NoWestGP" "NoEastFF" "NoEastGP")
# Name2_list=("AllPred" "NoPD")

# for Name1 in "${Name1_list[@]}"; do
#       for Name2 in "${Name2_list[@]}"; do
#             echo "Training the ANN with the ${Name1}_${Name2}_${Name3} training dataset"
#             DirIN="Data/Compute/28_Prob_AccRepFF/${Name1}_${Name3}/${Name2}"
#             DirOUT="Data/Plot/30_Prob_AccRepFF/${Name1}_${Name3}/${Name2}"
#             sbatch 30a_SubmitterATOS_Prob_AccRepFF.sh ${Year} ${DirIN} ${DirOUT}
#       done
# done

# Submitting the first batch of jobs
Name1="RedRndFF"
Name2_list=("AllPred" "NoPD")
Name4_list=(10 50 90)

for Name2 in "${Name2_list[@]}"; do
      for Name4 in "${Name4_list[@]}"; do
            echo "Training the ANN with the ${Name1}/pdt_${Name1}_${Name4}_${Name2}_${Name3} training dataset"
            DirIN="Data/Compute/29_Prob_AccRepFF_Mean_RedRndFF/${Name1}_${Name3}/${Name2}/${Name4}/Mean"
            DirOUT="Data/Plot/30_Prob_AccRepFF/${Name1}_${Name3}/${Name2}/${Name4}/Mean"
            sbatch 30a_SubmitterATOS_Prob_AccRepFF.sh ${Year} ${DirIN} ${DirOUT}
      done
done