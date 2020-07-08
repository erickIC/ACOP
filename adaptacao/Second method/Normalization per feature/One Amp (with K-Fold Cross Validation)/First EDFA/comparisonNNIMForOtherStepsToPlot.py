'''
	This script reads the 'new_models' mask with tilt value, define a reading step to generate
	training data and apply Neural Network (NN) and Interpolation Method (IM) techniques to
	predict P_out.
'''

import numpy as np
import interpolationMethod as IM
import neuralNetworkMethod as NN
import pickle
import matplotlib.pyplot as plt

def unnormalization_in(data, min_gset, max_gset, min_pin, max_pin, range_a, range_b):
	unnormalized_data = []
	for i in range(0, data.shape[0]):
		values = []
		for j in range(0, data.shape[1]):
		    if j == 0:
		        values.append(((float(data[i][j]) - float(range_a)) * (float(max_gset)-float(min_gset))) / (float(range_b) - float(range_a)) + float(min_gset))
		    else:
			    values.append(((float(data[i][j]) - float(range_a)) * (float(max_pin)-float(min_pin))) / (float(range_b) - float(range_a)) + float(min_pin))
		unnormalized_data.append(values)
	return np.array(unnormalized_data)


wavelength = [1560.713, 1559.794, 1559.04, 1558.187, 1557.433, 1556.613, 
               1555.858, 1555.038, 1554.153, 1553.398, 1552.578, 1551.758,
               1550.971, 1550.02, 1549.397, 1548.61, 1547.822, 1547.002, 
               1546.182, 1545.395, 1544.608, 1543.788, 1543.001, 1542.214,
               1541.426, 1540.639, 1539.852, 1538.966, 1538.278, 1537.425, 
               1536.638, 1535.883, 1535.096, 1534.342, 1533.587, 1532.8, 
               1532.013, 1531.226, 1530.438, 1529.651]

input_file = "masks/mask-edfa1-padtec-new-models-with-tilt.txt"
data = []

number_of_channels = 40
max_tilt = 14

# Read mask
with open(input_file, 'r') as f_in:
	entries = f_in.readlines()
for j in range(0, len(entries)):
	auxiliary = entries[j].split()
	data.append(auxiliary)

data = np.array(data, dtype=np.float32)

# Defining dB steps for the test
dB_steps = [14]

for step in dB_steps:
	# For each step, create a list of valid tilt values
	biggest_global = 0

	training_tilts = []

	for tilt in range(0, max_tilt+1, step):
		training_tilts.append(tilt)
		if tilt != 0:
			training_tilts.append(-tilt)
	
	# Separating training and test data according to valid tilt values
	training_data = []
	test_data = []

	for signal in data:
		tilt = signal[41]
		if tilt in training_tilts:
			training_data.append(signal)
		else:
			test_data.append(signal)
	
	training_data = np.array(training_data, dtype=np.float32)
	test_data = np.array(test_data, dtype=np.float32)
	
	# Testing both techniques
	p_out_im = IM.interpolationMethod(training_data, test_data)
	p_out_nn, model, history = NN.neuralNetworkMethod(training_data, test_data)

	# Calculating prediction error for each model
	im_error = []
	nn_error = []

	biggest_test = []
	biggest_pred = []

	for i in range(0, test_data.shape[0]):
		im_signal_error = []
		nn_signal_error = []
		current_test = []
		current_pred = []
		current_biggest = 0
		for j in range(42, 42+number_of_channels):
			im_signal_error.append(np.abs(test_data[i][j] - p_out_im[i][j-42]))
			current_test.append(test_data[i][j])
			current_pred.append(p_out_im[i][j-42])
			if np.abs(test_data[i][j] - p_out_im[i][j-42]) > current_biggest:
				current_biggest = np.abs(test_data[i][j] - p_out_im[i][j-42])
			
		if current_biggest > biggest_global:
			biggest_global = current_biggest
			biggest_test = np.array(current_test)
			biggest_pred = np.array(current_pred)

print(biggest_global)
print(biggest_test)
print(biggest_pred)

arrays = {
    'biggest_global': biggest_global,
    'biggest_test': biggest_test,
    'biggest_pred': biggest_pred,
    'wavelength': wavelength
}

pickle_out = open("biggestTIP.obj","wb")
pickle.dump(arrays, pickle_out)
pickle_out.close()


plt.figure()
plt.plot(wavelength, biggest_pred, 'o-',label='predicted pout')
plt.plot(wavelength, biggest_test, 'o-',label='expected pout')
plt.ylabel('Pout (dBm)')
plt.xlabel('Wavelenght')
plt.title('TIP Estimator EDFA 1 Biggest Error Spectrum')
plt.grid(True)
plt.legend()

plt.savefig('SpectrumTIP.pdf', dpi = 200)
