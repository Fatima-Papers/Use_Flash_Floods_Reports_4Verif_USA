import os
import numpy as np
import metview as mv

##################################################################################################
# CODE DESCRIPTION
# 19_Compute_Combine_PDT.py combines the training dataset (Point Data Table, PDT) for each year to create the full 
# required training dataset.
# Runtime: the code takes up to 20 minutes to combine training datasets for 15 years in serial for all reductions.

# INPUT PARAMETERS DESCRIPTION
# Year_S (integer, in YYYY format): start year to consider.
# Year_F (integer, in YYYY format): final year to consider.
# Perc_RedFF_list (list of floats, from o to 1): list of percentages for the reduction of flood reports in the training dataset. 
# Specification_PDT (string): specification of the dataset (PDT) used  for training.
# Git_Repo (string): repository's local path.
# DirIN (string): relative path containing the pdt for each year.
# DirOUT (string): relative path containing the combined pdt.

# INPUT PARAMETERS
Year_S = 2005
Year_F = 2020
Perc_RedFF_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
Specification_PDT = "GradRedFF_NoPopDens"
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
DirIN = "Data/Compute/18_PDT_Year"
DirOUT = "Data/Compute/19_Combine_PDT"
##################################################################################################


# Defining the number of grid-points in the domain's mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask_lons = mv.longitudes(mask) - 360
mask_vals = mv.values(mask)
ind_domainGB = np.where(mask_vals == 1)[0]
NumGP_mask = ind_domainGB.shape[0]

# Initialize the variable that will contained the combined pdt
pdt_all = np.array([])

# Reducing randomly and gradually the number of flash flood reports in the dataset
for Perc_RedFF in Perc_RedFF_list:

      print()
      print("Creating reduced training dataset of: " + str(int(Perc_RedFF*100)) + "%")

      # Combining the pdts for each year
      for Year in range(Year_S, Year_F+1):

            print(" - Combining year: " + str(Year))

            # Reading the pdt for specific years
            FileIN = Git_Repo + "/" + DirIN + "/pdt_" + str(Year) + ".npy"
            pdt_year = np.load(FileIN)
            NumGP_all = pdt_year.shape[0]
            
            # Removing all the flood reports from the area to exclude
            for i in range(0, NumGP_all+1, NumGP_mask):
                  j = i + NumGP_mask -1
                  temp = pdt_year[i:j+1,0]
                  ind_ff = np.where(temp == 1)[0]
                  num_red_ff = ind_ff.shape[0] * Perc_RedFF
                  num_red_ff = np.floor(num_red_ff)
                  if num_red_ff > 0:
                        ind_random_red_ff = np.random.choice(ind_ff, size=int(num_red_ff), replace=False)
                        temp[ind_random_red_ff] = 0
                        pdt_year[i:j+1,0] = temp

            # Converting the counts of ff in each grid-box into a binary category (i.e., 0s and 1s)
            ff_bin = np.where(pdt_year[:,0] > 0, 1, 0).reshape(-1, 1)

            # Extracting the slor values
            slor = pdt_year[:,1].reshape(-1, 1)

            # Extracting the stdor values
            stdor = pdt_year[:,2].reshape(-1, 1)

            # Extracting the ss values
            ss = pdt_year[:,4].reshape(-1, 1)

            # Assessing how extreme is the rainfall near the flash flood reports
            tp_thr1 = pdt_year[:,5]
            tp_thr2 = pdt_year[:,6]
            tp_thr5 = pdt_year[:,7]
            tp_thr10 = pdt_year[:,8]
            tp_thr20 = pdt_year[:,9]
            tp_max = pdt_year[:,-1]
            
            ind_1_2 = np.where((tp_max>=tp_thr1) & (tp_max<tp_thr2))[0]
            ind_2_5 = np.where((tp_max>=tp_thr2) & (tp_max<tp_thr5))[0]
            ind_5_10 = np.where((tp_max>=tp_thr5) & (tp_max<tp_thr10))[0]
            ind_10_20 = np.where((tp_max>=tp_thr10) & (tp_max<tp_thr20))[0]
            ind_20 = np.where((tp_max>=tp_thr20))[0]
            
            tp_category = tp_max * 0
            tp_category[ind_1_2] = 1
            tp_category[ind_2_5] = 2
            tp_category[ind_5_10] = 5
            tp_category[ind_10_20] = 10
            tp_category[ind_20] = 20
            
            # Removing the data points in which all rainfall values are less than a RP=1 year
            ind_tp = np.where(tp_category != 0)[0]
            tp_category = tp_category.reshape(-1, 1)
            
            # Concatenate the single elements
            pdt = np.concatenate((ff_bin, tp_category, ss, slor, stdor), axis=1)
            pdt = pdt[ind_tp,:]
            if Year == Year_S:
                  pdt_all = pdt
            else:
                  pdt_all = np.vstack((pdt_all,pdt))

      # Remove all NaN in the dataset
      rows_without_nan = ~np.isnan(pdt_all).any(axis=1)
      pdt_all = pdt_all[rows_without_nan]

      # Printing the number of retained flood reports
      ind_repFF = np.where(pdt_all[:,0] == 1)[0]
      print(" - Number of retained flood reports = " + str(ind_repFF.shape[0]))

      # Saving the final point data table
      MainDirOUT = Git_Repo + "/" + DirOUT
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      FileOUT = MainDirOUT + "/pdt_" + Specification_PDT + "_" + str(int(Perc_RedFF*100)) + "_" + str(Year_S) + "_" + str(Year_F)
      np.save(FileOUT, pdt_all)