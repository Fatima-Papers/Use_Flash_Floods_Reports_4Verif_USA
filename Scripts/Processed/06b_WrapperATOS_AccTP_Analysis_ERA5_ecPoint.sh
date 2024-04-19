#!/bin/bash

Year_S=2005
Year_F=2022
echo "Plotting rainfall from ERA5-ecPoint reanalysis for year:"
for Year in $(seq $Year_S $Year_F); do
      echo " - $Year"
      sbatch 06a_SubmitterATOS_AccTP_Analysis_ERA5_ecPoint.sh $Year
done
