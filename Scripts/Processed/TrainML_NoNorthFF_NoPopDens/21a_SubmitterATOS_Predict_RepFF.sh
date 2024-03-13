#!/bin/bash

#SBATCH --job-name=Predict_RepFF
#SBATCH --output=/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA/Scripts/Processed/LogATOS/Predict_RepFF-%J.out
#SBATCH --error=/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA/Scripts/Processed/LogATOS/Predict_RepFF-%J.out
#SBATCH --cpus-per-task=64
#SBATCH --mem=128G
#SBATCH --time=2-00:00:00
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

python3 TrainML_NoNorthFF_NoPopDens/21_Compute_Predict_RepFF.py