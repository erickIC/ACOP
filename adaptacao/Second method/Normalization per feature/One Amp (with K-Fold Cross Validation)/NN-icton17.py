import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras import callbacks
from keras.layers import Dropout
from random import randint 

def unnormalization(x, max, min, range_a, range_b):
    z = []
    for i in range(0, len(x)):
        j = ((float(x[i]) - float(range_a))*(float(max)-float(min)))/ (float(range_b) - float(range_a)) + float(min)
        z.append(j)
    return z


### Reading file and placing data in an matrix where each row is a channel of a input
input_folder1 = "masks/mask-edfa1-padtec-icton17-fold-1v2.txt"
input_folder2 = "masks/mask-edfa1-padtec-icton17-fold-2v2.txt"
input_folder3 = "masks/mask-edfa1-padtec-icton17-fold-3v2.txt"
input_folder4 = "masks/mask-edfa1-padtec-icton17-fold-4v2.txt"
input_folder5 = "masks/mask-edfa1-padtec-icton17-fold-5v2.txt"
info_file = "masks/mask-edfa1-padtec-icton17-infov2.txt"

with open(input_folder1, 'r') as f_in:
	data1 = []
	lines = f_in.readlines()
	for i in range(0, len(lines)):
		auxiliary = lines[i].split()
		data1.append([float(auxiliary[0]), float(auxiliary[1]), float(auxiliary[2]), float(auxiliary[3]), float(auxiliary[4]), float(auxiliary[5])])

with open(input_folder2, 'r') as f_in:
	data2 = []
	lines = f_in.readlines()
	for i in range(0, len(lines)):
		auxiliary = lines[i].split()
		data2.append([float(auxiliary[0]), float(auxiliary[1]), float(auxiliary[2]), float(auxiliary[3]), float(auxiliary[4]), float(auxiliary[5])])

with open(input_folder3, 'r') as f_in:
	data3 = []
	lines = f_in.readlines()
	for i in range(0, len(lines)):
		auxiliary = lines[i].split()
		data3.append([float(auxiliary[0]), float(auxiliary[1]), float(auxiliary[2]), float(auxiliary[3]), float(auxiliary[4]), float(auxiliary[5])])

with open(input_folder4, 'r') as f_in:
	data4 = []
	lines = f_in.readlines()
	for i in range(0, len(lines)):
		auxiliary = lines[i].split()
		data4.append([float(auxiliary[0]), float(auxiliary[1]), float(auxiliary[2]), float(auxiliary[3]), float(auxiliary[4]), float(auxiliary[5])])

with open(input_folder5, 'r') as f_in:
	data5 = []
	lines = f_in.readlines()
	for i in range(0, len(lines)):
		auxiliary = lines[i].split()
		data5.append([float(auxiliary[0]), float(auxiliary[1]), float(auxiliary[2]), float(auxiliary[3]), float(auxiliary[4]), float(auxiliary[5])])

### Splitting data into training and testing set, and then using k-Fold Cross Validation to calculate error

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
	fold_x1.append([data1[i][0], data1[i][1], data1[i][2], data1[i][3]])
	fold_y1.append([data1[i][4], data1[i][5]])

	fold_x2.append([data2[i][0], data2[i][1], data2[i][2], data2[i][3]])
	fold_y2.append([data2[i][4], data2[i][5]])

	fold_x3.append([data3[i][0], data3[i][1], data3[i][2], data3[i][3]])
	fold_y3.append([data3[i][4], data3[i][5]])

	fold_x4.append([data4[i][0], data4[i][1], data4[i][2], data4[i][3]])
	fold_y4.append([data4[i][4], data4[i][5]])

	fold_x5.append([data5[i][0], data5[i][1], data5[i][2], data5[i][3]])
	fold_y5.append([data5[i][4], data5[i][5]])

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

#print(len(fold_x1), len(fold_y1), len(fold_x2), len(fold_y2), len(fold_x3), len(fold_y3), len(fold_x4), len(fold_y4), len(fold_x5), len(fold_y5))

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

	model.add(Dense(4, input_dim=4, activation='sigmoid'))
	model.add(Dropout(0.1))
	model.add(Dense(4, activation='sigmoid'))
	model.add(Dense(2, activation ='sigmoid'))

	model.compile(optimizer = 'adam', loss = 'mse', metrics = ['acc'])

	cb = callbacks.EarlyStopping(monitor = 'val_loss', min_delta = 0, patience = 120, verbose = 0, mode='auto')

	history = model.fit(trainings_x[i], trainings_y[i], validation_data=(tests_x[i], tests_y[i]), epochs = num_epochs,callbacks=[cb])

	model.save('nn-icon17v2' + str(i + 1) + '.h5')
	models.append(model)
	histories.append(history)


print(models[0].summary())
