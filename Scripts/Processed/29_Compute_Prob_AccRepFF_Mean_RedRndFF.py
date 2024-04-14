import os
from datetime import datetime, timedelta
import metview as mv

#######################################################################################################
# CODE DESCRIPTION
# 29_Compute_Prob_AccRepFF_Mean_RedRndFF.py computes the mean probabilities of having a flash flood event in a given 
# grid-box from the random reduction of flash flood reports in the training dataset.
# Runtime: the script can take up to 4 hours to compute in serial.

# INPUT PARAMETERS DESCRIPTION
# Year (integer, in YYYY format): year to consider.
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# NamePDT_list (list of integers): list of names for the PDTs to consider.
# Perc_Red_list (list of integers, from 0 to 100): list of reductions in percentage (%) of flash flood reports in the training dataset. 
# Rep (integer): number of repetitions for the random reduction of flash flood reports in the training dataset. 
# Git_Repo (string): repository's local path.
# Dir_IN_OUT (string): relative path of the directory containing the single and mean probabilities.

# INPUT PARAMETERS
Year = 2021
Acc = 12
Disc_Acc = 12
NamePDT_list = ["AllPred", "NoPD"]
Perc_Red_list = [10, 50, 90]
Rep = 100
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Compute/28_Prob_AccRepFF/RedRndFF_2005_2020"
DirOUT = "Data/Compute/29_Prob_AccRepFF_Mean_RedRndFF/RedRndFF_2005_2020"
#######################################################################################################


# Computing the mean probabilities of the randomly reduced training datasets
for NamePDT in NamePDT_list:

      for Perc_Red in Perc_Red_list:

            print("Computing the mean probabilities of the following randomly reduced training dataset: " + DirIN.split("/")[-1] + "_" + NamePDT + "_" + str(Perc_Red))
            print("Considering the single realizations: ")

            TheDateTime_Start_S = datetime(Year, 1, 1, 0)
            TheDateTime_Start_F = datetime(Year, 12, 31, 12)
            TheDateTime_Start = TheDateTime_Start_S
            while TheDateTime_Start <= TheDateTime_Start_F:

                  TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)
                  TheDateTime_PercSS = TheDateTime_Start - timedelta(days=1) # selecting the soil saturation percentage for 1 day prior the considered accumulation period (to not correlate it with the rainfall)
                  print(" - on " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC")
                  
                  prob_All_Realizations = None
                  for ind_Rep in range(Rep):

                        if Rep <= 10:
                              ind_Rep_STR = f"{ind_Rep:01}"
                        elif  Rep > 10 and  Rep <= 100:
                              ind_Rep_STR = f"{ind_Rep:02}"
                        elif Rep > 100 and  Rep <= 1000:
                              ind_Rep_STR = f"{ind_Rep:03}"
                        elif Rep > 1000 and  Rep <= 10000:
                              ind_Rep_STR = f"{ind_Rep:04}"
                        else:
                              print("ERROR! Number of repetions too big. Consider a maximum of 10000 repetions.")
                   
                        # Reading the single random realization
                        FileIN = Git_Repo + "/" + DirIN  + "/" + NamePDT   + "/" + f"{Perc_Red:02}" + "/" + ind_Rep_STR + "/Prob_AccRepFF_"  +  TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
                        prob_All_Realizations = mv.merge(prob_All_Realizations, mv.read(FileIN))

                  # Computing the mean of all the single random realizations
                  prob_mean = mv.mean(prob_All_Realizations)
                  
                  # Saving the mean of all the single random realizations
                  MainDirOUT = Git_Repo + "/" + DirOUT  + "/" + NamePDT   + "/" + f"{Perc_Red:02}" + "/Mean"
                  if not os.path.exists(MainDirOUT):
                        os.makedirs(MainDirOUT)
                  FileOUT = MainDirOUT + "/Prob_AccRepFF_"  +  TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
                  mv.write(FileOUT, prob_mean)
            
                  TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)