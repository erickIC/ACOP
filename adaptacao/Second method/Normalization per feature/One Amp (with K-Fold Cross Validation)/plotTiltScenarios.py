import numpy as np
from collections import defaultdict
import scipy.constants as sp
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

## Creating Total Pout dictionary and saving corresponding indexes
dict_pout_total_edfa1, dict_pout_total_edfa2 = (defaultdict(list) for _ in range(2))

for i in range(0, len(input_data_edfa1)):
	dict_pout_total_edfa1[int(round(input_data_edfa1[i][1]))].append(i)
	dict_pout_total_edfa2[int(round(input_data_edfa2[i][1]))].append(i)

## Searching best maximum, minimum and null output tilt in each Total Pout of EDFA 1
max_tilt_edfa1_index, min_tilt_edfa1_index, null_tilt_edfa1_index = (None for _ in range(3))
tilt_difference = 0

# For each Total Pout, find best maximum, minimum and null output tilt and compare to the best found
for t_pout in dict_pout_total_edfa1.keys():
	max_tilt_edfa1 = float("-inf")
	min_tilt_edfa1, null_tilt_edfa1 = (float("inf") for _ in range(2))
	current_max_tilt_index, current_min_tilt_index, current_null_tilt_index = (None for _ in range(3))

	for index in dict_pout_total_edfa1[t_pout]:
		# Calculating output tilt and checking its condition in relation to other indexes
		tilt = (input_data_edfa1[index][49] - input_data_edfa1[index][49+number_of_channels-1])

		if tilt > max_tilt_edfa1:
			max_tilt_edfa1 = tilt
			current_max_tilt_index = index
		if tilt < min_tilt_edfa1:
			min_tilt_edfa1 = tilt
			current_min_tilt_index = index
		if abs(tilt) < null_tilt_edfa1:
			null_tilt_edfa1 = abs(tilt)
			current_null_tilt_index = index

	# Checking if current Total Pout result is the best
	current_tilt_difference = (max_tilt_edfa1 - min_tilt_edfa1)
	
	if current_tilt_difference > tilt_difference:
		max_tilt_edfa1_index = current_max_tilt_index
		min_tilt_edfa1_index = current_min_tilt_index
		null_tilt_edfa1_index = current_null_tilt_index
		tilt_difference = current_tilt_difference

## Searching best maximum, minimum and null output tilt in each Total Pout of EDFA 2
max_tilt_edfa2_index, min_tilt_edfa2_index, null_tilt_edfa2_index = (None for _ in range(3))
tilt_difference = 0

# For each Total Pout, find best maximum, minimum and null output tilt and compare to the best found
for t_pout in dict_pout_total_edfa2.keys():
	max_tilt_edfa2 = float("-inf")
	min_tilt_edfa2, null_tilt_edfa2 = (float("inf") for _ in range(2))
	current_max_tilt_index, current_min_tilt_index, current_null_tilt_index = (None for _ in range(3))

	for index in dict_pout_total_edfa2[t_pout]:
		# Calculating output tilt and checking its condition in relation to other indexes
		tilt = (input_data_edfa2[index][49] - input_data_edfa2[index][49+number_of_channels-1])

		if tilt > max_tilt_edfa2:
			max_tilt_edfa2 = tilt
			current_max_tilt_index = index
		if tilt < min_tilt_edfa2:
			min_tilt_edfa2 = tilt
			current_min_tilt_index = index
		if abs(tilt) < null_tilt_edfa2:
			null_tilt_edfa2 = abs(tilt)
			current_null_tilt_index = index

	# Checking if current Total Pout result is the best
	current_tilt_difference = (max_tilt_edfa2 - min_tilt_edfa2)
	
	if current_tilt_difference > tilt_difference:
		max_tilt_edfa2_index = current_max_tilt_index
		min_tilt_edfa2_index = current_min_tilt_index
		null_tilt_edfa2_index = current_null_tilt_index
		tilt_difference = current_tilt_difference

## Plotting tilt graphics
font = {'size' : 35}
plt.rc('font', **font)

wavelength = [1560.713, 1559.794, 1559.04, 1558.187, 1557.433, 1556.613, 1555.858, 1555.038, 1554.153, 1553.398, 1552.578, 1551.758, 1550.971, 1550.02, 1549.397, 1548.61, 1547.822, 1547.002, 1546.182, 1545.395, 1544.608, 1543.788, 1543.001, 1542.214, 1541.426, 1540.639, 1539.852, 1538.966, 1538.278, 1537.425, 1536.638, 1535.883, 1535.096, 1534.342, 1533.587, 1532.8, 1532.013, 1531.226, 1530.438, 1529.651]
frequency = [round((0.001*sp.c/wavelength[i]), 1) for i in range(len(wavelength))]

# EDFA 1
max_tilt_edfa1_output = input_data_edfa1[max_tilt_edfa1_index][49:(49+number_of_channels)]
max_tilt_edfa1 = max_tilt_edfa1_output[0] - max_tilt_edfa1_output[-1]
min_tilt_edfa1_output = input_data_edfa1[min_tilt_edfa1_index][49:(49+number_of_channels)]
min_tilt_edfa1 = min_tilt_edfa1_output[0] - min_tilt_edfa1_output[-1]
null_tilt_edfa1_output = input_data_edfa1[null_tilt_edfa1_index][49:(49+number_of_channels)]
null_tilt_edfa1 = null_tilt_edfa1_output[0] - null_tilt_edfa1_output[-1]

plt.figure(figsize=(12,10))
plt.plot(frequency, max_tilt_edfa1_output, marker='^', linestyle='', markersize=12, color='k')
plt.plot(frequency, min_tilt_edfa1_output, marker='o', linestyle='', markersize=12, color='k')
plt.plot(frequency, null_tilt_edfa1_output, marker='s', linestyle='', markersize=12, color='k')
plt.plot([frequency[0], frequency[-1]], [max_tilt_edfa1_output[0], max_tilt_edfa1_output[-1]], linewidth=5, label= 'Tilt: ' + str(round(max_tilt_edfa1, 2)) + ' dB')
plt.plot([frequency[0], frequency[-1]], [min_tilt_edfa1_output[0], min_tilt_edfa1_output[-1]], linewidth=5,  label= 'Tilt: ' + str(round(min_tilt_edfa1, 2)) + ' dB')
plt.plot([frequency[0], frequency[-1]], [null_tilt_edfa1_output[0], null_tilt_edfa1_output[-1]], linewidth=5,  label= 'Tilt: ' + str(round(null_tilt_edfa1, 2)) + ' dB')
plt.ylabel('Output Signal Power')
plt.xlabel('Frequency')
plt.legend(bbox_to_anchor=(0.,1.0), loc="lower left", ncol=2)
plt.tight_layout()
plt.savefig("First EDFA/plots/TiltScenarioEDFA1.pdf", dpi=200)

plt.clf()

# EDFA 2
max_tilt_edfa2_output = input_data_edfa2[max_tilt_edfa2_index][49:(49+number_of_channels)]
max_tilt_edfa2 = max_tilt_edfa2_output[0] - max_tilt_edfa2_output[-1]
min_tilt_edfa2_output = input_data_edfa2[min_tilt_edfa2_index][49:(49+number_of_channels)]
min_tilt_edfa2 = min_tilt_edfa2_output[0] - min_tilt_edfa2_output[-1]
null_tilt_edfa2_output = input_data_edfa2[null_tilt_edfa2_index][49:(49+number_of_channels)]
null_tilt_edfa2 = null_tilt_edfa2_output[0] - null_tilt_edfa2_output[-1]

plt.figure(figsize=(14,10))
plt.plot(frequency, max_tilt_edfa2_output, marker='^', linestyle='', markersize=12, color='k')
plt.plot(frequency, min_tilt_edfa2_output, marker='v', linestyle='', markersize=12, color='k')
plt.plot(frequency, null_tilt_edfa2_output, marker='s', linestyle='', markersize=12, color='k')
plt.plot([frequency[0], frequency[-1]], [max_tilt_edfa2_output[0], max_tilt_edfa2_output[-1]], linewidth=5, label= 'Tilt: ' + str(round(max_tilt_edfa2, 2)) + ' dB')
plt.plot([frequency[0], frequency[-1]], [min_tilt_edfa2_output[0], min_tilt_edfa2_output[-1]], linewidth=5,  label= 'Tilt: ' + str(round(min_tilt_edfa2, 2)) + ' dB')
plt.plot([frequency[0], frequency[-1]], [null_tilt_edfa2_output[0], null_tilt_edfa2_output[-1]], linewidth=5,  label= 'Tilt: ' + str(round(null_tilt_edfa2, 2)) + ' dB')
plt.ylabel('Output Signal Power')
plt.xlabel('Frequency')
plt.legend(bbox_to_anchor=(0.,1.0), loc="lower left", ncol=2)
plt.tight_layout()
plt.savefig("Second EDFA/plots/TiltScenarioEDFA2.pdf", dpi=200)

## Saving plot info
output_path_edfa1 = "First EDFA/plots/TiltScenarioInfoEDFA1.txt"
output_path_edfa2 = "Second EDFA/plots/TiltScenarioInfoEDFA2.txt"

with open(output_path_edfa1, 'w') as edfa1_output:
	new_line = "Tilt positivo:\n"
	new_line += "G_set: " + str(input_data_edfa1[max_tilt_edfa1_index][6]) + "\n"
	new_line += "Pin_total: " + str(int(round(input_data_edfa1[max_tilt_edfa1_index][0]))) + "\n"
	new_line += "Pout_total: " + str(int(round(input_data_edfa1[max_tilt_edfa1_index][1]))) + "\n"
	new_line += "\n"
	new_line += "Tilt negativo:\n"
	new_line += "G_set: " + str(input_data_edfa1[min_tilt_edfa1_index][6]) + "\n"
	new_line += "Pin_total: " + str(int(round(input_data_edfa1[min_tilt_edfa1_index][0]))) + "\n"
	new_line += "Pout_total: " + str(int(round(input_data_edfa1[min_tilt_edfa1_index][1]))) + "\n"
	new_line += "\n"
	new_line += "Tilt zero:\n"
	new_line += "G_set: " + str(input_data_edfa1[null_tilt_edfa1_index][6]) + "\n"
	new_line += "Pin_total: " + str(int(round(input_data_edfa1[null_tilt_edfa1_index][0]))) + "\n"
	new_line += "Pout_total: " + str(int(round(input_data_edfa1[null_tilt_edfa1_index][1]))) + "\n"

	edfa1_output.writelines(new_line)

with open(output_path_edfa2, 'w') as edfa2_output:
	new_line = "Tilt positivo:\n"
	new_line += "G_set: " + str(input_data_edfa2[max_tilt_edfa2_index][6]) + "\n"
	new_line += "Pin_total: " + str(int(round(input_data_edfa2[max_tilt_edfa2_index][0]))) + "\n"
	new_line += "Pout_total: " + str(int(round(input_data_edfa2[max_tilt_edfa2_index][1]))) + "\n"
	new_line += "\n"
	new_line += "Tilt negativo:\n"
	new_line += "G_set: " + str(input_data_edfa2[min_tilt_edfa2_index][6]) + "\n"
	new_line += "Pin_total: " + str(int(round(input_data_edfa2[min_tilt_edfa2_index][0]))) + "\n"
	new_line += "Pout_total: " + str(int(round(input_data_edfa2[min_tilt_edfa2_index][1]))) + "\n"
	new_line += "\n"
	new_line += "Tilt zero:\n"
	new_line += "G_set: " + str(input_data_edfa2[null_tilt_edfa2_index][6]) + "\n"
	new_line += "Pin_total: " + str(int(round(input_data_edfa2[null_tilt_edfa2_index][0]))) + "\n"
	new_line += "Pout_total: " + str(int(round(input_data_edfa2[null_tilt_edfa2_index][1]))) + "\n"

	edfa2_output.writelines(new_line)