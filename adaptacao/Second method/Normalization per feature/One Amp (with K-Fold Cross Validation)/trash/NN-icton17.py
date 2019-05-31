import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense
from random import randint 

### Reading file and placing data in an matrix where each row is a channel of a input
input_file = "mask-edfa1-padtec-icton17-normalized.txt"
info_file = "mask-edfa1-padtec-icton17-info.txt"

with open(input_file, 'r') as f_in:
	data = []
	caught = []
	lines = f_in.readlines()
	for i in range(0, len(lines)):
		auxiliary = lines[i].split()
		data.append([float(auxiliary[0]), float(auxiliary[1]), float(auxiliary[2]), float(auxiliary[3]), float(auxiliary[4]), float(auxiliary[5])])
		caught.append(0)

### Splitting data into training and testing set, and then using k-Fold Cross Validation to calculate error


# Building neural network

model = Sequential()

model.add(Dense(4, input_dim=4, activation='sigmoid'))
model.add(Dense(4, activation='sigmoid'))
model.add(Dense(2, activation ='sigmoid'))

print(model.summary())

#input()

model.compile(optimizer = 'adam', loss = 'mse', metrics = ['acc'])

# model.fit(training_x, training_y, epochs = 100)

# loss, acc = model.evaluate(test_x, test_y)

# t = "Trained model accuracy: " + str((acc*100)) + "%" + " and the loss: " + str(loss)
# print(t)

# file.close()