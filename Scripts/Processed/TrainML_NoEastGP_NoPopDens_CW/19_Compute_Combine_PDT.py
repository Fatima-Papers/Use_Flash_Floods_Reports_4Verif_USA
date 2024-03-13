import os
import numpy as np
import metview as mv

###########################################################################
# CODE DESCRIPTION
# 19_Compute_Combine_PDT.py combines the training dataset (Point Data Table, PDT) for 
# each year to create the full required training dataset.
# Runtime: the code takes up to 5 minutes to combine training datasets for 25 years.

# INPUT PARAMETERS DESCRIPTION
# Year_S (integer, in YYYY format): start year to consider.
# Year_F (integer, in YYYY format): final year to consider.
# Specification_PDT (string): specification of the dataset (PDT) used  for training.
# Git_Repo (string): repository's local path.
# FileIN_Mask (string): relative path of the mask for which to extract the population density.
# DirIN (string): relative path containing the pdt for each year.
# DirOUT (string): relative path containing the combined pdt.

# INPUT PARAMETERS
Year_S = 2005
Year_F = 2020
Specification_PDT = "NoEastGP_NoPopDens_CW"
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
DirIN = "Data/Compute/18_PDT_Year"
DirOUT = "Data/Compute/19_Combine_PDT"
###########################################################################


# Defining the number of grid-points in the domain's mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask_lons = mv.longitudes(mask) - 360
mask_vals = mv.values(mask)
ind_domainGB = np.where(mask_vals == 1)[0]
NumGP_mask = ind_domainGB.shape[0]

# Masking the points to exclude in the training
mask_lons = mask_lons[ind_domainGB]
ind_lons_west =  np.where(mask_lons < -100)[0]

# Combining the pdts for each year
iter = 0
for Year in range(Year_S, Year_F+1):

      print("Combining year: " + str(Year))

      # Reading the pdt for specific years
      FileIN = Git_Repo + "/" + DirIN + "/pdt_" + str(Year) + ".npy"
      pdt_year = np.load(FileIN)
      NumGP_all = pdt_year.shape[0]
      
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
      tp_category = tp_category.reshape(-1, 1)
      
      # Concatenate the single elements by selecting only gridpoint in Western USA
      for i in range(0, NumGP_all, NumGP_mask):
            j = i + NumGP_mask -1
            temp_ff = ff_bin[i:j+1]
            temp_tp = tp_category[i:j+1]
            temp_ss = ss[i:j+1]
            temp_slor = slor[i:j+1]
            temp_stdor = stdor[i:j+1]

            pdt = np.concatenate((temp_ff[ind_lons_west], temp_tp[ind_lons_west], temp_ss[ind_lons_west], temp_slor[ind_lons_west], temp_stdor[ind_lons_west]), axis=1)
            
            if iter == 0:
                  pdt_all = pdt
            else:
                  pdt_all = np.vstack((pdt_all,pdt))
      
            iter = iter  + 1
      
# Removing the data points in which all rainfall values are less than a RP=1 year
ind_tp_greater_RP1 = np.where(pdt_all[:,1] != 0)[0]
pdt_all = pdt_all[ind_tp_greater_RP1,:]

# Remove all NaN in the dataset
rows_without_nan = ~np.isnan(pdt_all).any(axis=1)
pdt_all = pdt_all[rows_without_nan,:]

# Saving the final point data table
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
      os.makedirs(MainDirOUT)
FileOUT = MainDirOUT + "/pdt_" + Specification_PDT + "_" + str(Year_S) + "_" + str(Year_F)
np.save(FileOUT, pdt_all)