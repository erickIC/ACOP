'''
	This script reads the 'new_models' mask with tilt value, define tilt groups to generate
	training data and apply Neural Network (NN) and Interpolation Method (IM) techniques to
	predict P_out.
'''

import numpy as np
import interpolationMethod as IM
import neuralNetworkMethod as NN
import pickle

input_file = "masks/mask-edfa2-padtec-new-models-with-tilt.txt"
data = []

number_of_channels = 40

# Read mask
with open(input_file, 'r') as f_in:
	entries = f_in.readlines()
for j in range(0, len(entries)):
	auxiliary = entries[j].split()
	data.append(auxiliary)

data = np.array(data, dtype=np.float32)

# Defining tilt groups for the test
tilt_group_2 = [-8, -5, 0, 5, 8]
tilt_group_3 = [-8, 0, 8]

tilt_groups = [tilt_group_2, tilt_group_3]

group_count = 2	# for model saving purpose

for tilt_group in tilt_groups:
	# Separating training and test data according to valid tilt values
	training_data = []
	test_data = []

	for signal in data:
		tilt = signal[41]
		if tilt in tilt_group:
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

	# Saving NN model and history for current group
	model.save('models/nn-model-for-group-' + str(group_count) + '.h5')
	history_data = [history.epoch, history.history['val_loss']]
	with open('models/nn-history-for-group-' + str(group_count) + '.obj', 'wb') as pickle_out:
		pickle.dump(history_data, pickle_out)
	
	# Savings results for each step
	im_output_file = "errors/im-error-for-group-" + str(group_count) + "-without-gm.txt"
	nn_output_file = "errors/nn-error-for-group-" + str(group_count) + ".txt"

	with open(im_output_file, 'w') as im_f_out:
		for signal in im_error:
			im_f_out.write("".join([str(value) + " " for value in signal]))
			im_f_out.write('\n')

	with open(nn_output_file, 'w') as nn_f_out:
		for signal in nn_error:
			nn_f_out.write("".join([str(value) + " " for value in signal]))
			nn_f_out.write('\n')
	
	group_count += 1