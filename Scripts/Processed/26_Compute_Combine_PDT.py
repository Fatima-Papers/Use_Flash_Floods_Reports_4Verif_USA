import os
import sys
import numpy as np
import metview as mv

####################################################################################################################################
# CODE DESCRIPTION
# 26_Compute_Combine_PDT.py combines the year training dataset (Point Data Table, PDT) to create the full required training dataset.
# Runtime: the code can take up to 15 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year_S (integer, in YYYY format): start year to consider.
# Year_F (integer, in YYYY format): final year to consider.
# Type_ReductionFF (string): type of reduction of flash flood reports. Valid values are "AllFF", "FF", "GP", and "RedRndFF".
# Name_Region (string): name of the region to consider int he reduction of flash flood reports. Valid values are "North", "South", "West", and "East".
# North_South_LatBoundary (integer, from -90 to +90): value of the latitude boundary that separates north from south.
# West_East_LonBoundary (integer, from -180 to +180): value of the longitude boundary that separates west from east.
# NamePred (list of strings): list containing the name of the considered predictors.
# Pred2Keep (list of booleans): list containing the values "True" if the correspondent predictor is to be included in the PDT, and "False" otherwise.
# Perc_RedFF_list (list of integers from 0 to 100): list of percentages to consider to reduce the number of flash flood reports when "Type_ReductionFF=RedRndFF".
# Git_Repo (string): repository's local path.
# FileIN_Mask (string): relative path of the file containing the domain's mask.
# DirIN (string): relative path of the directory containing the pdt for each year.
# DirOUT (string): relative path of the directory containing the combined pdt.

# INPUT PARAMETERS
Year_S = sys.argv[1]
Year_F = sys.argv[2]
Type_ReductionFF = sys.argv[3]
Name_Region = sys.argv[4]
North_South_LatBoundary = sys.argv[5]
West_East_LonBoundary = sys.argv[6]
NamePred = sys.argv[7]
Pred2Keep = sys.argv[8]
Perc_RedFF_list = sys.argv[9]
Repetitions_RedFF = sys.argv[10]
Git_Repo = sys.argv[11]
FileIN_Mask = sys.argv[12]
DirIN = sys.argv[13]
DirOUT = sys.argv[14]
####################################################################################################################################


####################
# CUSTOM FUNCTIONS #
####################

# Function to remove all the flash flood reports in the considered region from the pdt
def Exclude_FF(pdt, ind_reg):

      numGP_pdt = pdt.shape[0]
      for i in range(0, numGP_pdt, numGP_mask):
            j = i + numGP_mask -1
            temp = pdt[i:j+1,0]
            temp[ind_reg] = 0
            pdt[i:j+1,0] = temp

      return pdt


# Function to remove all the grid-points in the considered region from the pdt
def Exclude_GP(pdt, ind_reg):

      iter = 0
      numGP_pdt = pdt.shape[0]
      for i in range(0, numGP_pdt, numGP_mask):
            j = i + numGP_mask -1
            temp = pdt[i:j+1,:]
            ind_reg2rem = ~np.in1d(np.arange(temp.shape[0]), ind_reg)
            temp_red = temp[ind_reg2rem]
            if iter == 0:
                  pdt_reduced = temp_red
            else:
                  pdt_reduced = np.vstack((pdt_reduced, temp_red))
            iter = iter + 1
      
      return pdt_reduced


# Function to reduce randomly the number of flash flood reports from the pdt
def Reduce_RandomFF(pdt, Perc_RedFF):

      numGP_pdt = pdt.shape[0]
      for i in range(0, numGP_pdt, numGP_mask):
            j = i + numGP_mask -1
            temp = pdt[i:j+1,0]
            ind_ff = np.where(temp == 1)[0]
            num_red_ff = np.ceil(ind_ff.shape[0] * (Perc_RedFF/100)) # approximates toward the closest biggest integer
            if num_red_ff > 0:
                  ind_random_red_ff = np.random.choice(ind_ff, size=int(num_red_ff), replace=False)
                  temp[ind_random_red_ff] = 0
                  pdt[i:j+1,0] = temp

      return pdt
############################################################################################################################


print()
print("Merging the yearly PDTs. Considering year:")

# Converting the input variables to the required format
Year_S = int(Year_S)
Year_F = int(Year_F)
North_South_LatBoundary = int(North_South_LatBoundary)
West_East_LonBoundary = int(West_East_LonBoundary)
NamePred = NamePred.split(",")
Pred2Keep = Pred2Keep.split(",")
Pred2Keep = [item == 'True' for item in Pred2Keep]
Perc_RedFF_list = Perc_RedFF_list.split(",")
Perc_RedFF_list = [int(item) for item in Perc_RedFF_list]
Repetitions_RedFF = int(Repetitions_RedFF)

# Defining latitudes, longitudes, and number of grid-points in the considered domain
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
ind_mask = np.where(mv.values(mask) == 1)[0]
lats_mask = mv.latitudes(mask)[ind_mask]
lons_mask = (mv.longitudes(mask) - 360)[ind_mask]
numGP_mask = ind_mask.shape[0]

# Determining the region to consider
if Name_Region == "North":
      ind_reg =  np.where(lats_mask >= North_South_LatBoundary)[0]
elif Name_Region == "South":
      ind_reg =  np.where(lats_mask < North_South_LatBoundary)[0]
elif Name_Region == "West":
      ind_reg =  np.where(lons_mask < West_East_LonBoundary)[0]
elif Name_Region == "East":
      ind_reg =  np.where(lons_mask >= West_East_LonBoundary)[0]

# Defining the name of the PDT
if np.sum(Pred2Keep) == len(Pred2Keep):
      NamePDT_2 = "AllPred"
else:
      NamePDT_2 = ""
      for ind_Pred in range(1,len(NamePred)):
            if Pred2Keep[ind_Pred] == False:
                  NamePDT_2 = NamePDT_2 + "No" + NamePred[ind_Pred]


# Merging the yearly PDTs
if Type_ReductionFF == "FF":
      
      NamePDT_1 = "No" + Name_Region + Type_ReductionFF
      iter = 0
      pdt_all = np.array([]) # initializing the variable that will contained the merged yearly PDTs
      for Year in range(Year_S, Year_F+1):

            print(" - " + str(Year))

            # Reading the pdt for specific years
            FileIN = Git_Repo + "/" + DirIN + "/pdt_" + str(Year) + ".npy"
            pdt_year = np.load(FileIN)

            # Removing predictors from the PDT
            Pred2Keep.insert(0, True) # adding the column that correspond to the predictand, i.e. the flash flood reports, that it is always set to "True"
            pdt_year = pdt_year[:,Pred2Keep]
            
            pdt_temp = Exclude_FF(pdt_year, ind_reg)

            # Converting the counts of point flash flood reports in each grid-box into a binary value (i.e., 0 when there are no reports in the grid-box and 1 when there is at least one report)
            pdt_temp[:,0] = np.where(pdt_temp[:,0] > 0, 1, 0)
      
            # Removing data points with return period class less than a 1 year
            rows_ClassRP_gt0 = np.where(pdt_temp[:,2] != 0)[0]
            pdt_temp = pdt_temp[rows_ClassRP_gt0,:]

            # Removing rows containing NaN values in one or more columns
            rows_without_nan = ~np.isnan(pdt_temp).any(axis=1)
            pdt_temp = pdt_temp[rows_without_nan]

            # Merging the yearly PDT
            if iter == 0:
                  pdt_all = pdt_temp
            else:
                  pdt_all = np.vstack((pdt_all, pdt_temp))

            iter = iter  + 1
            Pred2Keep = Pred2Keep[1::]

      # Saving the merged PDT for all considered years
      Specification_PDT = NamePDT_1 + "_" + NamePDT_2
      MainDirOUT = Git_Repo + "/" + DirOUT + "/" + NamePDT_1
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      FileOUT = MainDirOUT + "/pdt_" + Specification_PDT + "_" + str(Year_S) + "_" + str(Year_F)
      np.save(FileOUT, pdt_all)

elif Type_ReductionFF == "GP":
      
      NamePDT_1 = "No" + Name_Region + Type_ReductionFF
      iter = 0
      pdt_all = np.array([]) # initializing the variable that will contained the merged yearly PDTs
      for Year in range(Year_S, Year_F+1):

            print(" - " + str(Year))

            # Reading the pdt for specific years
            FileIN = Git_Repo + "/" + DirIN + "/pdt_" + str(Year) + ".npy"
            pdt_year = np.load(FileIN)

            # Removing predictors from the PDT
            Pred2Keep.insert(0, True) # adding the column that correspond to the predictand, i.e. the flash flood reports, that it is always set to "True"
            pdt_year = pdt_year[:,Pred2Keep]

            pdt_temp = Exclude_GP(pdt_year, ind_reg)

            # Converting the counts of point flash flood reports in each grid-box into a binary value (i.e., 0 when there are no reports in the grid-box and 1 when there is at least one report)
            pdt_temp[:,0] = np.where(pdt_temp[:,0] > 0, 1, 0)
      
            # Removing data points with return period class less than a 1 year
            rows_ClassRP_gt0 = np.where(pdt_temp[:,2] != 0)[0]
            pdt_temp = pdt_temp[rows_ClassRP_gt0,:]

            # Removing rows containing NaN values in one or more columns
            rows_without_nan = ~np.isnan(pdt_temp).any(axis=1)
            pdt_temp = pdt_temp[rows_without_nan]

            # Merging the yearly PDT
            if iter == 0:
                  pdt_all = pdt_temp
            else:
                  pdt_all = np.vstack((pdt_all, pdt_temp))

            iter = iter  + 1
            Pred2Keep = Pred2Keep[1::]

      # Saving the merged PDT for all considered years
      Specification_PDT = NamePDT_1 + "_" + NamePDT_2
      MainDirOUT = Git_Repo + "/" + DirOUT + "/" + NamePDT_1
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      FileOUT = MainDirOUT + "/pdt_" + Specification_PDT + "_" + str(Year_S) + "_" + str(Year_F)
      np.save(FileOUT, pdt_all)

elif Type_ReductionFF == "RedRndFF":
      
      if Repetitions_RedFF <= 10:
            NumDigStr = 1
      elif Repetitions_RedFF <= 100:
            NumDigStr = 2
      elif Repetitions_RedFF <= 1000:
            NumDigStr = 3
      else:
            NumDigStr = 4

      for indRep in range(Repetitions_RedFF):
            
            for Perc_RedFF in Perc_RedFF_list:
                  
                  iter = 0
                  pdt_all = np.array([]) # initializing the variable that will contained the merged yearly PDTs
                  a = 0
                  b = 0
                  for Year in range(Year_S, Year_F+1):

                        print(" - " + str(Year))

                        # Reading the pdt for specific years
                        FileIN = Git_Repo + "/" + DirIN + "/pdt_" + str(Year) + ".npy"
                        pdt_year = np.load(FileIN)

                        # Removing predictors from the PDT
                        Pred2Keep.insert(0, True) # adding the column that correspond to the predictand, i.e. the flash flood reports, that it is always set to "True"
                        pdt_year = pdt_year[:,Pred2Keep]
                        a = a + np.nansum(pdt_year[:,0])

                        # Reducing the number of flash flood reports
                        pdt_temp = Reduce_RandomFF(pdt_year, Perc_RedFF)
                        b = b + np.nansum(pdt_temp[:,0])
                        NamePDT_1 = Type_ReductionFF + "_" + f"{Perc_RedFF:02}" + "_" + f"{indRep:0{NumDigStr}}"

                        # Converting the counts of point flash flood reports in each grid-box into a binary value (i.e., 0 when there are no reports in the grid-box and 1 when there is at least one report)
                        pdt_temp[:,0] = np.where(pdt_temp[:,0] > 0, 1, 0)
                  
                        # Removing data points with return period class less than a 1 year
                        rows_ClassRP_gt0 = np.where(pdt_temp[:,2] != 0)[0]
                        pdt_temp = pdt_temp[rows_ClassRP_gt0,:]

                        # Removing rows containing NaN values in one or more columns
                        rows_without_nan = ~np.isnan(pdt_temp).any(axis=1)
                        pdt_temp = pdt_temp[rows_without_nan]

                        # Merging the yearly PDT
                        if iter == 0:
                              pdt_all = pdt_temp
                        else:
                              pdt_all = np.vstack((pdt_all, pdt_temp))

                        iter = iter  + 1
                        Pred2Keep = Pred2Keep[1::]
                  
                  print(a,b)

                  # Saving the merged PDT for all considered years
                  Specification_PDT = NamePDT_1 + "_" + NamePDT_2 
                  MainDirOUT = Git_Repo + "/" + DirOUT + "/" + Type_ReductionFF
                  if not os.path.exists(MainDirOUT):
                        os.makedirs(MainDirOUT)
                  FileOUT = MainDirOUT + "/pdt_" + Specification_PDT + "_" + str(Year_S) + "_" + str(Year_F)
                  np.save(FileOUT, pdt_all)

else:
      
      NamePDT_1 = "AllFF"
      iter = 0
      pdt_all = np.array([]) # initializing the variable that will contained the merged yearly PDTs
      for Year in range(Year_S, Year_F+1):

            print(" - " + str(Year))

            # Reading the pdt for specific years
            FileIN = Git_Repo + "/" + DirIN + "/pdt_" + str(Year) + ".npy"
            pdt_year = np.load(FileIN)

            # Removing predictors from the PDT
            Pred2Keep.insert(0, True) # adding the column that correspond to the predictand, i.e. the flash flood reports, that it is always set to "True"
            pdt_year = pdt_year[:,Pred2Keep]
            
            pdt_temp = pdt_year

            # Converting the counts of point flash flood reports in each grid-box into a binary value (i.e., 0 when there are no reports in the grid-box and 1 when there is at least one report)
            pdt_temp[:,0] = np.where(pdt_temp[:,0] > 0, 1, 0)
      
            # Removing data points with return period class less than a 1 year
            rows_ClassRP_gt0 = np.where(pdt_temp[:,2] != 0)[0]
            pdt_temp = pdt_temp[rows_ClassRP_gt0,:]

            # Removing rows containing NaN values in one or more columns
            rows_without_nan = ~np.isnan(pdt_temp).any(axis=1)
            pdt_temp = pdt_temp[rows_without_nan]

            # Merging the yearly PDT
            if iter == 0:
                  pdt_all = pdt_temp
            else:
                  pdt_all = np.vstack((pdt_all, pdt_temp))

            iter = iter  + 1
            Pred2Keep = Pred2Keep[1::]

      # Saving the merged PDT for all considered years
      Specification_PDT = NamePDT_1 + "_" + NamePDT_2
      MainDirOUT = Git_Repo + "/" + DirOUT + "/" + Type_ReductionFF
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      FileOUT = MainDirOUT + "/pdt_" + Specification_PDT + "_" + str(Year_S) + "_" + str(Year_F)
      np.save(FileOUT, pdt_all)
