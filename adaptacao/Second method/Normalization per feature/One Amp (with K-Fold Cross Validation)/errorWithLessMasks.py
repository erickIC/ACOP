import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras import callbacks
from keras.layers import Dropout
import matplotlib.pyplot as plt

path = "EDFA_1STG/result_allMask_40channels_EDFA1STG_In_Tilt_"
dB = "dB"
extension = ".txt"
tilt_value = ["flat_modified", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14",
				"-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8", "-9", "-10", "-11", "-12", "-13", "-14"]

number_of_channels = 40
caught = []

def normalization(x, min, max, range_a, range_b):
	z = ((float(range_b) - float(range_a)) * ((x - float(min))/(float(max) - float(min)))) + float(range_a)
	return z

def unnormalization(data, min, max, range_a, range_b):
	unnormalized_data = []
	for i in range(0, data.shape[0]):
		values = []
		for j in range(0, data.shape[1]):
			values.append(((float(data[i][j]) - float(range_a)) * (float(max)-float(min))) / (float(range_b) - float(range_a)) + float(min))
		unnormalized_data.append(values)
	return np.array(unnormalized_data)

def read_files(data, step):
	for i in range(0, len(tilt_value), step):
		# Fix for 4dB step
		if step == 4 and i > 12:
			i += 2
			if i >= len(tilt_value):
				continue
		# Solving file name
		input_file = ""
		input_file = path + tilt_value[i]
		if i != 0:
			input_file += dB
		input_file += extension
		# Reading data
		if input_file not in caught:
			with open(input_file, 'r') as f_in:
				caught.append(input_file)
				entries = f_in.readlines()
			for j in range(0, len(entries)):
				auxiliary = entries[j].split()
				line = [0] * 81
				line[0] = float(auxiliary[6])	# G_set
				for k in range(0, number_of_channels):
					line[1+k] = float(auxiliary[9+k])	# P_in (channel)
				for m in range(0, number_of_channels):
					line[41+m] = float(auxiliary[49+m])	# P_out (channel)
				data.append(line)

# Mask step
step_db = 14

## Reading training and test data
training_data = []
read_files(training_data, step_db)
training_data = np.array(training_data)

test_data = []
read_files(test_data, 1)
test_data = np.array(test_data)

## Setting max and min

# Gset
max_gset = training_data[0][0]
min_gset = training_data[0][0]

# Pin
max_pin = training_data[0][1]
min_pin = training_data[0][1]

# Pout
max_pout = training_data[0][41]
min_pout = training_data[0][41]

for i in range(0, training_data.shape[0]):
	if training_data[i][0] > max_gset:
		max_gset = training_data[i][0]
		continue
	if training_data[i][0] < min_gset:
		min_gset = training_data[i][0]

	for j in range(1, 41):
		if training_data[i][j] > max_pin:
			max_pin = training_data[i][j]
			continue
		if training_data[i][j] < min_pin:
			min_pin = training_data[i][j]

	for j in range(41, 81):
		if training_data[i][j] > max_pout:
			max_pout = training_data[i][j]
			continue
		if training_data[i][j] < min_pout:
			min_pout = training_data[i][j]

## Normalize data
range_a = 0.15
range_b = 0.85

normalized_training_data = np.zeros_like(training_data)
normalized_test_data = np.zeros_like(test_data)

# Training data
for i in range(0, training_data.shape[0]):
	normalized_training_data[i, 0] = normalization(training_data[i, 0], min_gset, max_gset, range_a, range_b)
	for j in range(1, 41):
		normalized_training_data[i, j] = normalization(training_data[i, j], min_pin, max_pin, range_a, range_b)
	for j in range(41, 81):
		normalized_training_data[i, j] = normalization(training_data[i, j], min_pout, max_pout, range_a, range_b)

# Test data
for i in range(0, test_data.shape[0]):
	normalized_test_data[i, 0] = normalization(test_data[i, 0], min_gset, max_gset, range_a, range_b)
	for j in range(1, 41):
		normalized_test_data[i, j] = normalization(test_data[i, j], min_pin, max_pin, range_a, range_b)
	for j in range(41, 81):
		normalized_test_data[i, j] = normalization(test_data[i, j], min_pout, max_pout, range_a, range_b)

## Building neural network
num_epochs = 5000
model = Sequential()
model.add(Dense(54, input_dim = 41, activation='sigmoid'))
model.add(Dropout(0.1))
model.add(Dense(54, activation='sigmoid'))
model.add(Dense(40, activation='sigmoid'))
model.compile(optimizer = 'adam', loss = 'mse', metrics = ['acc'])
cb = callbacks.EarlyStopping(monitor = 'val_loss', min_delta = 0, patience = 120, verbose = 0, mode='auto')
model.fit(normalized_training_data[:, :41], normalized_training_data[:, 41:], validation_data=(normalized_test_data[:, :41], normalized_test_data[:, 41:]), epochs = num_epochs,callbacks=[cb])
output = model.predict(normalized_test_data[:, :41])

## Unnormalizing output
output = unnormalization(output, min_pout, max_pout, range_a, range_b)

## Calculating absolute error
diff = []
for i in range(0 , output.shape[0]):
    current_diff = 0
    for j in range(0, output.shape[1]):
        current_diff += abs(test_data[i, 41+j] - output[i, j])
    diff.append(current_diff/output.shape[1])

## Plot result
plt.boxplot(diff)
plt.title('Error using less masks (14dB step)')
plt.ylabel('P_out (dB)')
plt.show()