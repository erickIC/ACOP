'''
	This script reads the 'new_models' mask with tilt value, define a reading step to generate
	training data and apply Neural Network (NN) and Interpolation Method (IM) techniques to
	predict P_out.
'''

import numpy as np
import interpolationMethod as IM
import neuralNetworkMethod as NN
import pickle

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
dB_steps = [2, 4, 7, 14]

for step in dB_steps:
	# For each step, create a list of valid tilt values
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

	for i in range(0, test_data.shape[0]):
		im_signal_error = []
		nn_signal_error = []
		for j in range(42, 42+number_of_channels):
			im_signal_error.append(np.abs(test_data[i][j] - p_out_im[i][j-42]))
			nn_signal_error.append(np.abs(test_data[i][j] - p_out_nn[i][j-42]))
		im_error.append(im_signal_error)
		nn_error.append(nn_signal_error)
	
	# Saving NN model and history for current step
	model.save('models/nn-model-for-' + str(step) + 'dB-step.h5')
	history_data = [history.epoch, history.history['val_loss']]
	with open('models/nn-history-for-' + str(step) + 'dB-step.obj', 'wb') as pickle_out:
		pickle.dump(history_data, pickle_out)
	
	# Savings results for each step
	im_output_file = "errors/im-error-for-" + str(step) + "dB-step-without-gm.txt"
	nn_output_file = "errors/nn-error-for-" + str(step) + "dB-step.txt"

	with open(im_output_file, 'w') as im_f_out:
		for signal in im_error:
			im_f_out.write("".join([str(value) + " " for value in signal]))
			im_f_out.write('\n')

	with open(nn_output_file, 'w') as nn_f_out:
		for signal in nn_error:
			nn_f_out.write("".join([str(value) + " " for value in signal]))
			nn_f_out.write('\n')