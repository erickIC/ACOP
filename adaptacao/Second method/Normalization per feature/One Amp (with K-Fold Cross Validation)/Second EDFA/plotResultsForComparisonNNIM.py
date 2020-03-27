'''
	This script read the .txt files containing the results for the P_out prediction of IM and NN techniques,
	considering the dB step used, and generate a boxplot of the corresponding error.
'''

import numpy as np
import matplotlib.pyplot as plt

font = {'size' : 48}
plt.rc('font', **font)

## Group 1
im_input_file = "errors/im-error-for-group-1-without-gm.txt"
nn_input_file = "errors/nn-error-for-group-1.txt"
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

# Plotting results per fold (only used for 1dB step)
fold_size = int(len(im_mean_error) / 5)

plt.figure(num=1, figsize=(15,12))

plt.boxplot([im_mean_error[0:fold_size],
			 im_mean_error[fold_size:fold_size*2],
			 im_mean_error[fold_size*2:fold_size*3],
			 im_mean_error[fold_size*3:fold_size*4],
			 im_mean_error[fold_size*4:]])
plt.title("Mean error per signal for Interpolation Method (7 masks)")
plt.xticks(np.arange(1, 6), ["Fold 1", "Fold 2", "Fold 3", "Fold 4", "Fold 5"])
plt.ylabel("Error (dB)")
bottom_mean_group_1, top_mean_group_1 = plt.ylim()
plt.savefig("plots/ResultMeanErrorPerFold-IM-group-1.pdf", dpi=200)

plt.clf()

plt.boxplot([im_max_error[0:fold_size],
			 im_max_error[fold_size:fold_size*2],
			 im_max_error[fold_size*2:fold_size*3],
			 im_max_error[fold_size*3:fold_size*4],
			 im_max_error[fold_size*4:]])
plt.title("Maximum error per signal for Interpolation Method (7 masks)")
plt.xticks(np.arange(1, 6), ["Fold 1", "Fold 2", "Fold 3", "Fold 4", "Fold 5"])
plt.ylabel("Error (dB)")
bottom_max_group_1, top_max_group_1 = plt.ylim()
plt.savefig("plots/ResultMaxErrorPerFold-IM-group-1.pdf", dpi=200)

plt.clf()

plt.boxplot([nn_mean_error[0:fold_size],
			 nn_mean_error[fold_size:fold_size*2],
			 nn_mean_error[fold_size*2:fold_size*3],
			 nn_mean_error[fold_size*3:fold_size*4],
			 nn_mean_error[fold_size*4:]])
plt.title("Mean error per signal for Neural Network (7 masks)")
plt.xticks(np.arange(1, 6), ["Fold 1", "Fold 2", "Fold 3", "Fold 4", "Fold 5"])
plt.ylabel("Error (dB)")
plt.savefig("plots/ResultMeanErrorPerFold-NN-group-1.pdf", dpi=200)

plt.clf()

plt.boxplot([nn_max_error[0:fold_size],
			 nn_max_error[fold_size:fold_size*2],
			 nn_max_error[fold_size*2:fold_size*3],
			 nn_max_error[fold_size*3:fold_size*4],
			 nn_max_error[fold_size*4:]])
plt.title("Maximum error per signal for Neural Network (7 masks)")
plt.xticks(np.arange(1, 6), ["Fold 1", "Fold 2", "Fold 3", "Fold 4", "Fold 5"])
plt.ylabel("Error (dB)")
plt.savefig("plots/ResultMaxErrorPerFold-NN-group-1.pdf", dpi=200)

plt.clf()

# Plotting NN results without 'zoom'
plt.boxplot([nn_mean_error[0:fold_size],
			 nn_mean_error[fold_size:fold_size*2],
			 nn_mean_error[fold_size*2:fold_size*3],
			 nn_mean_error[fold_size*3:fold_size*4],
			 nn_mean_error[fold_size*4:]])
plt.title("Mean error per signal for Neural Network (7 masks)")
plt.xticks(np.arange(1, 6), ["Fold 1", "Fold 2", "Fold 3", "Fold 4", "Fold 5"])
plt.ylabel("Error (dB)")
plt.ylim(bottom_mean_group_1, top_mean_group_1)
plt.savefig("plots/ResultMeanErrorPerFold-NN-group-1-without-zoom.pdf", dpi=200)

plt.clf()

plt.boxplot([nn_max_error[0:fold_size],
			 nn_max_error[fold_size:fold_size*2],
			 nn_max_error[fold_size*2:fold_size*3],
			 nn_max_error[fold_size*3:fold_size*4],
			 nn_max_error[fold_size*4:]])
plt.title("Maximum error per signal for Neural Network (7 masks)")
plt.xticks(np.arange(1, 6), ["Fold 1", "Fold 2", "Fold 3", "Fold 4", "Fold 5"])
plt.ylabel("Error (dB)")
plt.ylim(bottom_max_group_1, top_max_group_1)
plt.savefig("plots/ResultMaxErrorPerFold-NN-group-1-without-zoom.pdf", dpi=200)

plt.clf()

## Groups 2 and 3
# Reading and plotting general results for both techniques
groups = [1, 2, 3]

im_general_error = []
nn_general_error = []

for group in groups:
	im_input_file = "errors/im-error-for-group-" + str(group) + "-without-gm.txt"
	nn_input_file = "errors/nn-error-for-group-" + str(group) + ".txt"

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

	# Creating list of general results
	im_general_error.append(im_data)
	nn_general_error.append(nn_data)

# Calculating average error and maximum error per signal
im_mean_error = []
nn_mean_error = []

im_max_error = []
nn_max_error = []

for im_group_error, nn_group_error in zip(im_general_error, nn_general_error):
	im_mean_error.append(np.mean(im_group_error, axis=1))
	im_max_error.append(np.amax(im_group_error, axis=1))
	nn_mean_error.append(np.mean(nn_group_error, axis=1))
	nn_max_error.append(np.amax(nn_group_error, axis=1))

# Plotting results
plt.boxplot([im_mean_error[0], im_mean_error[1], im_mean_error[2]])
plt.title("Mean error for Interpolation Method")
plt.xticks(np.arange(1, 4), ["7", "5", "3"])
plt.xlabel("Number of masks")
plt.ylabel("Mean error (dB)")
bottom_mean_other_groups, top_mean_other_groups = plt.ylim()
plt.tight_layout()
plt.savefig("plots/ResultMeanErrorPerGroup-IM.pdf", dpi=200)

plt.clf()

plt.boxplot([im_max_error[0], im_max_error[1], im_max_error[2]])
plt.title("Maximum error for Interpolation Method")
plt.xticks(np.arange(1, 4), ["7", "5", "3"])
plt.xlabel("Number of masks")
plt.ylabel("Maximum error (dB)")
bottom_max_other_groups, top_max_other_groups = plt.ylim()
plt.tight_layout()
plt.savefig("plots/ResultMaxErrorPerGroup-IM.pdf", dpi=200)

plt.clf()

plt.boxplot([nn_mean_error[0], nn_mean_error[1], nn_mean_error[2]])
plt.title("Mean error for Spectrum-Tilt")
plt.xticks(np.arange(1, 4), ["7", "5", "3"])
plt.xlabel("Number of masks")
plt.ylabel("Mean error (dB)")
plt.tight_layout()
plt.savefig("plots/ResultMeanErrorPerGroup-NN.pdf", dpi=200)

plt.clf()

plt.boxplot([nn_max_error[0], nn_max_error[1], nn_max_error[2]])
plt.title("Maximum error for Spectrum-Tilt")
plt.xticks(np.arange(1, 4), ["7", "5", "3"])
plt.xlabel("Number of masks")
plt.ylabel("Maximum error (dB)")
plt.tight_layout()
plt.savefig("plots/ResultMaxErrorPerGroup-NN.pdf", dpi=200)

plt.clf()

# Plotting NN results without 'zoom'
plt.boxplot([nn_mean_error[0], nn_mean_error[1], nn_mean_error[2]])
plt.title("Mean error for Spectrum-Tilt")
plt.xticks(np.arange(1, 4), ["7 masks", "5 masks", "3 masks"])
plt.ylabel("Error (dB)")
plt.ylim(bottom_mean_other_groups, top_mean_other_groups)
plt.savefig("plots/ResultMeanErrorPerGroup-NN-without-zoom.pdf", dpi=200)

plt.clf()

plt.boxplot([nn_max_error[0], nn_max_error[1], nn_max_error[2]])
plt.title("Maximum error for Spectrum-Tilt")
plt.xticks(np.arange(1, 4), ["7 masks", "5 masks", "3 masks"])
plt.ylabel("Error (dB)")
plt.ylim(bottom_max_other_groups, top_max_other_groups)
plt.savefig("plots/ResultMaxErrorPerGroup-NN-without-zoom.pdf", dpi=200)