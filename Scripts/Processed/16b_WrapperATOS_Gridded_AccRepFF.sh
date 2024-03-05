#!/bin/bash

Year_S=2005
Year_F=2021
echo "Computing the accumulated gridded flash flood reports for:"
for Year in $(seq $Year_S $Year_F); do
      echo " - $Year"
      sbatch 16a_SubmitterATOS_Gridded_AccRepFF.sh $Year
done
