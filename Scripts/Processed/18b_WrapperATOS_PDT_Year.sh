#!/bin/bash

Year_S=1996
Year_F=2021
echo "Computing PDT for year:"
for Year in $(seq $Year_S $Year_F); do
      echo " - $Year"
      sbatch 09a_SubmitterATOS_PDT_Year.sh $Year
done
