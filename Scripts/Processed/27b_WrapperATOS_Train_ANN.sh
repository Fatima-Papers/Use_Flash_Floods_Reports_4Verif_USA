#!/bin/bash

# Submit the first batch of jobs
Git_Repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
Name1_list=("AllFF", "NoNorthFF" "NoNorthGP" "NoSouthFF" "NoSouthGP" "NoWestFF" "NoWestGP" "NoEastFF" "NoEastGP")
Name2_list=("AllPred" "NoPD")
Name3="2005_2020"

for Name1 in "${Name1_list[@]}"; do
      for Name2 in "${Name2_list[@]}"; do
            echo "Training the ANN with the ${Name1}_${Name2}_${Name3} training dataset"
            FileIN="Data/Compute/26_Combine_PDT/${Name1}/pdt_${Name1}_${Name2}_${Name3}.npy"
            DirOUT="Data/Compute/27_Train_ANN/${Name1}_${Name3}/${Name2}"
            sbatch 27a_SubmitterATOS_Train_ANN.sh ${Git_Repo} ${FileIN} ${DirOUT}
      done
done

# Submit the second batch of jobs
Git_Repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
Name1="RedRndFF"
Name2_list=("AllPred" "NoPD")
Name3="2005_2020"
Name4_list=(10 50 90)
Rep_S=0
Rep_F=99

for Name2 in "${Name2_list[@]}"; do
      for Name4 in "${Name4_list[@]}"; do
            for Name5 in $(seq -f "%02g" ${Rep_S} ${Rep_F}); do
                  echo "Training the ANN with the ${Name1}/pdt_${Name1}_${Name4}_${Name5}_${Name2}_${Name3} training dataset"
                  FileIN="Data/Compute/26_Combine_PDT/${Name1}/pdt_${Name1}_${Name4}_${Name5}_${Name2}_${Name3}.npy"
                  DirOUT="Data/Compute/27_Train_ANN/${Name1}_${Name3}/${Name2}/${Name4}/${Name5}"
                  sbatch 27a_SubmitterATOS_Train_ANN.sh ${Git_Repo} ${FileIN} ${DirOUT}
            done
      done
done