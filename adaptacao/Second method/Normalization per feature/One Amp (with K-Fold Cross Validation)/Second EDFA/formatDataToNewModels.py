input_file = "masks/mask-edfa2-padtec.txt"
output_file = "masks/mask-edfa2-padtec-new-models.txt"

# Formatting data to match new models
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
			tilt = float(columns[3]) - float(columns[3 + number_of_channels-1]) # Tilt
			new_line += str(tilt) + '\t' + new_line2 + new_line3
			f_out.write(new_line + '\n')