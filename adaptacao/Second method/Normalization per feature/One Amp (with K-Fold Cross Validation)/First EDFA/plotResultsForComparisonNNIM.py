'''
	This script read the .txt files containing the results for the P_out prediction of IM and NN techniques,
	considering the dB step used, and generate a boxplot of the corresponding error.
'''

import numpy as np
import matplotlib.pyplot as plt

## 1dB Step
im_input_file = "im-error-for-1dB-step.txt"
nn_input_file = "nn-error-for-1dB-step.txt"
im_data = []
nn_data = []

number_of_channels = 40

# Reading error files
with open(im_input_file, 'r') as im_f_in, open(nn_input_file, 'r') as nn_f_in:
	im_entries = im_f_in.readlines()
	nn_entries = nn_f_in.readlines()
for j in range(0, len(im_entries)):
	im_auxiliary = im_entries[j].split()
	nn_auxiliary = nn_entries[j].split()
	im_data.append(im_auxiliary)
	nn_data.append(nn_auxiliary)

im_data = np.array(im_data, dtype=np.float32)
nn_data = np.array(nn_data, dtype=np.float32)

# Calculating average error and maximum error per signal
im_mean_error = np.mean(im_data, axis=1)
nn_mean_error = np.mean(nn_data, axis=1)

im_max_error = np.amax(im_data, axis=1)
nn_max_error = np.amax(nn_data, axis=1)

# Plotting results per fold
fold_size = int(len(im_mean_error) / 5)

plt.figure(1)
plt.boxplot([im_mean_error[0:fold_size],
			 im_mean_error[fold_size:fold_size*2],
			 im_mean_error[fold_size*2:fold_size*3],
			 im_mean_error[fold_size*3:fold_size*4],
			 im_mean_error[fold_size*4:]])
plt.title("Mean error per signal for Interpolation Method")
plt.xticks(np.arange(1, 6), ["Fold 1", "Fold 2", "Fold 3", "Fold 4", "Fold 5"])
plt.ylabel("Error (dB)")
plt.savefig("ResultMeanErrorPerFold-IM.pdf", dpi=200)

plt.clf()

plt.boxplot([im_max_error[0:fold_size],
			 im_max_error[fold_size:fold_size*2],
			 im_max_error[fold_size*2:fold_size*3],
			 im_max_error[fold_size*3:fold_size*4],
			 im_max_error[fold_size*4:]])
plt.title("Maximum error per signal for Interpolation Method")
plt.xticks(np.arange(1, 6), ["Fold 1", "Fold 2", "Fold 3", "Fold 4", "Fold 5"])
plt.ylabel("Error (dB)")
plt.savefig("ResultMaxErrorPerFold-IM.pdf", dpi=200)

plt.clf()

plt.boxplot([nn_mean_error[0:fold_size],
			 nn_mean_error[fold_size:fold_size*2],
			 nn_mean_error[fold_size*2:fold_size*3],
			 nn_mean_error[fold_size*3:fold_size*4],
			 nn_mean_error[fold_size*4:]])
plt.title("Mean error per signal for Neural Network")
plt.xticks(np.arange(1, 6), ["Fold 1", "Fold 2", "Fold 3", "Fold 4", "Fold 5"])
plt.ylabel("Error (dB)")
plt.savefig("ResultMeanErrorPerFold-NN.pdf", dpi=200)

plt.clf()

plt.boxplot([nn_max_error[0:fold_size],
			 nn_max_error[fold_size:fold_size*2],
			 nn_max_error[fold_size*2:fold_size*3],
			 nn_max_error[fold_size*3:fold_size*4],
			 nn_max_error[fold_size*4:]])
plt.title("Maximum error per signal for Neural Network")
plt.xticks(np.arange(1, 6), ["Fold 1", "Fold 2", "Fold 3", "Fold 4", "Fold 5"])
plt.ylabel("Error (dB)")
plt.savefig("ResultMaxErrorPerFold-NN.pdf", dpi=200)

plt.clf()

# Plotting general results comparing both techniques
plt.boxplot([im_mean_error, nn_mean_error])
plt.title("Mean error per signal")
plt.xticks(np.arange(1, 3), ["Interpolation Method", "Neural Network"])
plt.ylabel("Error (dB)")
plt.savefig("ResultComparisonMeanError-NNIM.pdf", dpi=200)

plt.clf()

plt.boxplot([im_max_error, nn_max_error])
plt.title("Maximum error per signal")
plt.xticks(np.arange(1, 3), ["Interpolation Method", "Neural Network"])
plt.ylabel("Error (dB)")
plt.savefig("ResultComparisonMaxError-NNIM.pdf", dpi=200)