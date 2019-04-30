'''
    Reaseacher group: EASY Group.
    Oriented by : Professor Erick Barboza.
    Students: Allan Bezerra, Jose Carlos Pinheiro Filho, Wagner Williams.
    Programmer: Jose Carlos Pinheiro Filho.

    Description:
    Code to create forty neural networks with only one output to Pout which each one is a diferente channel, using EarlyStoppping to previne the overfitting taking all the data to train.
    And plotting the difference between the signal predicted and the expected for non-normalized data with more information, boxplot of absolute error and the training curve. 

    licensed under the GNU General Public License v3.0.
'''

import numpy as np
from numpy import median
import matplotlib.pyplot as plt
import keras
from keras.models import Sequential
from keras.layers import Dense
from random import randint 
from keras import callbacks
from keras.layers import Dropout
from matplotlib.ticker import PercentFormatter



#Read the file. 
imput_file = 'mask-edfa1-padtec-modified-normalized.txt'

with open(imput_file, 'r') as file:
    data = []
    not_caught = []
    lines = file.readlines() 
    for i in range(0, len(lines)):
        auxiliary = lines[i].split('\t')
        x = []
        for j in range(0, len(auxiliary)-1):
            x.append(float(auxiliary[j]))
        data.append(x)
        not_caught.append(True)
#Separate the training set and the test set.
eighty_percent = int(1 * len(data))
number_channels = 40

array_x = []
array_xt = []

array_y_pout = []
array_yt_pout = []

for i in range(0, 40):
    array_y_pout.append([])
    array_yt_pout.append([])

      

while len(array_x) != eighty_percent: #While to set the training set.
    current = randint(0, len(not_caught) - 1)
    if  not_caught[current]:
        auxiliary = data[current]
        not_caught[current] = True
        x = [auxiliary[0]]
        for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            array_y_pout[i].append([auxiliary[41+i]])
        array_x.append(x)
 
for i in range(len(not_caught)):
    if not_caught[i]:
        auxiliary = data[i]
        not_caught[i] = False
        x = [auxiliary[0]]
        for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            array_yt_pout[i].append([auxiliary[41+i]])
        array_xt.append(x)
        if len(array_xt) ==  int(0.2 * len(data)):
            break 

#print(array_y_pout)
#print(len(array_y_pout))
#print(len(array_y_pout[i]))
            
training_x = np.array(array_x)
for i in range(0, len(array_y_pout)):
    array_y_pout[i] = np.array(array_y_pout[i])
training_y_pout = np.array(array_y_pout)

test_x = np.array(array_xt)
for i in range(0, len(array_y_pout)):
    array_yt_pout[i] = np.array(array_yt_pout[i])
test_y_pout = np.array(array_yt_pout)

#print(training_y_pout.shape[1])

#Create ta neural network to Pout

models = []

for i in range(0, training_y_pout.shape[0]):
    #print(training_y_pout[i])
    model_current = Sequential()

    model_current.add(Dense(28, input_dim = 41, activation ='sigmoid'))
    model_current.add(Dense(28, activation ='sigmoid'))
    model_current.add(Dense(1, activation ='sigmoid'))

    model_current.compile(optimizer = 'adam', loss = 'mse', metrics=['mean_absolute_error'])

    num_epochs = 5000
    cb = callbacks.EarlyStopping(monitor = 'val_loss', min_delta = 0, patience = 120, verbose = 0, mode='auto')

    model_current.fit(training_x, training_y_pout[i], validation_data=(test_x, test_y_pout[i]), epochs = num_epochs,callbacks=[cb])

    model_current.save('model_single_channel' + str(i+1) + '.h5')

    models.append(model_current)

print(len(models))