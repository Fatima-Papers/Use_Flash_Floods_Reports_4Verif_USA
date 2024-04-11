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
#             DirIN_ANN="Data/Compute/27_Train_ANN/${Name1}_${Name3}/${Name2}"
#             DirOUT="Data/Compute/28_Prob_AccRepFF/${Name1}_${Name3}/${Name2}"
#             sbatch 28a_SubmitterATOS_Prob_AccRepFF.sh ${Year} ${DirIN_ANN} ${DirOUT}
#       done
# done

# Submitting the first batch of jobs
Name1="RedRndFF"
Name2_list=("AllPred" "NoPD")
Name4_list=(10 50 90)
Rep_S=30
Rep_F=49

for Name2 in "${Name2_list[@]}"; do
      for Name4 in "${Name4_list[@]}"; do
            for Name5 in $(seq -f "%02g" ${Rep_S} ${Rep_F}); do
                  echo "Training the ANN with the ${Name1}/pdt_${Name1}_${Name4}_${Name5}_${Name2}_${Name3} training dataset"
                  DirIN_ANN="Data/Compute/27_Train_ANN/${Name1}_${Name3}/${Name2}/${Name4}/${Name5}"
                  DirOUT="Data/Compute/28_Prob_AccRepFF/${Name1}_${Name3}/${Name2}/${Name4}/${Name5}"
                  sbatch 28a_SubmitterATOS_Prob_AccRepFF.sh ${Year} ${DirIN_ANN} ${DirOUT}
            done
      done
done