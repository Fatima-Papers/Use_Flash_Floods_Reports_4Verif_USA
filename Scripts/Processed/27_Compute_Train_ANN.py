import os
import sys
import time
import numpy as np
import tensorflow as tf


############################################################################
# CODE DESCRIPTION
# 27_Compute_Train_ANN.py trains an artificial neural network (ANN) to predict the 
# probabilities of having a flash flood event in a given grid-box. 
# Runtime: the code can take up to 2 to 5 minutes to run for each epoch.

# INPUT PARAMETERS DESCRIPTION
# Git_Repo (string): repository's local path
# FileIN (string): relative path of the file containing the training dataset (point data table, pdt).
# DirOUT (string): relative path of the directory containing the ANN's weights and metadata.

# INPUT PARAMETERS
Git_Repo = sys.argv[1]
FileIN = sys.argv[2]
DirOUT = sys.argv[3]
############################################################################


####################
# CUSTOM FUNCTIONS # 
####################

# Function to estimate the time taken by the ANN at each epoch
class TimeHistory(tf.keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.times = []

    def on_epoch_begin(self, epoch, logs={}):
        self.epoch_start_time = time.time()

    def on_epoch_end(self, epoch, logs={}):
        self.times.append(time.time() - self.epoch_start_time)

time_callback = TimeHistory()
#############################################################


# Reading the training dataset (point data table)
print()
print("Training the ANN model for:" + FileIN)
pdt = np.load(Git_Repo + "/" + FileIN)

# Preparing the variables containing the predictors (x) and the target (y)
count_FF = pdt.shape[0]
x = pdt[:,1:] # preparing the predictors 
y_temp = pdt[:,0] # preparing the target
y = np.zeros((count_FF,2))
ind_FF_1 = np.where(y_temp == 1)[0]
ind_FF_0 = np.where(y_temp == 0)[0]
y[ind_FF_1,0] = 1  # first target category (i.e. first column) = yes-flash-flood-events
y[ind_FF_0,1] = 1  # second category (i.e. second column) = no-flash-flood-events

# Training the model
num_inputs = x.shape[1]
num_epochs = 50
num_patience_reduceLRO = 5
num_patience_eralyStopping = 8

model = tf.keras.Sequential([
tf.keras.layers.InputLayer(input_shape=(num_inputs,)),  # Input layer specifying the input shape
tf.keras.layers.Dense(8, activation=tf.nn.relu),  # First hidden dense layer with ReLU activation
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
        
history = model.fit(
    x, 
    y,
    epochs = num_epochs,
    validation_split = 0.2,
    shuffle=True,
    callbacks=[reduce_lr_callback, early_stopping_callback, time_callback]
)

train_accuracy = history.history['accuracy'] # extracting meta-data about the training
validation_accuracy = history.history['val_accuracy']
train_time = time_callback.times

# Saving the model weigths and meta-data
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
    os.makedirs(MainDirOUT)
model.save_weights(MainDirOUT + "/test.weights.h5", overwrite=True)
np.save(MainDirOUT + "/train_accuracy", train_accuracy)
np.save(MainDirOUT + "/validation_accuracy", validation_accuracy)
np.save(MainDirOUT + "/train_time", train_time)