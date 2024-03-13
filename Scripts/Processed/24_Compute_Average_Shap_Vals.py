import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv
import matplotlib.pyplot as plt

###########################################################################
# CODE DESCRIPTION
# 24_Compute_Average_Shap_Vals.py computes the average of shap values for the different predictors.
# Runtime: the script can take up to 1 hour to run in serial.

# INPUT PARAMETERS DESCRIPTION
# DateTime_Start_S (date and time): start date (first three numbers) and time (fourth number) for the analysis period (representing the beginning of the accumulation period).
# DateTime_Start_F (date and time): final date (first three numbers) and time (fourth number) for the analysis period (representing the beginning of the accumulation period).
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# Years_Train (string): years covered in the training dataset.
# Specification_PDT (string): specification of the dataset (PDT) used  for training.
# Git_Repo (string): repository's local path
# DirIN_ML (string): relative path of the directory containg the weights for the ML model.
# DirOUT (string): relative path containing the ML predictions.

# INPUT PARAMETERS
DateTime_Final_S = datetime(2021,1,1,12)
DateTime_Final_F = datetime(2021,12,31,12)
Acc = 12
Disc_Acc = 12
Mask_Domain = [22,-130,52,-60]
Perc_list = [99.8, 99.9, 99.95, 99.98, 99.99]
RP_list = [1,2,5,10,20]
Years_Train = "2005_2020"
Specification_PDT_list = ["AllRepFF_NoPopDens", "AllRepFF_AllPredictors"]
Predictors_array_list = [["Total Precipitation", "Percentage of Soil Mosture", "Slope of the Sub-Grid Orography", "Standard Deviation of the Sub-Grid Orography"], ["Total Precipitation", "Percentage of Soil Saturation", "Slope of the Sub-Grid Orography", "Standard Deviation of the Sub-Grid Orography", "Population Density"]]
PredSymb_array_list = [["tp", "ss", "slor", "stdor"], ["tp", "ss", "slor", "stdor", "pd"]]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
DirIN_RainThr = "Data/Raw/Analysis/ERA5_ecPoint/tp_climate"
DirIN_Rain = "Data/Raw/Analysis/ERA5_ecPoint/tp"
DirIN = "Data/Compute/21_Predict_RepFF"
DirOUT = "Data/Plot/24_Average_Shap_Vals"
#############################################################################


# Definition of general parameters
Num_Periods = ((DateTime_Final_F - DateTime_Final_S).days + 1 ) * (24/Disc_Acc)
Num_tp_cat = len(RP_list)

# Reading domain's mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask_lats = mv.latitudes(mask)
mask_lons = mv.longitudes(mask)
mask_vals = mv.values(mask)
mask_index = np.where(mask_vals == 1)[0]
mask_lats = mask_lats[mask_index]
mask_lons = mask_lons[mask_index]

# Computing the average of shap values for the different predictors
for ind in range(len(Specification_PDT_list)):

      Specification_PDT = Specification_PDT_list[ind]
      Predictors_array = Predictors_array_list[ind]
      PredSymb_array = PredSymb_array_list[ind]
      Num_Pred = len(Predictors_array)
      
      Training_Dataset = Specification_PDT + "_" + Years_Train

      print()
      print("Computing the average of shap values for the predictors in the training dataset: " + Training_Dataset)

      # Initialization of the variable that will store all the required mean shap values
      mean_shap_vals = np.zeros((int(Num_Periods), int(Num_Pred), int(Num_tp_cat) + 1))
      
      # Computing the mean shap values for different conditions
      TheDateTime_Final = DateTime_Final_S
      ind_day = 0
      while TheDateTime_Final <= DateTime_Final_F:
            
            print(" - " + TheDateTime_Final.strftime("%Y%m%d%H"))
            FileIN = Git_Repo + "/" + DirIN + "/" + Training_Dataset + "/Shap_Vals_" +  TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
            shap = mv.nearest_gridpoint(mv.read(FileIN), mask_lats, mask_lons)
            
            #########################################################
            # Computing the mean shap values over all the points in the domain #
            #########################################################

            temp_shap_vals = np.nanmean(np.absolute(shap), axis=1)
            mean_shap_vals[ind_day, :, 0] = temp_shap_vals

            #####################################################
            # Computing the mean shap values over different tp categories #
            #####################################################

            # Reading the rainfall analysis and categorizing it climatologically, and extracting the nearest values to the mask grid-points 
            if TheDateTime_Final.strftime("%H") == 0:
                  TheDate = TheDateTime_Final - timedelta(days=1)
                  EndPeriod = "24"
            else:
                  TheDate = TheDateTime_Final
                  EndPeriod = "12"
            FileIN_Rain = Git_Repo + "/" + DirIN_Rain + "/" + TheDate.strftime("%Y%m") + "/Pt_BC_PERC_" + TheDate.strftime("%Y%m%d") + "_" + f"{EndPeriod:02}" + ".grib2"
            tp = mv.read(FileIN_Rain)[-1]
            tp_mask = mv.nearest_gridpoint(tp, mask_lats, mask_lons).reshape(-1, 1)

            tp_climate = mv.read(Git_Repo + "/" + DirIN_RainThr + "/tp_climate_12h_ERA5_ecPoint.grib")
            percs = np.load(Git_Repo + "/" + DirIN_RainThr + "/percs_computed_4_tp_climate.npy")
            
            tp_cat_mask = np.zeros(tp_mask.shape)
            for i in range(len(Perc_list)):
                  if i < len(Perc_list)-1:
                        Perc1 = Perc_list[i]
                        Perc2 = Perc_list[i+1]
                        RP = RP_list[i]
                        ind_perc1 = np.where(percs == Perc1)[0]
                        ind_perc2 = np.where(percs == Perc2)[0]
                        tp_thr1 = mv.nearest_gridpoint(tp_climate[ind_perc1], mask_lats, mask_lons).reshape(-1, 1)
                        tp_thr2 = mv.nearest_gridpoint(tp_climate[ind_perc2], mask_lats, mask_lons).reshape(-1, 1)
                        ind = np.where((tp_mask>=tp_thr1) & (tp_mask<tp_thr2))[0]
                        tp_cat_mask[ind] = RP
                  else:
                        Perc = Perc_list[i]
                        RP = RP_list[i]
                        ind_perc = np.where(percs == Perc)[0]
                        tp_thr = mv.nearest_gridpoint(tp_climate[ind_perc], mask_lats, mask_lons).reshape(-1, 1)
                        ind = np.where(tp_mask>=tp_thr)[0]
                        tp_cat_mask[ind] = RP 
            
            # Read the shap values and select those for the specific rainfall categories
            ind_RP = 1
            for RP in RP_list:
                  ind_tp = np.where(tp_cat_mask == RP)[0]
                  if len(ind_tp) != 0:
                        shap_tp = shap[:, ind_tp]
                        temp_shap_vals = np.nanmean(np.absolute(shap_tp), axis=1)
                        mean_shap_vals[ind_day, :, ind_RP] = temp_shap_vals
                  ind_RP = ind_RP + 1

            ind_day = ind_day + 1
            
            TheDateTime_Final = TheDateTime_Final + timedelta(hours=Disc_Acc)

      mean_shap_vals = np.nanmean(mean_shap_vals, axis = 0) * 100

      for ind in range(int(Num_tp_cat) + 1):
            if ind == 0:
                  plt.title("Shap values for predictors in " + Training_Dataset + "\nfor all points in the domain", pad=10, weight="bold")
                  FileName = "All"
            else:
                  plt.title("Shap values for predictors in " + Training_Dataset + "\nfor tp>RP=" + str(RP_list[ind-1]), pad=10, weight="bold")
                  FileName = str(RP_list[ind-1])
            plt.bar(PredSymb_array, mean_shap_vals[:,ind], color="deeppink")
            plt.xlabel("Predictors")
            plt.ylabel("Shap values [%]")
            plt.ylim(0,1)

            # Saving the plots
            MainDirOUT = Git_Repo + "/" + DirOUT
            if not os.path.exists(MainDirOUT):
                  os.makedirs(MainDirOUT)
            FileOUT = MainDirOUT + "/Mean_Shap_Vals_" + Training_Dataset + "_" + FileName + ".png"
            plt.savefig(FileOUT, dpi=1000)