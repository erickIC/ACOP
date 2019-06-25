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

def unnormalization(data, min, max, range_a, range_b):
	unnormalized_data = []
	for i in range(0, data.shape[0]):
		values = []
		for j in range(0, data.shape[1]):
			values.append(((float(data[i][j]) - float(range_a)) * (float(max)-float(min))) / (float(range_b) - float(range_a)) + float(min))
		unnormalized_data.append(values)
	return np.array(unnormalized_data)

#Read the file. 

input_folder1 = "masks/mask-edfa1-padtec-new-models-fold-1v2.txt"
input_folder2 = "masks/mask-edfa1-padtec-new-models-fold-2v2.txt"
input_folder3 = "masks/mask-edfa1-padtec-new-models-fold-3v2.txt"
input_folder4 = "masks/mask-edfa1-padtec-new-models-fold-4v2.txt"
input_folder5 = "masks/mask-edfa1-padtec-new-models-fold-5v2.txt"
info_file = "masks/mask-edfa1-padtec-new-models-infov2.txt"

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

for i in range(0, len(data1)):
    auxiliary = data1[i]
    x = [auxiliary[0]]
    y = []
    for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            y.append(auxiliary[42+i]) #42 because 41 is tilt.
    x.append(auxiliary[41])
    fold_x1.append(x)
    fold_y1.append(y)

for i in range(0, len(data2)):
    auxiliary = data2[i]
    x = [auxiliary[0]]
    y = []
    for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            y.append(auxiliary[42+i]) #42 because 41 is tilt.
    x.append(auxiliary[41])
    fold_x2.append(x)
    fold_y2.append(y)

for i in range(0, len(data3)):
    auxiliary = data3[i]
    x = [auxiliary[0]]
    y = []
    for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            y.append(auxiliary[42+i]) #42 because 41 is tilt.
    x.append(auxiliary[41])
    fold_x3.append(x)
    fold_y3.append(y)

for i in range(0, len(data4)):
    auxiliary = data4[i]
    x = [auxiliary[0]]
    y = []
    for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            y.append(auxiliary[42+i]) #42 because 41 is tilt.
    x.append(auxiliary[41])
    fold_x4.append(x)
    fold_y4.append(y)

for i in range(0, len(data5)):
    auxiliary = data5[i]
    x = [auxiliary[0]]
    y = []
    for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            y.append(auxiliary[42+i]) #42 because 41 is tilt.
    x.append(auxiliary[41])
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

training_x1 = np.concatenate((fold_x1, fold_x2, fold_x3, fold_x4), axis = 0)
training_y1 = np.concatenate((fold_y1, fold_y2, fold_y3, fold_y4), axis = 0)
test_x1 = fold_x5 
test_y1 = fold_y5

training_x2 = np.concatenate((fold_x1, fold_x2, fold_x3, fold_x5), axis = 0)
training_y2 = np.concatenate((fold_y1, fold_y2, fold_y3, fold_y5), axis = 0)
test_x2 = fold_x4 
test_y2 = fold_y4

training_x3 = np.concatenate((fold_x1, fold_x2, fold_x5, fold_x4), axis = 0)
training_y3 = np.concatenate((fold_y1, fold_y2, fold_y5, fold_y4), axis = 0)
test_x3 = fold_x3
test_y3 = fold_y3

training_x4 = np.concatenate((fold_x1, fold_x5, fold_x3, fold_x4), axis = 0)
training_y4 = np.concatenate((fold_y1, fold_y5, fold_y3, fold_y4), axis = 0)
test_x4 = fold_x2
test_y4 = fold_y2

training_x5 = np.concatenate((fold_x5, fold_x2, fold_x3, fold_x4), axis = 0)
training_y5 = np.concatenate((fold_y5, fold_y2, fold_y3, fold_y4), axis = 0)
test_x5 = fold_x1 
test_y5 = fold_y1

trainings_x = [training_x1, training_x2, training_x3, training_x4, training_x5]
trainings_y = [training_y1, training_y2, training_y3, training_y4, training_y5]
tests_x = [test_x1, test_x2, test_x3, test_x4, test_x5]
tests_y = [test_y1, test_y2, test_y3, test_y4, test_y5]

# Building neural network
k = int(5)
models = []
histories = []
num_epochs = 5000

for i in range(0, k):
	model = Sequential()

	model.add(Dense(55, input_dim = 42, activation='sigmoid'))
	model.add(Dropout(0.1))
	model.add(Dense(55, activation='sigmoid'))
	model.add(Dense(40, activation='sigmoid'))

	model.compile(optimizer = 'adam', loss = 'mse', metrics = ['acc'])

	cb = callbacks.EarlyStopping(monitor = 'val_loss', min_delta = 0, patience = 120, verbose = 0, mode='auto')

	history = model.fit(trainings_x[i], trainings_y[i], validation_data=(tests_x[i], tests_y[i]), epochs = num_epochs,callbacks=[cb])

	model.save('nn-42to40v2' + str(i + 1) + '.h5')

	models.append(model)
	histories.append(history)


print(models[0].summary())