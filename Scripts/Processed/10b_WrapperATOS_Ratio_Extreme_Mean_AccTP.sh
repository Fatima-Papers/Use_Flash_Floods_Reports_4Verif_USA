#!/bin/bash

Year_S=2005
Year_F=2021
echo "Plotting the ratio between the extreme and the mean point-rainfall ERA5-ecPoint reanalysis in each grid-box:"
for Year in $(seq $Year_S $Year_F); do
      echo " - $Year"
      sbatch 10a_SubmitterATOS_Ratio_Extreme_Mean_AccTP.sh $Year
done