import numpy as np

# path = "First EDFA/EDFA_1STG/result_allMask_40channels_EDFA1STG_In_Tilt_"
path = "Second EDFA/EDFA_2STG/result_allMask_40channels_EDFA2STG_In_Tilt_"
dB = "dB"
extension = ".txt"
# flat_modified = "flat_modified"
flat_modified = "Flat"

# tilts = np.arange(1, 15)
tilts = np.arange(2, 9, 3)
number_of_channels = 40

wavelength = [1560.713, 1559.794, 1559.04, 1558.187, 1557.433, 1556.613, 1555.858, 1555.038, 1554.153, 1553.398, 1552.578, 1551.758, 1550.971, 1550.02, 1549.397, 1548.61, 1547.822, 1547.002, 1546.182, 1545.395, 1544.608, 1543.788, 1543.001, 1542.214, 1541.426, 1540.639, 1539.852, 1538.966, 1538.278, 1537.425, 1536.638, 1535.883, 1535.096, 1534.342, 1533.587, 1532.8, 1532.013, 1531.226, 1530.438, 1529.651]

## Per-Channel
# output_file = "First EDFA/EDFA_1STG/PerChannel/mask-edfa1-padtec-per-channel.txt"
output_file = "Second EDFA/EDFA_2STG/PerChannel/mask-edfa2-padtec-per-channel.txt"

def read_files_for_1dB_step(data, tilts):
	for i in range(len(tilts)):
		# Positive mask
		input_file = path + str(tilts[i]) + dB + extension
		with open(input_file, 'r') as f_in:
			entries = f_in.readlines()
		for j in range(0, len(entries)):
			auxiliary = entries[j].split()
			for k in range(0, number_of_channels):
				line = ""
				line += auxiliary[0] + '\t'	# Pin_total
				line += auxiliary[6] + '\t'	# G_set
				line += str(wavelength[k]) + '\t'	# Wavelength
				line += auxiliary[49+k] + '\t'	# Pout_channel
				data += line + '\n'

		# Negative mask
		input_file = path + '-' + str(tilts[i]) + dB + extension
		with open(input_file, 'r') as f_in:
			entries = f_in.readlines()
		for j in range(0, len(entries)):
			auxiliary = entries[j].split()
			for k in range(0, number_of_channels):
				line = ""
				line += auxiliary[0] + '\t'	# Pin_total
				line += auxiliary[6] + '\t'	# G_set
				line += str(wavelength[k]) + '\t'	# Wavelength
				line += auxiliary[49+k] + '\t'	# Pout_channel
				data += line + '\n'
	return data

def include_flat_modified(data):
	input_file = path + flat_modified + extension
	with open(input_file, 'r') as f_in:
		entries = f_in.readlines()
	for j in range(0, len(entries)):
		auxiliary = entries[j].split()
		for k in range(0, number_of_channels):
			line = ""
			line += auxiliary[0] + '\t'	# Pin_total
			line += auxiliary[6] + '\t'	# G_set
			line += str(wavelength[k]) + '\t'	# Wavelength
			line += auxiliary[49+k] + '\t'	# Pout_channel
			data += line + '\n'
	return data

# Reading all files
data = ""
data = read_files_for_1dB_step(data, tilts)
data = include_flat_modified(data)

# Writing output
with open(output_file, 'w') as f_out:
	f_out.writelines(data)

## Per-Channel with Tilt
# output_file = "First EDFA/EDFA_1STG/PerChannel-Tilt/mask-edfa1-padtec-per-channel-with-tilt.txt"
output_file = "Second EDFA/EDFA_2STG/PerChannel-Tilt/mask-edfa2-padtec-per-channel-with-tilt.txt"

def read_files_for_1dB_step(data, tilts):
	for i in range(len(tilts)):
		# Positive mask
		input_file = path + str(tilts[i]) + dB + extension
		with open(input_file, 'r') as f_in:
			entries = f_in.readlines()
		for j in range(0, len(entries)):
			auxiliary = entries[j].split()
			for k in range(0, number_of_channels):
				line = ""
				line += auxiliary[0] + '\t'	# Pin_total
				line += auxiliary[6] + '\t'	# G_set
				line += str(wavelength[k]) + '\t'	# Wavelength
				line += str(tilts[i]) + '\t'	# Tilt
				line += auxiliary[49+k] + '\t'	# Pout_channel
				data += line + '\n'

		# Negative mask
		input_file = path + '-' + str(tilts[i]) + dB + extension
		with open(input_file, 'r') as f_in:
			entries = f_in.readlines()
		for j in range(0, len(entries)):
			auxiliary = entries[j].split()
			for k in range(0, number_of_channels):
				line = ""
				line += auxiliary[0] + '\t'	# Pin_total
				line += auxiliary[6] + '\t'	# G_set
				line += str(wavelength[k]) + '\t'	# Wavelength
				line += '-' + str(tilts[i]) + '\t'	# Tilt
				line += auxiliary[49+k] + '\t'	# Pout_channel
				data += line + '\n'
	return data

def include_flat_modified(data):
	input_file = path + flat_modified + extension
	with open(input_file, 'r') as f_in:
		entries = f_in.readlines()
	for j in range(0, len(entries)):
		auxiliary = entries[j].split()
		for k in range(0, number_of_channels):
			line = ""
			line += auxiliary[0] + '\t'	# Pin_total
			line += auxiliary[6] + '\t'	# G_set
			line += str(wavelength[k]) + '\t'	# Wavelength
			line += str(0) + '\t'	# Tilt
			line += auxiliary[49+k] + '\t'	# Pout_channel
			data += line + '\n'
	return data

# Reading all files
data = ""
data = read_files_for_1dB_step(data, tilts)
data = include_flat_modified(data)

# Writing output
with open(output_file, 'w') as f_out:
	f_out.writelines(data)

## Spectrum
# output_file = "First EDFA/EDFA_1STG/Spectrum/mask-edfa1-padtec-spectrum.txt"
output_file = "Second EDFA/EDFA_2STG/Spectrum/mask-edfa2-padtec-spectrum.txt"

def read_files_for_1dB_step(data, tilts):
	for i in range(len(tilts)):
		# Positive mask
		input_file = path + str(tilts[i]) + dB + extension
		with open(input_file, 'r') as f_in:
			entries = f_in.readlines()
		for j in range(0, len(entries)):
			auxiliary = entries[j].split()
			line = ""
			line_pin = ""
			line_pout = ""
			line += str(auxiliary[6]) + '\t'	# G_set
			for k in range(0, number_of_channels):
				line_pin += str(auxiliary[9+k]) + '\t'	# Pin_channel
				line_pout += str(auxiliary[49+k]) + '\t'	# Pout_channel
			line += line_pin 
			line += line_pout
			data += line + '\n'

		# Negative mask
		input_file = path + '-' + str(tilts[i]) + dB + extension
		with open(input_file, 'r') as f_in:
			entries = f_in.readlines()
		for j in range(0, len(entries)):
			auxiliary = entries[j].split()
			line = ""
			line_pin = ""
			line_pout = ""
			line += str(auxiliary[6]) + '\t'	# G_set
			for k in range(0, number_of_channels):
				line_pin += str(auxiliary[9+k]) + '\t'	# Pin_channel
				line_pout += str(auxiliary[49+k]) + '\t'	# Pout_channel
			line += line_pin 
			line += line_pout
			data += line + '\n'
	return data

def include_flat_modified(data):
	input_file = path + flat_modified + extension
	with open(input_file, 'r') as f_in:
		entries = f_in.readlines()
	for j in range(0, len(entries)):
		auxiliary = entries[j].split()
		line = ""
		line_pin = ""
		line_pout = ""
		line += str(auxiliary[6]) + '\t'	# G_set
		for k in range(0, number_of_channels):
			line_pin += str(auxiliary[9+k]) + '\t'	# Pin_channel
			line_pout += str(auxiliary[49+k]) + '\t'	# Pout_channel
		line += line_pin 
		line += line_pout
		data += line + '\n'
	return data

# Reading all files
data = ""
data = read_files_for_1dB_step(data, tilts)
data = include_flat_modified(data)

# Writing output
with open(output_file, 'w') as f_out:
	f_out.writelines(data)

## Spectrum-Tilt
# output_file = "First EDFA/EDFA_1STG/Spectrum-Tilt/mask-edfa1-padtec-spectrum-with-tilt.txt"
output_file = "Second EDFA/EDFA_2STG/Spectrum-Tilt/mask-edfa2-padtec-spectrum-with-tilt.txt"

def read_files_for_1dB_step(data, tilts):
	for i in range(len(tilts)):
		# Positive mask
		input_file = path + str(tilts[i]) + dB + extension
		with open(input_file, 'r') as f_in:
			entries = f_in.readlines()
		for j in range(0, len(entries)):
			auxiliary = entries[j].split()
			line = ""
			line_pin = ""
			line_pout = ""
			line += str(auxiliary[6]) + '\t'	# G_set
			for k in range(0, number_of_channels):
				line_pin += str(auxiliary[9+k]) + '\t'	# Pin_channel
				line_pout += str(auxiliary[49+k]) + '\t'	# Pout_channel
			line += line_pin
			line += str(tilts[i]) + '\t'
			line += line_pout
			data += line + '\n'

		# Negative mask
		input_file = path + '-' + str(tilts[i]) + dB + extension
		with open(input_file, 'r') as f_in:
			entries = f_in.readlines()
		for j in range(0, len(entries)):
			auxiliary = entries[j].split()
			line = ""
			line_pin = ""
			line_pout = ""
			line += str(auxiliary[6]) + '\t'	# G_set
			for k in range(0, number_of_channels):
				line_pin += str(auxiliary[9+k]) + '\t'	# Pin_channel
				line_pout += str(auxiliary[49+k]) + '\t'	# Pout_channel
			line += line_pin
			line += '-' + str(tilts[i]) + '\t'
			line += line_pout
			data += line + '\n'
	return data

def include_flat_modified(data):
	input_file = path + flat_modified + extension
	with open(input_file, 'r') as f_in:
		entries = f_in.readlines()
	for j in range(0, len(entries)):
		auxiliary = entries[j].split()
		line = ""
		line_pin = ""
		line_pout = ""
		line += str(auxiliary[6]) + '\t'	# G_set
		for k in range(0, number_of_channels):
			line_pin += str(auxiliary[9+k]) + '\t'	# Pin_channel
			line_pout += str(auxiliary[49+k]) + '\t'	# Pout_channel
		line += line_pin
		line += str(0) + '\t'
		line += line_pout
		data += line + '\n'
	return data

# Reading all files
data = ""
data = read_files_for_1dB_step(data, tilts)
data = include_flat_modified(data)

# Writing output
with open(output_file, 'w') as f_out:
	f_out.writelines(data)