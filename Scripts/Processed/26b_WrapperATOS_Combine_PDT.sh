#!/bin/bash

# General Inputs
Year_S=2005
Year_F=2020
North_South_LatBoundary=38
West_East_LonBoundary=-100
Git_Repo="/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask="Data/Raw/Mask/USA_ERA5/Mask.grib"
DirIN="Data/Compute/25_PDT_Year"
DirOUT="Data/Compute/26_Combine_PDT"

#############################
# Specific Inputs - NoNorthFF_AllPred
Type_ReductionFF="FF"
Name_Region="North"
NamePred="StdOrog,ClassRP,RatioEM,PercSS,LAI,PD"
Pred2Keep="True,True,True,True,True,True"
Perc_RedFF_list="10,50,90"
Repetitions_RedFF=10
sbatch 26a_SubmitterATOS_Combine_PDT.sh ${Year_S} ${Year_F} ${Type_ReductionFF} ${Name_Region} ${North_South_LatBoundary} ${West_East_LonBoundary} ${NamePred} ${Pred2Keep} ${Perc_RedFF_list} ${Repetitions_RedFF} ${Git_Repo} ${FileIN_Mask} ${DirIN} ${DirOUT}

# Specific Inputs - NoSouthFF_AllPred
Type_ReductionFF="FF"
Name_Region="South"
NamePred="StdOrog,ClassRP,RatioEM,PercSS,LAI,PD"
Pred2Keep="True,True,True,True,True,True"
Perc_RedFF_list="10,50,90"
Repetitions_RedFF=10
sbatch 26a_SubmitterATOS_Combine_PDT.sh ${Year_S} ${Year_F} ${Type_ReductionFF} ${Name_Region} ${North_South_LatBoundary} ${West_East_LonBoundary} ${NamePred} ${Pred2Keep} ${Perc_RedFF_list} ${Repetitions_RedFF} ${Git_Repo} ${FileIN_Mask} ${DirIN} ${DirOUT}

# Specific Inputs - NoWestFF_AllPred
Type_ReductionFF="FF"
Name_Region="West"
NamePred="StdOrog,ClassRP,RatioEM,PercSS,LAI,PD"
Pred2Keep="True,True,True,True,True,True"
Perc_RedFF_list="10,50,90"
Repetitions_RedFF=10
sbatch 26a_SubmitterATOS_Combine_PDT.sh ${Year_S} ${Year_F} ${Type_ReductionFF} ${Name_Region} ${North_South_LatBoundary} ${West_East_LonBoundary} ${NamePred} ${Pred2Keep} ${Perc_RedFF_list} ${Repetitions_RedFF} ${Git_Repo} ${FileIN_Mask} ${DirIN} ${DirOUT}

# Specific Inputs - NoEastFF_AllPred
Type_ReductionFF="FF"
Name_Region="East"
NamePred="StdOrog,ClassRP,RatioEM,PercSS,LAI,PD"
Pred2Keep="True,True,True,True,True,True"
Perc_RedFF_list="10,50,90"
Repetitions_RedFF=10
sbatch 26a_SubmitterATOS_Combine_PDT.sh ${Year_S} ${Year_F} ${Type_ReductionFF} ${Name_Region} ${North_South_LatBoundary} ${West_East_LonBoundary} ${NamePred} ${Pred2Keep} ${Perc_RedFF_list} ${Repetitions_RedFF} ${Git_Repo} ${FileIN_Mask} ${DirIN} ${DirOUT}

############################
# Specific Inputs - NoNorthFF_NoPD
Type_ReductionFF="FF"
Name_Region="North"
NamePred="StdOrog,ClassRP,RatioEM,PercSS,LAI,PD"
Pred2Keep="True,True,True,True,True,False"
Perc_RedFF_list="10,50,90"
Repetitions_RedFF=10
sbatch 26a_SubmitterATOS_Combine_PDT.sh ${Year_S} ${Year_F} ${Type_ReductionFF} ${Name_Region} ${North_South_LatBoundary} ${West_East_LonBoundary} ${NamePred} ${Pred2Keep} ${Perc_RedFF_list} ${Repetitions_RedFF} ${Git_Repo} ${FileIN_Mask} ${DirIN} ${DirOUT}

# Specific Inputs - NoSouthFF_NoPD
Type_ReductionFF="FF"
Name_Region="South"
NamePred="StdOrog,ClassRP,RatioEM,PercSS,LAI,PD"
Pred2Keep="True,True,True,True,True,False"
Perc_RedFF_list="10,50,90"
Repetitions_RedFF=10
sbatch 26a_SubmitterATOS_Combine_PDT.sh ${Year_S} ${Year_F} ${Type_ReductionFF} ${Name_Region} ${North_South_LatBoundary} ${West_East_LonBoundary} ${NamePred} ${Pred2Keep} ${Perc_RedFF_list} ${Repetitions_RedFF} ${Git_Repo} ${FileIN_Mask} ${DirIN} ${DirOUT}

# Specific Inputs - NoWestFF_NoPD
Type_ReductionFF="FF"
Name_Region="West"
NamePred="StdOrog,ClassRP,RatioEM,PercSS,LAI,PD"
Pred2Keep="True,True,True,True,True,False"
Perc_RedFF_list="10,50,90"
Repetitions_RedFF=10
sbatch 26a_SubmitterATOS_Combine_PDT.sh ${Year_S} ${Year_F} ${Type_ReductionFF} ${Name_Region} ${North_South_LatBoundary} ${West_East_LonBoundary} ${NamePred} ${Pred2Keep} ${Perc_RedFF_list} ${Repetitions_RedFF} ${Git_Repo} ${FileIN_Mask} ${DirIN} ${DirOUT}

# Specific Inputs - NoEastFF_NoPD
Type_ReductionFF="FF"
Name_Region="East"
NamePred="StdOrog,ClassRP,RatioEM,PercSS,LAI,PD"
Pred2Keep="True,True,True,True,True,False"
Perc_RedFF_list="10,50,90"
Repetitions_RedFF=10
sbatch 26a_SubmitterATOS_Combine_PDT.sh ${Year_S} ${Year_F} ${Type_ReductionFF} ${Name_Region} ${North_South_LatBoundary} ${West_East_LonBoundary} ${NamePred} ${Pred2Keep} ${Perc_RedFF_list} ${Repetitions_RedFF} ${Git_Repo} ${FileIN_Mask} ${DirIN} ${DirOUT}

#############################
# Specific Inputs - NoNorthGP_AllPred
Type_ReductionFF="GP"
Name_Region="North"
NamePred="StdOrog,ClassRP,RatioEM,PercSS,LAI,PD"
Pred2Keep="True,True,True,True,True,True"
Perc_RedFF_list="10,50,90"
Repetitions_RedFF=10
sbatch 26a_SubmitterATOS_Combine_PDT.sh ${Year_S} ${Year_F} ${Type_ReductionFF} ${Name_Region} ${North_South_LatBoundary} ${West_East_LonBoundary} ${NamePred} ${Pred2Keep} ${Perc_RedFF_list} ${Repetitions_RedFF} ${Git_Repo} ${FileIN_Mask} ${DirIN} ${DirOUT}

# Specific Inputs - NoSouthGP_AllPred
Type_ReductionFF="GP"
Name_Region="South"
NamePred="StdOrog,ClassRP,RatioEM,PercSS,LAI,PD"
Pred2Keep="True,True,True,True,True,True"
Perc_RedFF_list="10,50,90"
Repetitions_RedFF=10
sbatch 26a_SubmitterATOS_Combine_PDT.sh ${Year_S} ${Year_F} ${Type_ReductionFF} ${Name_Region} ${North_South_LatBoundary} ${West_East_LonBoundary} ${NamePred} ${Pred2Keep} ${Perc_RedFF_list} ${Repetitions_RedFF} ${Git_Repo} ${FileIN_Mask} ${DirIN} ${DirOUT}

# Specific Inputs - NoWestGP_AllPred
Type_ReductionFF="GP"
Name_Region="West"
NamePred="StdOrog,ClassRP,RatioEM,PercSS,LAI,PD"
Pred2Keep="True,True,True,True,True,True"
Perc_RedFF_list="10,50,90"
Repetitions_RedFF=10
sbatch 26a_SubmitterATOS_Combine_PDT.sh ${Year_S} ${Year_F} ${Type_ReductionFF} ${Name_Region} ${North_South_LatBoundary} ${West_East_LonBoundary} ${NamePred} ${Pred2Keep} ${Perc_RedFF_list} ${Repetitions_RedFF} ${Git_Repo} ${FileIN_Mask} ${DirIN} ${DirOUT}

# Specific Inputs - NoEastGP_AllPred
Type_ReductionFF="GP"
Name_Region="East"
NamePred="StdOrog,ClassRP,RatioEM,PercSS,LAI,PD"
Pred2Keep="True,True,True,True,True,True"
Perc_RedFF_list="10,50,90"
Repetitions_RedFF=10
sbatch 26a_SubmitterATOS_Combine_PDT.sh ${Year_S} ${Year_F} ${Type_ReductionFF} ${Name_Region} ${North_South_LatBoundary} ${West_East_LonBoundary} ${NamePred} ${Pred2Keep} ${Perc_RedFF_list} ${Repetitions_RedFF} ${Git_Repo} ${FileIN_Mask} ${DirIN} ${DirOUT}

############################
# Specific Inputs - NoNorthGP_NoPD
Type_ReductionFF="GP"
Name_Region="North"
NamePred="StdOrog,ClassRP,RatioEM,PercSS,LAI,PD"
Pred2Keep="True,True,True,True,True,False"
Perc_RedFF_list="10,50,90"
Repetitions_RedFF=10
sbatch 26a_SubmitterATOS_Combine_PDT.sh ${Year_S} ${Year_F} ${Type_ReductionFF} ${Name_Region} ${North_South_LatBoundary} ${West_East_LonBoundary} ${NamePred} ${Pred2Keep} ${Perc_RedFF_list} ${Repetitions_RedFF} ${Git_Repo} ${FileIN_Mask} ${DirIN} ${DirOUT}

# Specific Inputs - NoSouthGP_NoPD
Type_ReductionFF="GP"
Name_Region="South"
NamePred="StdOrog,ClassRP,RatioEM,PercSS,LAI,PD"
Pred2Keep="True,True,True,True,True,False"
Perc_RedFF_list="10,50,90"
Repetitions_RedFF=10
sbatch 26a_SubmitterATOS_Combine_PDT.sh ${Year_S} ${Year_F} ${Type_ReductionFF} ${Name_Region} ${North_South_LatBoundary} ${West_East_LonBoundary} ${NamePred} ${Pred2Keep} ${Perc_RedFF_list} ${Repetitions_RedFF} ${Git_Repo} ${FileIN_Mask} ${DirIN} ${DirOUT}

# Specific Inputs - NoWestGP_NoPD
Type_ReductionFF="GP"
Name_Region="West"
NamePred="StdOrog,ClassRP,RatioEM,PercSS,LAI,PD"
Pred2Keep="True,True,True,True,True,False"
Perc_RedFF_list="10,50,90"
Repetitions_RedFF=10
sbatch 26a_SubmitterATOS_Combine_PDT.sh ${Year_S} ${Year_F} ${Type_ReductionFF} ${Name_Region} ${North_South_LatBoundary} ${West_East_LonBoundary} ${NamePred} ${Pred2Keep} ${Perc_RedFF_list} ${Repetitions_RedFF} ${Git_Repo} ${FileIN_Mask} ${DirIN} ${DirOUT}

# Specific Inputs - NoEastGP_NoPD
Type_ReductionFF="GP"
Name_Region="East"
NamePred="StdOrog,ClassRP,RatioEM,PercSS,LAI,PD"
Pred2Keep="True,True,True,True,True,False"
Perc_RedFF_list="10,50,90"
Repetitions_RedFF=10
sbatch 26a_SubmitterATOS_Combine_PDT.sh ${Year_S} ${Year_F} ${Type_ReductionFF} ${Name_Region} ${North_South_LatBoundary} ${West_East_LonBoundary} ${NamePred} ${Pred2Keep} ${Perc_RedFF_list} ${Repetitions_RedFF} ${Git_Repo} ${FileIN_Mask} ${DirIN} ${DirOUT}

##############################
# Specific Inputs - RedRndFF_AllPred
Type_ReductionFF="RedRndFF"
Name_Region="East"
NamePred="StdOrog,ClassRP,RatioEM,PercSS,LAI,PD"
Pred2Keep="True,True,True,True,True,True"
Perc_RedFF_list="10,50,90"
Repetitions_RedFF=100
sbatch 26a_SubmitterATOS_Combine_PDT.sh ${Year_S} ${Year_F} ${Type_ReductionFF} ${Name_Region} ${North_South_LatBoundary} ${West_East_LonBoundary} ${NamePred} ${Pred2Keep} ${Perc_RedFF_list} ${Repetitions_RedFF} ${Git_Repo} ${FileIN_Mask} ${DirIN} ${DirOUT}

# Specific Inputs - RedRndFF_NoPD
Type_ReductionFF="RedRndFF"
Name_Region="East"
NamePred="StdOrog,ClassRP,RatioEM,PercSS,LAI,PD"
Pred2Keep="True,True,True,True,True,False"
Perc_RedFF_list="10,50,90"
Repetitions_RedFF=100
sbatch 26a_SubmitterATOS_Combine_PDT.sh ${Year_S} ${Year_F} ${Type_ReductionFF} ${Name_Region} ${North_South_LatBoundary} ${West_East_LonBoundary} ${NamePred} ${Pred2Keep} ${Perc_RedFF_list} ${Repetitions_RedFF} ${Git_Repo} ${FileIN_Mask} ${DirIN} ${DirOUT}

##############################
# Specific Inputs - AllFF_AllPred
Type_ReductionFF="AllFF"
Name_Region="East"
NamePred="StdOrog,ClassRP,RatioEM,PercSS,LAI,PD"
Pred2Keep="True,True,True,True,True,True"
Perc_RedFF_list="10,50,90"
Repetitions_RedFF=100
sbatch 26a_SubmitterATOS_Combine_PDT.sh ${Year_S} ${Year_F} ${Type_ReductionFF} ${Name_Region} ${North_South_LatBoundary} ${West_East_LonBoundary} ${NamePred} ${Pred2Keep} ${Perc_RedFF_list} ${Repetitions_RedFF} ${Git_Repo} ${FileIN_Mask} ${DirIN} ${DirOUT}

# Specific Inputs - AllFF_NoPD
Type_ReductionFF="AllFF"
Name_Region="East"
NamePred="StdOrog,ClassRP,RatioEM,PercSS,LAI,PD"
Pred2Keep="True,True,True,True,True,False"
Perc_RedFF_list="10,50,90"
Repetitions_RedFF=100
sbatch 26a_SubmitterATOS_Combine_PDT.sh ${Year_S} ${Year_F} ${Type_ReductionFF} ${Name_Region} ${North_South_LatBoundary} ${West_East_LonBoundary} ${NamePred} ${Pred2Keep} ${Perc_RedFF_list} ${Repetitions_RedFF} ${Git_Repo} ${FileIN_Mask} ${DirIN} ${DirOUT}
