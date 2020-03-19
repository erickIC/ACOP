'''
Get all .txt files in the EDFA_1STG folder and join them in a single one
'''

import os
import glob

# Input folder and output file
folder_path = os.getcwd() + '/EDFA_2STG'
output_file = 'result_allMask_40channels_EDFA2STG_All_Tilts.txt'

# Reads all files and writes into output
with open(output_file, 'w') as f_out:
	for filename in glob.glob(os.path.join(folder_path, '*.txt')):
		with open(filename, 'r') as f_in:
			f_out.write(f_in.read())