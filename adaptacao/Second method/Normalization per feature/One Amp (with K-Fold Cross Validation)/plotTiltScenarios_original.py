import numpy as np
import matplotlib.pyplot as plt

number_of_channels = 40

## Input files
input_mask_edfa1 = "First EDFA/EDFA_1STG/result_allMask_40channels_EDFA1STG_In_Tilt_flat_modified.txt"
input_mask_edfa2 = "Second EDFA/EDFA_2STG/result_allMask_40channels_EDFA2STG_In_Tilt_Flat.txt"

input_paths = [input_mask_edfa1, input_mask_edfa2]

## Input data lists
input_data_edfa1, input_data_edfa2 = ([] for _ in range(2))

input_lists = [input_data_edfa1, input_data_edfa2]

## Reading files
for input_path, input_data in zip(input_paths, input_lists):
	with open(input_path, 'r') as input_file:
		lines = input_file.readlines()
		for i in range(0, len(lines)):
			aux = [float(n) for n in lines[i].split()]
			input_data.append(aux)

input_data_edfa1 = np.array(input_data_edfa1)
input_data_edfa2 = np.array(input_data_edfa2)

## Searching maximum and minimum output tilt for each mask
max_tilt_edfa1_index = None
min_tilt_edfa1_index = None
max_tilt_edfa1 = float("-inf")
min_tilt_edfa1 = float("inf")

max_tilt_edfa2_index = None
min_tilt_edfa2_index = None
max_tilt_edfa2 = float("-inf")
min_tilt_edfa2 = float("inf")

for i in range(0, len(input_data_edfa1)):
	# Calculating output tilt
	tilt_edfa1 = (input_data_edfa1[i][49] - input_data_edfa1[i][49+number_of_channels-1])
	tilt_edfa2 = (input_data_edfa2[i][49] - input_data_edfa2[i][49+number_of_channels-1])

	# Checking EDFA1 tilt
	if tilt_edfa1 > max_tilt_edfa1:
		max_tilt_edfa1 = tilt_edfa1
		max_tilt_edfa1_index = i
	if tilt_edfa1 < min_tilt_edfa1:
		min_tilt_edfa1 = tilt_edfa1
		min_tilt_edfa1_index = i

	# Checking EDFA2 tilt
	if tilt_edfa2 > max_tilt_edfa2:
		max_tilt_edfa2 = tilt_edfa2
		max_tilt_edfa2_index = i
	if tilt_edfa2 < min_tilt_edfa2:
		min_tilt_edfa2 = tilt_edfa2
		min_tilt_edfa2_index = i

## Plotting tilt graphics
font = {'size' : 24}
plt.rc('font', **font)

# EDFA 1
max_tilt_edfa1_output = input_data_edfa1[max_tilt_edfa1_index][49:(49+number_of_channels)]
min_tilt_edfa1_output = input_data_edfa1[min_tilt_edfa1_index][49:(49+number_of_channels)]

plt.figure(figsize=(8,6))
plt.plot(max_tilt_edfa1_output, marker='+', linestyle='', markersize=16, color='k')
plt.plot([0, number_of_channels-1], [max_tilt_edfa1_output[0], max_tilt_edfa1_output[-1]], linewidth=8, label=str(round(max_tilt_edfa1, 2)) + ' dB')
plt.plot(min_tilt_edfa1_output, marker='x', linestyle='', markersize=16, color='k')
plt.plot([0, number_of_channels-1], [min_tilt_edfa1_output[0], min_tilt_edfa1_output[-1]], linewidth=8,  label=str(round(min_tilt_edfa1, 2)) + ' dB')
plt.ylabel('Output Signal Power')
plt.xlabel('Frequency')
plt.locator_params(nbins=3)
plt.xticks([])
plt.legend(bbox_to_anchor=(0.,1.0), loc="lower left", ncol=2)
plt.tight_layout()
plt.savefig("First EDFA/plots/TiltScenarioEDFA1-TESTE.pdf", dpi=200)

plt.clf()

# EDFA 2
max_tilt_edfa2_output = input_data_edfa2[max_tilt_edfa2_index][49:(49+number_of_channels)]
min_tilt_edfa2_output = input_data_edfa2[min_tilt_edfa2_index][49:(49+number_of_channels)]

plt.figure(figsize=(8,6))
plt.plot(max_tilt_edfa2_output, marker='+', linestyle='', markersize=16, color='k')
plt.plot([0, number_of_channels-1], [max_tilt_edfa2_output[0], max_tilt_edfa2_output[-1]], linewidth=8, label=str(round(max_tilt_edfa2, 2)) + ' dB')
plt.plot(min_tilt_edfa2_output, marker='x', linestyle='', markersize=16, color='k')
plt.plot([0, number_of_channels-1], [min_tilt_edfa2_output[0], min_tilt_edfa2_output[-1]], linewidth=8,  label=str(round(min_tilt_edfa2, 2)) + ' dB')
plt.ylabel('Output Signal Power')
plt.xlabel('Frequency')
plt.locator_params(nbins=3)
plt.xticks([])
plt.legend(bbox_to_anchor=(0.,1.0), loc="lower left", ncol=2)
plt.tight_layout()
plt.savefig("Second EDFA/plots/TiltScenarioEDFA2-TESTE.pdf", dpi=200)