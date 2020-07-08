'''
	This script reads the 'new_models' mask with tilt value, define a reading step to generate
	training data and apply Neural Network (NN) and Interpolation Method (IM) techniques to
	predict P_out.
'''

import numpy as np
import interpolationMethod as IM
# import neuralNetworkMethod as NN
import pickle

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
	training_tilts = []

	for tilt in range(0, max_tilt+1, step):
		training_tilts.append(tilt)
		if tilt != 0:
			training_tilts.append(-tilt)
	
	if step == 14:
		biggest_global = 0

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
	print('arigato 1')
	
	# Testing both techniques
	p_out_im = IM.interpolationMethod(training_data, test_data)
	# p_out_nn, model, history = NN.neuralNetworkMethod(training_data, test_data)
	print('arigato 2')

	# Calculating prediction error for each model
	im_error = []
	# nn_error = []

	for i in range(0, test_data.shape[0]):
		im_signal_error = []
		# nn_signal_error = []
		if step == 14:
			current_test = []
			current_pred = []
			current_biggest = 0

		for j in range(42, 42+number_of_channels):
			im_signal_error.append(np.abs(test_data[i][j] - p_out_im[i][j-42]))
			# nn_signal_error.append(np.abs(test_data[i][j] - p_out_nn[i][j-42]))
			if step == 14:
				current_test.append(test_data[i][j])
				current_pred.append(p_out_im[i][j-42])
				if np.abs(test_data[i][j] - p_out_im[i][j-42]) > current_biggest:
					current_biggest = np.abs(test_data[i][j] - p_out_im[i][j-42])
		im_error.append(im_signal_error)
		# nn_error.append(nn_signal_error)
		if step == 14:
			if current_biggest > biggest_global:
				biggest_global = current_biggest
				biggest_test = np.array(current_test)
				biggest_pred = np.array(current_pred)
	
	if step == 14:
		arrays = {
		    'biggest_global': biggest_global,
		    'biggest_test': biggest_test,
		    'biggest_pred': biggest_pred,
		    'wavelength': wavelength
		}
		
		pickle_out = open("carlos/biggestTIP.obj","wb")
		pickle.dump(arrays, pickle_out)
		pickle_out.close()
	
	# Saving NN model and history for current step
	# model.save('carlos/models/nn-model-for-' + str(step) + 'dB-step.h5')
	# history_data = [history.epoch, history.history['val_loss']]
	# with open('carlos/models/nn-history-for-' + str(step) + 'dB-step.obj', 'wb') as pickle_out:
	# 	pickle.dump(history_data, pickle_out)
	
	# Savings results for each step
	im_output_file = "carlos/errors/im-error-for-" + str(step) + "dB-step-without-gm.txt"
	# nn_output_file = "carlos/errors/nn-error-for-" + str(step) + "dB-step.txt"

	with open(im_output_file, 'w') as im_f_out:
		for signal in im_error:
			im_f_out.write("".join([str(value) + " " for value in signal]))
			im_f_out.write('\n')

	# with open(nn_output_file, 'w') as nn_f_out:
	# 	for signal in nn_error:
	# 		nn_f_out.write("".join([str(value) + " " for value in signal]))
	# 		nn_f_out.write('\n')

	print('Finalizando step', step)