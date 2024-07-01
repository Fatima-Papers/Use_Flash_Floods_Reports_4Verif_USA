import os
from datetime import datetime, timedelta
from random import choices
import itertools
import numpy as np

#########################################################################################
# CODE DESCRIPTION
# 38_Compute_AROC_BS.py computes the values of the Area Under the ROC curve with the trapezoidal 
# approximation.
# Code Runtime: the script takes 1 minute to run in serial.

# INPUT PARAMETERS DESCRIPTION
# BaseDateS (date, in format YYYYMMDD): start forecast base date for the considered verification period.
# BaseDateF (date, in format YYYYMMDD): final forecast base date for the considered verification period.
# StepF_Start (integer, in hours): start end step of the considered accumulation period.
# StepF_Final (integer, in hours): final end step of the considered accumulation period.

# Acc (number, in hours): rainfall accumulation to consider.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Perc_VRT (integer, from 0 to 100): percentile that defines the verifying rainfall event to consider.
# SystemFC (string): name of the forecasting systems to consider.
# RepetitionsBS (integer, from 0 to infinite): number of repetitions to consider in the bootstrapping.
# Git_Repo (string): repository's local path.
# DirIN (string): relative path of the directory containing the counts of EM and OBS exceeding a certain VRT.
# DirOUT (string): relative path of the directory containing the AROC values, including the bootstrapped ones.

# NOTES ON THE VALUES FOR "Perc_VRT"
# The percentiles correspond roughly to the following return periods:
# 99.9th -> once in 1 years
# 99.95th -> once in 2 years
# 99.98th -> once in 5 years
# 99.99th -> once in 10 years
# 99.995th -> once in 20 years

# INPUT PARAMETERS
BaseDateS = datetime(2022, 1, 1)
BaseDateF = datetime(2022, 12, 31)
StepF_Start = 12
StepF_Final = 240
Disc_Step = 12
Acc = 12
Perc_VRT = 99.9
Prob_Thr_list = [0.1, 1, 2, 3, 4, 5, 8, 10]
SystemFC = "ecPoint"
RepetitionsBS = 0
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Compute/37_Counts_FC_OBS_Exceeding_VRT"
DirOUT = "Data/Compute/38_AROC_BS"
#########################################################################################


# COSTUME FUNCTIONS

###########################################
# "Trapezoidal" Area Under the ROC curve (AROCt) #
###########################################

# Note: the computation of AROC values uses the trapezoidal approximation
def AROC_trapezoidal(count_em, count_obs, NumEM):

      # Computing the probabilistic contingency table
      ct = np.empty([NumEM+1, 4])
      for index in range(NumEM+1):
            count_members = NumEM - index
            OBS_yes_fc = count_obs[np.where(count_em >= count_members)[0]] # observation instances for "yes" forecasts
            OBS_no_fc = count_obs[np.where(count_em < count_members)[0]] # observation instances for "no" forecasts
            ct[index][0] = np.where(OBS_yes_fc > 0)[0].shape[0]  # hits
            ct[index][1] = np.where(OBS_yes_fc == 0)[0].shape[0]  # false alarms
            ct[index][2] = np.where(OBS_no_fc > 0)[0].shape[0]  # misses
            ct[index][3] = np.where(OBS_no_fc == 0)[0].shape[0]  # correct negatives
      ct = ct.astype(int)  # setting all values as integers

      # Computing hit rates (hr) and false alarm rates (far).
      hr = ct[:, 0] / (ct[:, 0] + ct[:, 2])  # hit rates
      far = ct[:, 1] / (ct[:, 1] + ct[:, 3])  # false alarms

      # Adding the points (0,0) and (1,1) to the arrays to ensure the ROC curve is closed.
      hr = np.insert(hr, 0, 0)
      hr = np.insert(hr, -1, 1)
      far = np.insert(far, 0, 0)
      far = np.insert(far, -1, 1)

      # Computing AROC with the trapezoidal approximation, and approximating its value to the second decimal digit.
      AROCt = 0
      for i in range(len(hr)-1):
            j = i+1
            a = hr[i]
            b = hr[i+1]
            h = far[i+1] - far[i]
            AROCt = AROCt + (((a+b)*h) / 2)
      AROCt = round(AROCt, 2)

      return hr, far, AROCt

####################################################################################################


print(" ")
print("Computing AROCt including " + str(RepetitionsBS) + " bootstrapped values")

# Defining the n. of ensemble members for the forecasting system
if SystemFC == "ENS":
      NumEM = 51
elif SystemFC == "ecPoint":
      NumEM = 99

# Creating the list containing the steps to considered in the computations
StepF_list = range(StepF_Start, (StepF_Final+1), Disc_Step)
m = len(StepF_list)

# Initializing the variable containing the AROCt and AROCz values, and the bootstrapped ones
AROCt_array = np.zeros([m, RepetitionsBS+2])

# Computing the Area Under the ROC
for ind in range(len(Prob_Thr_list)+1):

      for indStepF in range(len(StepF_list)):

            # Selecting the StepF to consider
            StepF = StepF_list[indStepF]
            print(" - Computing AROCt and AROCz for " + SystemFC +", VRT>=" + str(Perc_VRT) + ", StepF=" + str(StepF))

            # Storing information about the step computed
            AROCt_array[indStepF, 0] = StepF

            # Reading the daily counts of ensemble members and observations exceeding the considered verifying rainfall event.
            original_datesSTR_array = [] # list of dates for which the counts are created (not all steps might have one if the forecasts did not exist)
            Count_EM_original = [] # initializing the variable that will contain the counts of ensemble members exceeding the VRT for the original dates
            Count_OBS_original = [] # initializing the variable that will contain the counts of observations exceeding the VRT for the original dates
            BaseDate = BaseDateS
            while BaseDate <= BaseDateF:

                  FileIN = Git_Repo + "/" + DirIN + "/" + f"{Acc:02d}" + "h/PercVRT_" + str(Perc_VRT) + "/" + SystemFC + "/" + f"{StepF:03d}" + "/Count_FC_OBS_" + f"{Acc:02d}" + "h_PercVRT_" + str(Perc_VRT) + "_" + SystemFC + "_" + BaseDate.strftime("%Y%m%d") + "_" + BaseDate.strftime("%H") + "_" + f"{StepF:03d}" + ".npy"

                  if os.path.isfile(FileIN): # proceed if the files exists
                        original_datesSTR_array.append(BaseDate.strftime("%Y%m%d"))
                        Count_EM_OBS = np.load(FileIN)
                        Count_EM_original.append(Count_EM_OBS[0].tolist())
                        Count_OBS_original.append(Count_EM_OBS[ind+1].tolist())
                  BaseDate += timedelta(days=1)
            Count_EM_original = np.array(Count_EM_original, dtype=object)
            Count_OBS_original = np.array(Count_OBS_original, dtype=object)

            # Computing AROCt and AROCz for the original and the bootstrapped values
            for ind_repBS in range(RepetitionsBS+1):
                  
                  # Selecting whether to compute AROCt and AROCz for original or the bootstrapped values
                  if ind_repBS == 0:  # original
                        Count_EM = Count_EM_original
                        Count_OBS = Count_OBS_original
                  else:  # bootstrapped
                        NumDays = len(original_datesSTR_array)
                        datesBS_array = np.array(choices(population=original_datesSTR_array, k=NumDays)) # list of bootstrapped dates
                        indBS = np.searchsorted(original_datesSTR_array, datesBS_array) # indexes of the bootstrapped dates
                        Count_EM = Count_EM_original[indBS] # indexing the bootstrapped counts
                        Count_OBS = Count_OBS_original[indBS] # indexing the bootstrapped counts

                  # # Expand the list of lists into a unique array
                  # Count_EM = np.array(list(itertools.chain.from_iterable(Count_EM.tolist())))
                  # Count_OBS = np.array(list(itertools.chain.from_iterable(Count_OBS.tolist())))

                  # Computing AROCt
                  HR, FAR, AROCt = AROC_trapezoidal(Count_EM, Count_OBS, NumEM)
                  AROCt_array[indStepF, ind_repBS+1] = AROCt

            # Saving AROCt
            if ind == 0:
                  Name = "True"
            else:
                  Name = "Pseudo_" + str(Prob_Thr_list[ind-1])

      DirOUT_temp = Git_Repo + "/" + DirOUT + "/" + f"{Acc:02d}" + "h"
      FileNameOUT_temp = "AROC_" + f"{Acc:02d}" + "h_" + SystemFC + "_" + str(Perc_VRT) + "_" + Name
      if not os.path.exists(DirOUT_temp):
            os.makedirs(DirOUT_temp)
      np.save(DirOUT_temp + "/" + FileNameOUT_temp, AROCt_array)