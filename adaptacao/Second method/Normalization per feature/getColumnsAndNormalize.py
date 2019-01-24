'''
Gets the following columns from input file: Gset, Pin, Pout, Noise Figure.
Then, writes this info into each output file, in the original and normalized form, respectively.
'''

import numpy as np

def normalization(x, min, max, range_a, range_b):	
	z = ( (float(range_b) - float(range_a)) * ( (x - float(min))/(float(max) - float(min)) ) ) + float(range_a)
	return z


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
	range_a = 0.15
	range_b = 0.85

	for i in range(0, data.shape[0]):
		new_line = ""
		
		new_line += str(normalization(data[i][0], min_gset, max_gset, range_a, range_b)) + '\t'
		for j in range(1, 41):
			new_line += str(normalization(data[i][j], min_pin, max_pin, range_a, range_b)) + '\t'
		for j in range(41, 81):
			new_line += str(normalization(data[i][j], min_pout, max_pout, range_a, range_b)) + '\t'
		for j in range(81, data.shape[1]):
			new_line += str(normalization(data[i][j], min_nf, max_nf, range_a, range_b)) + '\t'
		f_out.write(new_line + '\n')

#Creating the file of minimums and maximums.		
output_file = "min-max.txt"
with open(output_file, 'w') as f_out:
	new_line = str(max_gset) + '\t' + str(max_pin) + '\t' + str(max_pout) + '\t' + str(max_nf)
	f_out.write(new_line + '\n')
	new_line = str(min_gset) + '\t' + str(min_pin) + '\t' + str(min_pout) + '\t' + str(min_nf)
	f_out.write(new_line + '\n')
	f_out.close()