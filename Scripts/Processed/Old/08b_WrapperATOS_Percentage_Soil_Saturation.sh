#!/bin/bash

Year_S=2005
Year_F=2021
echo "Plotting the percentage of soil saturation for year:"
for Year in $(seq $Year_S $Year_F); do
      echo " - $Year"
      sbatch 08a_SubmitterATOS_Percentage_Soil_Saturation.sh $Year
done
