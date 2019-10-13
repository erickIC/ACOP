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

input_folder1 = "masks/mask-edfa1-padtec-new-models-fold-1.txt"
input_folder2 = "masks/mask-edfa1-padtec-new-models-fold-2.txt"
input_folder3 = "masks/mask-edfa1-padtec-new-models-fold-3.txt"
input_folder4 = "masks/mask-edfa1-padtec-new-models-fold-4.txt"
input_folder5 = "masks/mask-edfa1-padtec-new-models-fold-5.txt"
info_file = "masks/mask-edfa1-padtec-new-models-info.txt"

#Data into a array with floats.
with open(input_folder1, 'r') as file:
    data1 = []
    lines = file.readlines() 
    for i in range(0, len(lines)):
        auxiliary = lines[i].split('\t')
        x = []
        for j in range(0, len(auxiliary)-1):
            x.append(float(auxiliary[j]))
        data1.append(x)

with open(input_folder2, 'r') as file:
    data2 = []
    lines = file.readlines() 
    for i in range(0, len(lines)):
        auxiliary = lines[i].split('\t')
        x = []
        for j in range(0, len(auxiliary)-1):
            x.append(float(auxiliary[j]))
        data2.append(x)

with open(input_folder3, 'r') as file:
    data3 = []
    lines = file.readlines() 
    for i in range(0, len(lines)):
        auxiliary = lines[i].split('\t')
        x = []
        for j in range(0, len(auxiliary)-1):
            x.append(float(auxiliary[j]))
        data3.append(x)

with open(input_folder4, 'r') as file:
    data4 = []
    lines = file.readlines() 
    for i in range(0, len(lines)):
        auxiliary = lines[i].split('\t')
        x = []
        for j in range(0, len(auxiliary)-1):
            x.append(float(auxiliary[j]))
        data4.append(x)

with open(input_folder5, 'r') as file:
    data5 = []
    lines = file.readlines() 
    for i in range(0, len(lines)):
        auxiliary = lines[i].split('\t')
        x = []
        for j in range(0, len(auxiliary)-1):
            x.append(float(auxiliary[j]))
        data5.append(x)



number_channels = 40

fold_x1 = []
fold_y1 = []

fold_x2 = []
fold_y2 = []

fold_x3 = []
fold_y3 = []

fold_x4 = []
fold_y4 = []

fold_x5 = []
fold_y5 = []

array_y = []
array_yt = []

for i in range(0, number_channels):
    array_y.append([])
    array_yt.append([])

for i in range(0, len(data1)):
    auxiliary = data1[i]
    x = [auxiliary[0]]
    y = []
    for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            y.append(auxiliary[42+i]) #42 because 41 is tilt.
            array_y[i].append([auxiliary[42+i]])
            #array_y_pout[i].append([auxiliary[41+i]])
    fold_x1.append(x)
    fold_y1.append(y)

for i in range(0, len(data2)):
    auxiliary = data2[i]
    x = [auxiliary[0]]
    y = []
    for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            y.append(auxiliary[42+i]) #42 because 41 is tilt.
            array_yt[i].append([auxiliary[42+i]])
            
    fold_x2.append(x)
    fold_y2.append(y)

for i in range(0, len(data3)):
    auxiliary = data3[i]
    x = [auxiliary[0]]
    y = []
    for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            y.append(auxiliary[42+i]) #42 because 41 is tilt.
            array_y[i].append([auxiliary[42+i]])
            
    fold_x3.append(x)
    fold_y3.append(y)

for i in range(0, len(data4)):
    auxiliary = data4[i]
    x = [auxiliary[0]]
    y = []
    for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            y.append(auxiliary[42+i]) #42 because 41 is tilt.
            array_y[i].append([auxiliary[42+i]])
            
    fold_x4.append(x)
    fold_y4.append(y)

for i in range(0, len(data5)):
    auxiliary = data5[i]
    x = [auxiliary[0]]
    y = []
    for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            y.append(auxiliary[42+i]) #42 because 41 is tilt.
            array_y[i].append([auxiliary[42+i]])
    fold_x5.append(x)
    fold_y5.append(y)

#print(len(fold_y1[0]), fold_y1[0])

fold_x1 = np.array(fold_x1)
fold_y1 = np.array(fold_y1)

fold_x2 = np.array(fold_x2)
fold_y2 = np.array(fold_y2)

fold_x3 = np.array(fold_x3)
fold_y3 = np.array(fold_y3)

fold_x4 = np.array(fold_x4)
fold_y4 = np.array(fold_y4)

fold_x5 = np.array(fold_x5)
fold_y5 = np.array(fold_y5)

training_x = np.concatenate((fold_x1, fold_x3, fold_x4, fold_x5), axis = 0)


test_x = fold_x2 


for i in range(0, len(array_y)):
    array_y[i] = np.array(array_y[i])
training_y = np.array(array_y)



for i in range(0, len(array_y)):
    array_yt[i] = np.array(array_yt[i])
test_y = np.array(array_yt)


#Create ta neural network to Pout

models = []

for i in range(0, training_y.shape[0]):
    #print(training_y_pout[i])
    model_current = Sequential()

    model_current.add(Dense(28, input_dim = 41, activation ='sigmoid'))
    model_current.add(Dropout(0.1))
    model_current.add(Dense(28, activation ='sigmoid'))
    model_current.add(Dense(1, activation ='sigmoid'))

    model_current.compile(optimizer = 'adam', loss = 'mse', metrics=['acc'])

    num_epochs = 5000
    cb = callbacks.EarlyStopping(monitor = 'val_loss', min_delta = 0, patience = 120, verbose = 0, mode='auto')

    model_current.fit(training_x, training_y[i], validation_data=(test_x, test_y[i]), epochs = num_epochs,callbacks=[cb])

    model_current.save('NN-41to1-4' + str(i+1) + '.h5')

    models.append(model_current)

print(len(models))