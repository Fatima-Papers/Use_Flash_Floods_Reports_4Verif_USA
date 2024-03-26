#!/bin/bash

Year_S=2005
Year_F=2023
echo "Plotting the maps of accumulated point flash flood reports for:"
for Year in $(seq $Year_S $Year_F); do
      echo " - $Year"
      sbatch 15a_SubmitterATOS_Map_Point_AccRepFF.sh $Year
done
