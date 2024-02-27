import os
import numpy as np
import tensorflow as tf

###########################################################################
# CODE DESCRIPTION
# 12_Compute_Training_Model.py trains the ML model.
# Runtime: up to 25 minutes when training the model over 20 years of reports.

# INPUT PARAMETERS DESCRIPTION
# Years_training (string): years covered in the training dataset.
# Git_Repo (string): repository's local path
# DirIN (string): relative path containing the point data table.
# DirOUT (string): relative path containing the weights for the ML model.

# INPUT PARAMETERS
Years_training = "1996_2020"
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Compute/10_Combine_PDT"
DirOUT = "Data/Compute/12_Training_Model"
###########################################################################

# Reading the training dataset
FileIN_training = Git_Repo + "/" + DirIN + "/pdt_" + Years_training + ".npy"
pdt_training = np.load(FileIN_training)

a = np.where(pdt_training[:,0] == 1)[0]
b = np.where(pdt_training[:,0] == 0)[0]
m = a.shape[0]
pdt_a = pdt_training[a,:]
pdt_b = pdt_training[b,:]
pdt_training = np.concatenate((pdt_a,pdt_b[0:2*m,:]), axis=0)

# Preparing the input/outputs categories
n_ff_all = pdt_training.shape[0]
x_training = pdt_training[:,1:-1]
y_training = np.zeros((n_ff_all,2))
y_training_temp = pdt_training[:,0]
ind_ff_1 = np.where(y_training_temp == 1)[0]
ind_ff_0 = np.where(y_training_temp == 0)[0]
y_training[ind_ff_1,0] = 1  # first category (i.e. first column) = yes-event
y_training[ind_ff_0,1] = 1  # second category (i.e. second column) = no-event

# Training the model
model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(3,)),  # Input layer specifying the input shape
    tf.keras.layers.Dense(8, activation=tf.nn.relu),  # First hidden dense layer with ReLU activation
    tf.keras.layers.Dense(8, activation=tf.nn.relu),  # Second hidden dense layer with ReLU activation
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
            verbose=1)
 
early_stopping_callback = tf.keras.callbacks.EarlyStopping(
                        monitor='val_loss',
                        min_delta=0,
                        patience=6,
                        verbose=1,
                        mode='auto'
                    )

model.fit(
    x_training, 
    y_training,
    epochs=100,
    validation_split=0.2,
    shuffle=True,
    callbacks=[reduce_lr_callback, early_stopping_callback]
)

# Saving the model weigths
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
      os.makedirs(MainDirOUT)
FileOUT = MainDirOUT + "/weights"
model.save_weights(
    FileOUT, overwrite=True, save_format=None, options=None
)