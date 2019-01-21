'''
Gets the following columns from input file: Gset, Pin, Pout, Noise Figure.
Then, writes this info into each output file, in the original and normalized form, respectively.
'''

import numpy as np

# Gets just the needed columns (Gset, Pin, Pout, Noise Figure)
input_file = "mask-edfa1-padtec.txt"
output_file = "mask-edfa1-padtec-modified.txt"

with open(output_file, 'w') as f_out:
	with open(input_file, 'r') as f_in:
		number_of_channels = int(f_in.readline())
		for line in f_in:
			new_line = ""
			new_line2 = ""
			new_line3 = ""
			columns = line.split('\t')

			new_line += columns[2] + '\t' # Gset
			for i in range(number_of_channels):
				new_line += columns[3+i] + '\t' # Pin
				new_line2 += columns[43+i] + '\t' # Pout
				new_line3 += columns[83+i] + '\t' # Noise Figure
			new_line += new_line2 + new_line3
			f_out.write(new_line + '\n')

# Normalization
input_file = "mask-edfa1-padtec-modified.txt"
output_file = "mask-edfa1-padtec-modified-normalized.txt"

with open(output_file, 'w') as f_out:
	with open(input_file, 'r') as f_in:
		data = []
		lines = f_in.readlines()
		for i in range(0, len(lines)):
			aux = lines[i].split()
			for j in range(0, len(aux)):
				aux[j] = float(aux[j])
			data.append(aux)
	data = np.array(data)
	
	# Max and Min of Gset
	max_gset = data[0][0]
	min_gset = data[0][0]

	for i in range(1, data.shape[0]):
		if data[i][0] > max_gset:
			max_gset = data[i][0]
			continue
		if data[i][0] < min_gset:
			min_gset = data[i][0]
	
	# Max and Min of Pin
	max_pin = data[0][1]
	min_pin = data[0][1]

	for i in range(0, data.shape[0]):
		for j in range(1, 41):
			if data[i][j] > max_pin:
				max_pin = data[i][j]
				continue
			if data[i][j] < min_pin:
				min_pin = data[i][j]

	# Max and Min of Pout
	max_pout = data[0][41]
	min_pout = data[0][41]

	for i in range(0, data.shape[0]):
		for j in range(41, 81):
			if data[i][j] > max_pout:
				max_pout = data[i][j]
				continue
			if data[i][j] < min_pout:
				min_pout = data[i][j]
	
	# Max and Min of Noise Figure
	max_nf = data[0][81]
	min_nf = data[0][81]

	for i in range(0, data.shape[0]):
		for j in range(81, data.shape[1]):
			if data[i][j] > max_nf:
				max_nf = data[i][j]
				continue
			if data[i][j] < min_nf:
				min_nf = data[i][j]
	
	# Writes normalized data into output file
	for i in range(0, data.shape[0]):
		new_line = ""
		new_line += str(round(((data[i][0] - min_gset) / (max_gset - min_gset)), 10)) + '\t'
		for j in range(1, 41):
			new_line += str(round(((data[i][j] - min_pin) / (max_pin - min_pin)), 10)) + '\t'
		for j in range(41, 81):
			new_line += str(round(((data[i][j] - min_pout) / (max_pout - min_pout)), 10)) + '\t'
		for j in range(81, data.shape[1]):
			new_line += str(round(((data[i][j] - min_nf) / (max_nf - min_nf)), 10)) + '\t'
		f_out.write(new_line + '\n')