#!/bin/bash

Year_S=2000
Year_F=2020
Disc_Year=5
echo "Plotting the percentage of soil saturation for year:"
for Year in $(seq $Year_S ${Disc_Year} $Year_F); do
      echo " - $Year"
      sbatch 10_Compute_PopDens_Regrid.sh $Year
done