#!/bin/bash

Git_Repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN="Scripts/Processed"
#Dataset_list=("TrainML_NoEastFF_AllPredictors" "TrainML_NoEastFF_NoPopDens" "TrainML_NoEastGP_AllPredictors" "TrainML_NoEastGP_NoPopDens" "TrainML_NoWestFF_AllPredictors" "TrainML_NoWestFF_NoPopDens" "TrainML_NoWestGP_AllPredictors" "TrainML_NoWestGP_NoPopDens" "TrainML_NoNorthFF_AllPredictors" "TrainML_NoNorthFF_NoPopDens" "TrainML_NoNorthGP_AllPredictors" "TrainML_NoNorthGP_NoPopDens" "TrainML_NoSouthFF_AllPredictors" "TrainML_NoSouthFF_NoPopDens" "TrainML_NoSouthGP_AllPredictors" "TrainML_NoSouthGP_NoPopDens" "TrainML_NoEastFF_AllPredictors_CW" "TrainML_NoEastFF_NoPopDens_CW" "TrainML_NoEastGP_AllPredictors_CW" "TrainML_NoEastGP_NoPopDens_CW" "TrainML_NoWestFF_AllPredictors_CW" "TrainML_NoWestFF_NoPopDens_CW" "TrainML_NoWestGP_AllPredictors_CW" "TrainML_NoWestGP_NoPopDens_CW" "TrainML_NoNorthFF_AllPredictors_CW" "TrainML_NoNorthFF_NoPopDens_CW" "TrainML_NoNorthGP_AllPredictors_CW" "TrainML_NoNorthGP_NoPopDens_CW" "TrainML_NoSouthFF_AllPredictors_CW" "TrainML_NoSouthFF_NoPopDens_CW" "TrainML_NoSouthGP_AllPredictors_CW" "TrainML_NoSouthGP_NoPopDens_CW")
Dataset_list=("TrainML_NoEastFF_AllPredictors" "TrainML_NoEastFF_AllPredictors_CW")

for Dataset in ${Dataset_list[@]}; do

      DirIN_temp="${Git_Repo}/${DirIN}/${Dataset}"
      echo $DirIN_temp
      sbatch ${DirIN_temp}/20a_SubmitterATOS_TrainML.sh

done