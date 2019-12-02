'''
	This script reads the 'new_models' mask with tilt value, split data in 5 folds and apply
	Neural Network (NN) and Interpolation Method (IM) techniques to predict P_out,  using 
	k-Fold Cross Validation.
'''

import numpy as np
import interpolationMethod as IM
import neuralNetworkMethod as NN

input_file = "masks/mask-edfa1-padtec-new-models-with-tilt.txt"
data = []

number_of_channels = 40

# Read mask
with open(input_file, 'r') as f_in:
	entries = f_in.readlines()
for j in range(0, len(entries)):
	auxiliary = entries[j].split()
	data.append(auxiliary)

# Create 5 folds and separate then in training groups
fold_size = int(len(data) / 5)

fold_1 = np.array(data[:fold_size], dtype=np.float32)
fold_2 = np.array(data[fold_size:fold_size*2], dtype=np.float32)
fold_3 = np.array(data[fold_size*2:fold_size*3], dtype=np.float32)
fold_4 = np.array(data[fold_size*3:fold_size*4], dtype=np.float32)
fold_5 = np.array(data[fold_size*4:], dtype=np.float32)

folds = [fold_1, fold_2, fold_3, fold_4, fold_5]

training_group_1 = np.concatenate((fold_2, fold_3, fold_4, fold_5))
training_group_2 = np.concatenate((fold_1, fold_3, fold_4, fold_5))
training_group_3 = np.concatenate((fold_1, fold_2, fold_4, fold_5))
training_group_4 = np.concatenate((fold_1, fold_2, fold_3, fold_5))
training_group_5 = np.concatenate((fold_1, fold_2, fold_3, fold_4))

training_groups = [training_group_1, training_group_2, training_group_3, training_group_4, training_group_5]

# Using k-Fold Cross Validation to test the techniques
im_error = []
nn_error = []

for fold, training_group in zip(folds, training_groups):
	p_out_im = IM.interpolationMethod(training_group, fold)
	p_out_nn = NN.neuralNetworkMethod(training_group, fold)

	# Calculating prediction error for each model
	for i in range(0, fold.shape[0]):
		im_signal_error = []
		nn_signal_error = []
		for j in range(42, 42+number_of_channels):
			im_signal_error.append(np.abs(fold[i][j] - p_out_im[i][j-42]))
			nn_signal_error.append(np.abs(fold[i][j] - p_out_nn[i][j-42]))
		im_error.append(im_signal_error)
		nn_error.append(nn_signal_error)

# Saving results
im_output_file = "im-error-for-1dB-step-without-gm.txt"
nn_output_file = "nn-error-for-1dB-step.txt"

with open(im_output_file, 'w') as im_f_out:
	for signal in im_error:
		im_f_out.write("".join([str(value) + " " for value in signal]))
		im_f_out.write('\n')

with open(nn_output_file, 'w') as nn_f_out:
	for signal in nn_error:
		nn_f_out.write("".join([str(value) + " " for value in signal]))
		nn_f_out.write('\n')