#!/bin/bash

Year_S=2023
Year_F=2024
echo "Computing the class of the RP for rainfall reanalysis:"
for Year in $(seq $Year_S $Year_F); do
      echo " - $Year"
      sbatch 07a_SubmitterATOS_ClassRP_AccTP.sh $Year
done
