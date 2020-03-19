def normalization(x, min, max, range_a, range_b):
	
	z = ( (float(range_b) - float(range_a)) * ( (x - float(min))/(float(max) - float(min)) ) ) + float(range_a)
	return z

mask = open('mascara2.txt', 'r')
written = open('testew.txt', 'w')
max_and_min = open('max_min.txt', 'w')

powers = mask.readlines()

channel = []
channel_float = []

biggest_pintotal = -float('inf')
biggest_gset = -float('inf')
biggest_wave = -float('inf')
biggest_gch = -float('inf')
biggest_nf = -float('inf')

smallest_pintotal = float('inf')
smallest_gset = float('inf')
smallest_wave = float('inf')
smallest_gch = float('inf')
smallest_nf = float('inf')

range_a = 0.15
range_b = 0.85

total_channels = int(powers[0])

 # For to take the max's and min's of every variable and to separate the channels.  

for i in range(1, len(powers)):

	channels = powers[i].split()

	for j in range(0, total_channels):
						 #Pintotal               Gset					wave									Gch         Pout                     Pin                          						NF

		channel_float.append([float(channels[0]), float(channels[2]), float(channels[3 + (3*total_channels) + j]), float(float(channels[3 + total_channels + j]) - float(channels[3 + j])), float(channels[3 + (2*total_channels) + j])])

		if float(channels[0]) > biggest_pintotal:
			biggest_pintotal = float(channels[0])

		if float(channels[0]) < smallest_pintotal:
			smallest_pintotal = float(channels[0])

		if 	float(channels[2]) > biggest_gset:
			biggest_gset = float(channels[2])

		if float(channels[2]) < smallest_gset:
			smallest_gset = float(channels[2])

		if float(channels[3 + (3*total_channels) + j]) > biggest_wave:
			biggest_wave = float(channels[3 + (3*total_channels) + j])

		if float(channels[3 + (3*total_channels) + j]) < smallest_wave:
			smallest_wave = float(channels[3 + (3*total_channels) + j])

		if float(float(channels[3 + total_channels + j]) - float(channels[3 + j])) > biggest_gch:
			biggest_gch = float(float(channels[3 + total_channels + j]) - float(channels[3 + j]))

		if float(float(channels[3 + total_channels + j]) - float(channels[3 + j])) < smallest_gch:
			smallest_gch = float(float(channels[3 + total_channels + j]) - float(channels[3 + j]))

		if 	float(channels[3 + (2*total_channels) + j]) > biggest_nf:
			biggest_nf = float(channels[3 + (2*total_channels) + j])

		if float(channels[3 + (2*total_channels) + j]) < smallest_nf:
			smallest_nf = float(channels[3 + (2*total_channels) + j])						



maximum = [biggest_pintotal, biggest_gset, biggest_wave, biggest_gch, biggest_nf]
minimum = [smallest_pintotal, smallest_gset, smallest_wave, smallest_gch, smallest_nf]
maximumstr = [str(biggest_pintotal) + ' ' + str(biggest_gset) + ' ' + str(biggest_wave) + ' ' + str(biggest_gch) + ' ' + str(biggest_nf) + '\n']
minimumstr = [str(smallest_pintotal) + ' ' + str(smallest_gset) + ' ' + str(smallest_wave) + ' ' + str(smallest_gch) + ' ' + str(smallest_nf) + '\n']
print(maximum)
print(minimum)
print(channel_float[0])

 #normalizing the data.

for i in range(0, len(channel_float)): #normalizing the data.
	current = channel_float[i]

	for j in range(0, len(current)):
		current[j] = normalization(current[j], minimum[j], maximum[j], range_a, range_b)

	channel_float[i] = current	
		

#Put the data in a new file.

for i in range(0, len(channel_float)): 

	channel.append(str(channel_float[i][0]) + ' ' + str(channel_float[i][1])  + ' ' + str(channel_float[i][2]) + ' ' + str(channel_float[i][3]) + ' ' + str(channel_float[i][4]) + '\n')

written.writelines(channel)
max_and_min.writelines(maximumstr)
max_and_min.writelines(minimumstr)
max_and_min.writelines([str(range_a) + ' ' + str(range_b) + '\n'])
mask.close()
written.close()
max_and_min.close()