def normalization(x, min, max, range_a, range_b):
	z = ((float(range_b) - float(range_a)) * ((x - float(min))/(float(max) - float(min)))) + float(range_a)
	return z

input_file = "masks/mask-edfa1-padtec-icton17.txt"
output_file = "masks/mask-edfa1-padtec-icton17-normalized.txt"
info_file = "masks/mask-edfa1-padtec-icton17-info.txt"

# Reading input mask
with open(input_file, 'r') as f_in:
	powers = f_in.readlines()

biggest_pintotal = -float('inf')
biggest_gset = -float('inf')
biggest_wave = -float('inf')
biggest_tilt = -float('inf')
biggest_gch = -float('inf')
biggest_nf = -float('inf')

smallest_pintotal = float('inf')
smallest_gset = float('inf')
smallest_wave = float('inf')
smallest_tilt = float('inf')
smallest_gch = float('inf')
smallest_nf = float('inf')

range_a = 0.15
range_b = 0.85

channel_float = []

# Loop to take the max's and min's of every variable and to separate the channels
for i in range(0, len(powers)):

	channels = powers[i].split()

	# Pintotal, Gset, Wavelength, Tilt, Gch, NF
	channel_float.append([float(channels[0]), float(channels[1]), float(channels[2]), float(channels[3]), float(channels[4]), float(channels[5])])

	if float(channels[0]) > biggest_pintotal:
		biggest_pintotal = float(channels[0])

	if float(channels[0]) < smallest_pintotal:
		smallest_pintotal = float(channels[0])

	if 	float(channels[1]) > biggest_gset:
		biggest_gset = float(channels[1])

	if float(channels[1]) < smallest_gset:
		smallest_gset = float(channels[1])

	if float(channels[2]) > biggest_wave:
		biggest_wave = float(channels[2])

	if float(channels[2]) < smallest_wave:
		smallest_wave = float(channels[2])

	if float(channels[3]) > biggest_tilt:
		biggest_tilt = float(channels[3])

	if float(channels[3]) < smallest_tilt:
		smallest_tilt = float(channels[3])

	if float(channels[4]) > biggest_gch:
		biggest_gch = float(channels[4])

	if float(channels[4]) < smallest_gch:
		smallest_gch = float(channels[4])

	if float(channels[5]) > biggest_nf:
		biggest_nf = float(channels[5])

	if float(channels[5]) < smallest_nf:
		smallest_nf = float(channels[5])

maximum = [biggest_pintotal, biggest_gset, biggest_wave, biggest_tilt, biggest_gch, biggest_nf]
minimum = [smallest_pintotal, smallest_gset, smallest_wave, smallest_tilt, smallest_gch, smallest_nf]
maximumstr = [str(biggest_pintotal) + ' ' + str(biggest_gset) + ' ' + str(biggest_wave) + ' ' + str(biggest_tilt) + ' ' + str(biggest_gch) + ' ' + str(biggest_nf) + '\n']
minimumstr = [str(smallest_pintotal) + ' ' + str(smallest_gset) + ' ' + str(smallest_wave) + ' ' + str(smallest_tilt) + ' ' + str(smallest_gch) + ' ' + str(smallest_nf) + '\n']

# Normalizing data
channel = []

for i in range(0, len(channel_float)):

	current = channel_float[i]
	for j in range(0, len(current)):
		current[j] = normalization(current[j], minimum[j], maximum[j], range_a, range_b)
	channel_float[i] = current

# Placing the data in the files
for i in range(0, len(channel_float)): 
	channel.append(str(channel_float[i][0]) + ' ' + str(channel_float[i][1])  + ' ' + str(channel_float[i][2]) + ' ' + str(channel_float[i][3]) + ' ' + str(channel_float[i][4]) + ' ' + str(channel_float[i][5]) + '\n')

with open(output_file, 'w') as f_out:
	f_out.writelines(channel)

with open(info_file, 'w') as f_info:
	f_info.writelines(maximumstr)
	f_info.writelines(minimumstr)
	f_info.writelines([str(range_a) + ' ' + str(range_b) + '\n'])