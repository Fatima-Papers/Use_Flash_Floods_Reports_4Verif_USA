#!/bin/bash

Year_S=2024
Year_F=2024
echo "Computing Percentage soil saturation for year:"
for Year in $(seq $Year_S $Year_F); do
      echo " - $Year"
      sbatch 11a_SubmitterATOS_Percentage_Soil_Saturation.sh $Year
done
