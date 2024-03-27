#!/bin/bash

Year_S=2005
Year_F=2021
echo "Plotting the class of the RP for rainfall reanalysis:"
for Year in $(seq $Year_S $Year_F); do
      echo " - $Year"
      sbatch 08a_SubmitterATOS_ClassRP_AccTP.sh $Year
done
