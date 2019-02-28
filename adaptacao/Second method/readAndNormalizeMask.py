'''
Made on base of previous code provide by Professor Erick Barboza.
This code transforms the data returned by the OptiSystem to be used to train the NN or SVR before normalization.
It selects just the Gch, Pin_ch, Pout_ch and NF.
It creates a file that contains the minimums and maximums of each column selected.
'''
def normalization(x, min, max, range_a, range_b):
	
	z = ( (float(range_b) - float(range_a)) * ( (x - float(min))/(float(max) - float(min)) ) ) + float(range_a)
	return z

string_path = "data-pout.txt" #Output file relative to pout
string_path2 = "data-nf.txt" #Output file relative to noise figure
string_path3 = "maxnmin-pout.txt" #Output file relative to maximus and minimums of pout
string_path4 = "maxnmin-nf.txt" #Output file relative to maximus and minimums of noise figure
string_file = "grouped-mask.txt" #input file

f = open(string_file, 'r+')
f_dpout = open(string_path, 'w')
f_dnf = open(string_path2, 'w')
f_mpout = open(string_path3, 'w')
f_mnf = open(string_path4, 'w')


#array to get the minimus and maximus to normalization Gch Pin_ch[0:39] Pout_ch[0:39] NF 
maximums_pout = [-float('inf')] * 81 
minimums_pout = [float('inf')] * 81

maximums_nf = [-float('inf')] * 81 
minimums_nf = [float('inf')] * 81

lines_pout = []
lines_nf = []


################### Separating the data ###########################
for line in f:

	columns = line.split('\t')
	
	new_line_pout = [float(0)] * 81
	new_line_nf = [float(0)] * 81

	#Gset
	new_line_pout[0] = float(columns[6])
	new_line_nf[0] = float(columns[6])

	if maximums_pout[0] < new_line_pout[0]:
		maximums_pout[0] = new_line_pout[0]
		maximums_nf[0] = new_line_nf[0]
	if minimums_pout[0] > new_line_pout[0]:
		minimums_pout[0] = new_line_pout[0]
		minimums_nf[0] = new_line_nf[0]
		

	for i in range(40):
		#Pin_ch
		new_line_pout[1+i] = float(columns[9+i])
		new_line_nf[1+i] = float(columns[9+i])

		if maximums_pout[1+i] < new_line_pout[1+i]:
			maximums_pout[1+i] = new_line_pout[1+i]
			maximums_nf[1+i] = new_line_nf[1+i]
		if minimums_pout[1+i] > new_line_pout[1+i]:
			minimums_pout[1+i] = new_line_pout[1+i]
			minimums_nf[1+i] = new_line_nf[1+i]

		#Pout_ch
		new_line_pout[41+i] = float(columns[49+i])

		if maximums_pout[41+i] < new_line_pout[41+i]:
			maximums_pout[41+i] = new_line_pout[41+i]
		if minimums_pout[41+i] > new_line_pout[41+i]:
			minimums_pout[41+i] = new_line_pout[41+i]

		#Noise Figure
		new_line_nf[41+i] = float(columns[129+i])

		if maximums_nf[41+i] < new_line_nf[41+i]:
			maximums_nf[41+i] = new_line_nf[41+i]
		if minimums_nf[41+i] > new_line_nf[41+i]:
			minimums_nf[41+i] = new_line_nf[41+i]
	#print(len(new_line_pout), '\n', new_line_pout)		
	lines_pout.append(new_line_pout)
	lines_nf.append(new_line_nf)


##################### Writing the max and min files ############################
string_max = ''
string_min = ''

for i in range(len(minimums_pout)):
	string_max += str(maximums_pout[i]) + '\t'
	string_min += str(minimums_pout[i]) + '\t'

string_max += '\n' + string_min + '\n'

f_mpout.writelines(string_max)

string_max = ''
string_min = ''

for i in range(len(minimums_nf)):
	string_max += str(maximums_nf[i]) + '\t'
	string_min += str(minimums_nf[i]) + '\t'

string_max += '\n' + string_min + '\n'

f_mnf.writelines(string_max)

################### Normalizing the data ####################
range_a = 0.15
range_b = 0.85

for i in range(len(lines_pout)): #Writing the pout file
	current = lines_pout[i]
	linetowrite = ''
	for j in range(len(current)):
		linetowrite += str(normalization(current[j], minimums_pout[j], maximums_pout[j], range_a, range_b)) + '\t'
	f_dpout.write(linetowrite + '\n')

for i in range(len(lines_pout)): #Writing the nf file
	current = lines_nf[i]
	linetowrite = ''
	for j in range(len(current)):
		linetowrite += str(normalization(current[j], minimums_nf[j], maximums_nf[j], range_a, range_b)) + '\t'
	f_dnf.write(linetowrite + '\n')

f.close()
f_mnf.close()
f_mpout.close()
f_dpout.close()
f_dnf.close()