import os
import numpy as np
import matplotlib.pyplot as plt

###########################################################################
# CODE DESCRIPTION
# 11_Compute_Exploring_PDT.py explores the content of the considered point data table.
# Runtime: negligible

# INPUT PARAMETERS DESCRIPTION
# Years_training (string): years covered in the training dataset.
# Git_Repo (string): repository's local path
# DirIN (string): relative path containing the point data table.
# DirOUT (string): relative path containing the exploratory distributions.

# INPUT PARAMETERS
Years_training = "1996_2020"
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Compute/10_Combine_PDT"
DirOUT = "Data/Compute/11_Exploring_PDT"
###########################################################################

# Reading the training and test point data tables
FileIN_training = Git_Repo + "/" + DirIN + "/pdt_" + Years_training + ".npy"
pdt = np.load(FileIN_training)
num_ff = pdt.shape[0]

print(np.unique(pdt[:,1]))
exit()

# Percentage of yes- and no- events over all cases
ind_ff_0 = np.where(pdt[:,0] == 0)[0]
num_ff_0 = ind_ff_0.shape[0]
ind_ff_1 = np.where(pdt[:,0] == 1)[0]
num_ff_1 = ind_ff_1.shape[0]
print(num_ff_0/num_ff*100)
print(num_ff_1/num_ff*100)

# Create a distribution of the values in each predictors
tp = pdt[:,1]
plt.hist(tp, bins=np.arange(0,22.5,1), width=0.9, density=True)      
plt.title("Distribution of rainfall categories")
plt.xlabel("Return Period [years]")
plt.ylabel("Relative frequency")
#plt.xticks([1,2,5,10,20])
plt.show()
exit()

ss = pdt[:,2]
plt.hist(ss, bins=np.arange(0,1.2,0.1), width=0.09)      
plt.title("Distribution of percentage of soil saturation")
plt.xlabel("Percentage [%]")
plt.ylabel("Absolute frequency")
plt.xticks(np.arange(0,1.1,0.1))
plt.close()

slor = pdt[:,3]
plt.hist(slor, bins=np.arange(-0.005,0.21,0.01), width=0.009)      
plt.title("Distribution of orography slopes")
plt.xlabel("Slope [-]")
plt.ylabel("Absolute frequency")
plt.close()

# Defining how the percentage of yes-events (flash floods) changes over different classes of predictors
tp_class = np.array([0,1,2,5,10,20,100])
ss_class = np.arange(0,1.1,0.1)
slor_class = np.arange(0,0.21,0.01)

hist = []
data = pdt[:,1]
data_class = tp_class
for ind_tp in range(len(data_class)-1):
      i = data_class[ind_tp]
      j = data_class[ind_tp+1]
      index = np.where( (data >= i) & (data < j))[0]
      pdt_temp = pdt[index,:]
      num_ff_temp = pdt_temp.shape[0]
      ind_ff_1 = np.where(pdt_temp[:,0] == 1)[0]
      num_ff_1 = ind_ff_1.shape[0]
      hist.append(num_ff_1/num_ff_temp*100)
plt.bar(data_class[:-1], hist)
plt.title("Percentage of yes-events")
plt.xlabel("Return Period [years]")
plt.ylabel("Relative frequency")
plt.xticks([0,1,2,5,10,20])
plt.close()

hist = []
data = pdt[:,2]
data_class = ss_class
for ind in range(len(data_class)-1):
      i = data_class[ind]
      j = data_class[ind+1]
      index = np.where( (data >= i) & (data < j))[0]
      pdt_temp = pdt[index,:]
      num_ff_temp = pdt_temp.shape[0]
      ind_ff_1 = np.where(pdt_temp[:,0] == 1)[0]
      num_ff_1 = ind_ff_1.shape[0]
      hist.append(num_ff_1/num_ff_temp*100)
plt.bar(data_class[:-1], hist, width=0.09)
plt.title("Percentage of yes-events - Percentage Soil Saturation")
plt.xlabel("Percentage [%]")
plt.ylabel("Absolute frequency")
plt.xticks(np.arange(0,1.1,0.1))
plt.show()
