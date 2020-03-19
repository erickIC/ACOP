import numpy as np

def normalization(x, min, max, range_a, range_b):
	z = ((float(range_b) - float(range_a)) * ((x - float(min))/(float(max) - float(min)))) + float(range_a)
	return z

input_file = "masks/mask-edfa1-padtec-new-modelsv2.txt"
output_file = "masks/mask-edfa1-padtec-new-models-normalizedv2.txt"
info_file = "masks/mask-edfa1-padtec-new-models-infov2.txt"

# Reading data
with open(input_file, 'r') as f_in:
	lines = f_in.readlines()

data = []
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

# Max and Min of Tilt
max_tilt = data[0][41]
min_tilt = data[0][41]

for i in range(1, data.shape[0]):
	if data[i][41] > max_tilt:
		max_tilt = data[i][41]
		continue
	if data[i][41] < min_tilt:
		min_tilt = data[i][41]

# Max and Min of Pout
max_pout = data[0][42]
min_pout = data[0][42]

for i in range(0, data.shape[0]):
	for j in range(42, 82):
		if data[i][j] > max_pout:
			max_pout = data[i][j]
			continue
		if data[i][j] < min_pout:
			min_pout = data[i][j]

# Max and Min of Noise Figure
max_nf = data[0][82]
min_nf = data[0][82]

for i in range(0, data.shape[0]):
	for j in range(82, data.shape[1]):
		if data[i][j] > max_nf:
			max_nf = data[i][j]
			continue
		if data[i][j] < min_nf:
			min_nf = data[i][j]

# Writes normalized data into output file
range_a = 0.15
range_b = 0.85

with open(output_file, 'w') as f_out:
	for i in range(0, data.shape[0]):
		new_line = ""
		
		new_line += str(normalization(data[i][0], min_gset, max_gset, range_a, range_b)) + '\t'
		for j in range(1, 41):
			new_line += str(normalization(data[i][j], min_pin, max_pin, range_a, range_b)) + '\t'
		new_line += str(normalization(data[i][41], min_tilt, max_tilt, range_a, range_b)) + '\t'
		for j in range(42, 82):
			new_line += str(normalization(data[i][j], min_pout, max_pout, range_a, range_b)) + '\t'
		for j in range(82, data.shape[1]):
			new_line += str(normalization(data[i][j], min_nf, max_nf, range_a, range_b)) + '\t'
		f_out.write(new_line + '\n')

# Save info to further use
with open(info_file, 'w') as f_info:
	new_line = str(max_gset) + '\t' + str(max_pin) + '\t' + str(max_tilt) + '\t'  + str(max_pout) + '\t' + str(max_nf)
	f_info.write(new_line + '\n')
	new_line = str(min_gset) + '\t' + str(min_pin) + '\t' + str(min_tilt) + '\t' + str(min_pout) + '\t' + str(min_nf)
	f_info.write(new_line + '\n')
	new_line = str(range_a) + '\t' + str(range_b)
	f_info.write(new_line + '\n')