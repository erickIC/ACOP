'''
	This script reads the 'new_models' mask with tilt value, define a reading step to generate
	training data and apply Neural Network (NN) and Interpolation Method (IM) techniques to
	predict P_out.
'''

import numpy as np
from collections import defaultdict
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

data = np.array(data, dtype=np.float32)

# Creating tilt dictionary
tilt_dict = defaultdict(list)

for signal in data:
	tilt = signal[41]
	tilt_dict[tilt].append(signal)

# TODO: montar training_data' de acordo com os passo definidos, e montar 'test_data' com o restante