#!/bin/bash

#SBATCH --job-name=Combine_DPT
#SBATCH --output=/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA/Scripts/Processed/LogATOS/Combine_DPT-%J.out
#SBATCH --error=/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA/Scripts/Processed/LogATOS/Combine_DPT-%J.out
#SBATCH --cpus-per-task=64
#SBATCH --mem=128G
#SBATCH --time=2-00:00:00
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

python3 TrainML_NoNorthGP_NoPopDens/19_Compute_Combine_PDT.py