import os
import numpy as np
import matplotlib.pyplot as plt

###########################################################################
# CODE DESCRIPTION
# 20a_Plot_TrainML_Cost_Accuracy.py plots the cost of training different models, and their 
# correspondent accuracy. 
# Runtime: negligible.

# INPUT PARAMETERS DESCRIPTION
# Years_Train (string): years included in the training dataset.
# Specification_PDT (string): specification indicating which PDT was used  for training.
# Git_Repo (string): repository's local path
# FileIN (string): relative path containing the point data table.
# DirOUT (string): relative path containing the weights for the ML model.

# INPUT PARAMETERS
Years_Train = "2005_2020"
Specification_PDT = "AllRepFF_NoPopDens"
Architecture_list = ["1HL_4N", "2HL_4N", "2HL_8N", "3HL_8N", "3HL_16N"]
Architecture_colour_list = ["blue", "red", "green", "cyan", "orange"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
Dir = "Data/Compute/20_TrainML"
##########################################################################

# Plotting the accuracy of training and validation datasets in different ANN architectures
fig, ax = plt.subplots(figsize=(8, 6))
for ind in range(len(Architecture_list)):
      
      Architecture = Architecture_list[ind]
      Architecture_colour = Architecture_colour_list[ind]

      train_accuracy = np.load(Git_Repo + "/" + Dir + "/" + Specification_PDT + "_" + Years_Train + "/train_accuracy_" + Architecture + ".npy")
      validation_accuracy = np.load(Git_Repo + "/" + Dir + "/" + Specification_PDT + "_" + Years_Train + "/validation_accuracy_" + Architecture + ".npy")
      epochs = np.arange(len(train_accuracy))
      
      plt.plot(epochs, train_accuracy, "-o", color = Architecture_colour, label = Architecture)
      plt.plot(epochs, validation_accuracy, "--o", color = Architecture_colour, label = Architecture)

plt.title("Accuracy of training and validation datasets\n in different ANN architectures", fontsize=12, pad=5, weight = "bold")
plt.xlabel("Epochs", fontsize=12, labelpad = 5)
plt.ylabel("Accuracy [0 to 1]", fontsize=12, labelpad = 5)
plt.xlim(-1,25)
plt.ylim(0.9943, 0.9954)
plt.legend()
plt.savefig(Git_Repo + "/" + Dir + "/" + Specification_PDT + "_" + Years_Train + "/accuracy")
plt.close()

# Plotting the time spent in training different ANN architectures
fig, ax = plt.subplots(figsize=(8, 6))
for ind in range(len(Architecture_list)):
      
      Architecture = Architecture_list[ind]
      Architecture_colour = Architecture_colour_list[ind]

      train_time = np.load(Git_Repo + "/" + Dir + "/" + Specification_PDT + "_" + Years_Train + "/train_time_" + Architecture + ".npy")
      epochs = np.arange(len(train_time))
      
      plt.plot(epochs, train_time, "-o", color = Architecture_colour, label = Architecture)

plt.title("Time spent in training different ANN architectures", fontsize=14, pad=5, weight = "bold")
plt.xlabel("Epochs", fontsize=12, labelpad = 5)
plt.ylabel("Time [seconds]", fontsize=12, labelpad = 5)
plt.xlim(-1,25)
plt.ylim(105, 135)
plt.legend()
plt.savefig(Git_Repo + "/" + Dir + "/" + Specification_PDT + "_" + Years_Train + "/time")