#!/bin/bash

for StepF in $(seq -f "%02g" 12 12 240); do
      sbatch 37a_SubmitterATOS_Counts_FC_OBS_Exceeding_VRT.sh ${StepF}
done