#!/bin/bash

Year_S=2005
Year_F=2023
echo "Computing the accumulated gridded flash flood reports for:"
for Year in $(seq $Year_S $Year_F); do
      echo " - $Year"
      sbatch 19a_SubmitterATOS_Grid_AccRepFF.sh $Year
done