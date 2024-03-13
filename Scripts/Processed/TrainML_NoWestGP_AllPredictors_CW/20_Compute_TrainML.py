import os
import numpy as np
import tensorflow as tf

###########################################################################
# CODE DESCRIPTION
# 20_Compute_TrainML.py trains the ML model to predict the probabilities of having a 
# flash flood event in a given grid-box. 
# Runtime: up to 10 minutes for each iteration when training the ML model over 25 years 
# of flood reports.

# INPUT PARAMETERS DESCRIPTION
# Years_Train (string): years included in the training dataset.
# Specification_PDT (string): specification indicating which PDT was used  for training.
# Git_Repo (string): repository's local path
# FileIN (string): relative path containing the point data table.
# DirOUT (string): relative path containing the weights for the ML model.

# INPUT PARAMETERS
Years_Train = "2005_2020"
Specification_PDT = "NoWestGP_AllPredictors_CW"
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Compute/19_Combine_PDT"
DirOUT = "Data/Compute/20_TrainML"
##########################################################################


# Reading the training dataset
FileIN_training = Git_Repo + "/" + DirIN + "/pdt_" + Specification_PDT + "_" + Years_Train + ".npy"
pdt_training = np.load(FileIN_training)

# Preparing the input/outputs categories
n_ff_all = pdt_training.shape[0]
x_training = pdt_training[:,1:]
y_training = np.zeros((n_ff_all,2))
y_training_temp = pdt_training[:,0]
ind_ff_1 = np.where(y_training_temp == 1)[0]
ind_ff_0 = np.where(y_training_temp == 0)[0]
y_training[ind_ff_1,0] = 1  # first category (i.e. first column) = yes-event
y_training[ind_ff_0,1] = 1  # second category (i.e. second column) = no-event

# Training the model
num_inputs = x_training.shape[1]
num_epochs = 50
num_patience_reduceLRO = 5
num_patience_eralyStopping = 8

model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(num_inputs,)),  # Input layer specifying the input shape
    tf.keras.layers.Dense(4, activation=tf.nn.relu),  # First hidden dense layer with ReLU activation
    tf.keras.layers.Dense(4, activation=tf.nn.relu),  # Second hidden dense layer with ReLU activation
    tf.keras.layers.Dense(2, activation=tf.nn.softmax)  # Output Dense layer with Softmax activation
    ])

model.compile(
    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss = tf.keras.losses.CategoricalCrossentropy(),
    metrics = [tf.keras.metrics.CategoricalAccuracy(name = "accuracy")],
    )

reduce_lr_callback = tf.keras.callbacks.ReduceLROnPlateau(
    monitor = 'val_loss',
    patience=3,
    factor=0.5,
    verbose=1
    )
 
early_stopping_callback = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    min_delta=0,
    patience=6,
    verbose=1,
    mode='auto'
    )
    
n_sample = pdt_training.shape[0]
n_sample_1 = ind_ff_1.shape[0]
n_sample_0 = ind_ff_0.shape[0]
class_weights = {0: 1/n_sample_1*n_sample, 1: 1/n_sample_0*n_sample}

history = model.fit(
    x_training, 
    y_training,
    epochs = num_epochs,
    validation_split = 0.2,
    class_weight = class_weights,
    shuffle=True,
    callbacks=[reduce_lr_callback, early_stopping_callback]
)

# Saving the model weigths and meta-data
MainDirOUT = Git_Repo + "/" + DirOUT + "/" + Specification_PDT + "_" + Years_Train
if not os.path.exists(MainDirOUT):
      os.makedirs(MainDirOUT)
model.save_weights(
    MainDirOUT + "/weights", overwrite=True, save_format=None, options=None
)