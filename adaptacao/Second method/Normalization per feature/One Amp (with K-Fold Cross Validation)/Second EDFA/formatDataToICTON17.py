input_file = "masks/mask-edfa2-padtec.txt"
output_file = "masks/mask-edfa2-padtec-icton17.txt"

# Formatting data to match ICTON 17 model
with open(input_file, 'r') as f_in:
	entries = f_in.readlines()
number_of_channels = int(entries[0])

channel = []
for i in range(1, len(entries)):
	channels = entries[i].split()
	tilt = float(channels[3]) - float(channels[3 + number_of_channels-1])
	for j in range(0, number_of_channels):
		# Total P_in, G_set, Wavelength, Tilt, Channel P_out, Noise Figure(NF)
		channel.append(str(channels[0]) + ' ' + str(channels[2]) + ' ' + str(channels[3 + (3 * number_of_channels) + j]) + ' ' + str(tilt) + ' ' + str(float(channels[3 + number_of_channels + j])) + ' ' + str(channels[3 + (2 * number_of_channels) + j]) + '\n')

with open(output_file, 'w') as f_out:
	f_out.writelines(channel)