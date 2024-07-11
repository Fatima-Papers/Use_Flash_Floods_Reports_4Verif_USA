import os
import numpy as np
import matplotlib.pyplot as plt

##########################################################################################################
# CODE DESCRIPTION
# 27c_Plot_Definition_Topology_ANN.py compares the accuracy for training and validation datases and the training time per epoch 
# as a function of the number of epochs used during training. The different topologies have been computed by changing manually  
# the neural network in the file "27_Compute_Train_ANN.py".
# Runtime: negligible.

# INPUT PARAMETERS DESCRIPTION
# Num_HL_N_list (list of strings): combination to consider for the number of hidden layers and neurons in each hidden layer.
# Colour_list (list of strings): colour to consider for each combination of number of hidden layers and neurons in each hidden layer.
# Git_Repo (string): repository's local path.
# DirIN (string): relative path of the directory containg the different ANN's topologies. 
# DirOUT (string): relative path of the directory containing the lines plots comparing the different ANN's topologies. 

# INPUT PARAMETERS
Num_HL_N_list = ["1HL_4N", "1HL_8N", "2HL_8N_8N", "3HL_4N_4N_4N", "3HL_8N_8N_8N", "4HL_4N_4N_4N_4N", "4HL_8N_8N_8N_8N", "2HL_8N_4N", "2HL_4N_4N"]
Colour_list = ["chocolate", "olive", "forestgreen", "palegreen", "purple", "slateblue", "deepskyblue", "mediumblue", "crimson"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Compute/27_Train_ANN/AllFF_2005_2020/NoPD"
DirOUT = "Data/Plot/27c_Plot_Definition_Topology_ANN/AllFF_2005_2020/NoPD"
##########################################################################################################


# Setting the main output directory
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
      os.makedirs(MainDirOUT)

# Plotting the accuracy for the training dataset (full)
for ind in range(len(Num_HL_N_list)):
      Num_HL_N = Num_HL_N_list[ind]
      Colour = Colour_list[ind]
      accuracy_training = np.load(Git_Repo + "/" + DirIN + "/" + Num_HL_N + "_train_accuracy.npy")
      x = np.arange(len(accuracy_training))
      plt.plot(x, accuracy_training, "-", color=Colour, linewidth=2, label=Num_HL_N)
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="y", colors="#36454F")
plt.tick_params(left=False, right=False, top=False)
plt.grid(axis="y", color="silver", linewidth=0.5)
plt.xlim([-0.2,25.2])
ax.set_ylim(bottom = 0.99045)
FileOUT = MainDirOUT + "/" + "train_accuracy.jpeg"
plt.savefig(FileOUT, format="jpeg", bbox_inches="tight", dpi=1000)
plt.close()

# Plotting the accuracy for the validation dataset
for ind in range(len(Num_HL_N_list)):
      Num_HL_N = Num_HL_N_list[ind]
      Colour = Colour_list[ind]
      accuracy_validation = np.load(Git_Repo + "/" + DirIN + "/" + Num_HL_N + "_validation_accuracy.npy")
      x = np.arange(len(accuracy_validation))
      plt.plot(x, accuracy_validation, "-", color=Colour, linewidth=2, label=Num_HL_N)
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="y", colors="#36454F")
plt.tick_params(left=False, right=False, top=False)
plt.grid(axis="y", color="silver", linewidth=0.5)
plt.xlim([-0.2,25.2])
ax.set_ylim(bottom = 0.98907)
FileOUT = MainDirOUT + "/" + "validation_accuracy.jpeg"
plt.savefig(FileOUT, format="jpeg", bbox_inches="tight", dpi=1000)
plt.close()

# Plotting the training time per epoch
for ind in range(len(Num_HL_N_list)):
      Num_HL_N = Num_HL_N_list[ind]
      Colour = Colour_list[ind]
      time_train_epoch = np.load(Git_Repo + "/" + DirIN + "/" + Num_HL_N + "_train_time.npy")
      x = np.arange(len(time_train_epoch))
      plt.plot(x, time_train_epoch, "-", color=Colour, linewidth=2, label=Num_HL_N)
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(axis="y", colors="#36454F")
plt.tick_params(left=False, right=False, top=False)
plt.grid(axis="y", color="silver", linewidth=0.5)
plt.xlim([-0.2,25.2])
plt.ylim([48,66])
plt.yticks(np.arange(48,66,4))
ax.set_ylim(bottom = 46)
FileOUT = MainDirOUT + "/" + "train_time_epoch.jpeg"
plt.savefig(FileOUT, format="jpeg", bbox_inches="tight", dpi=1000)
plt.close()