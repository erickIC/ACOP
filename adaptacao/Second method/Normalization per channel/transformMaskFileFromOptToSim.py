'''
This code transforms the data returned by the OptiSystem to be used by the Optical Simulator.
It selects just the important columns and adds the wavelength columns.
'''

stringPath = "mask-edfa1-padtec.txt" #Output file
stringFile = "grouped-mask.txt" #input file

f = open(stringFile, 'r+')
fOut = open(stringPath, 'w')

fOut.write("40\n")	#The number of channels
for line in f:
	newLine = ""
	newLine2 = ""
	newLine3 = ""
	columns = line.split('\t')
	# Pin \t Pout \t Gset
	newLine += columns[0] + '\t' + columns[1] + '\t' + columns[6] + '\t'
	for i in range(40):
		newLine += columns[9+i] + '\t' #Pin_ch
		newLine2 += columns[49+i] + '\t' #Pout_ch
		newLine3 += columns[129+i] + '\t' #Noise Figure
	newLine += newLine2 + newLine3
	newLine += "1560.713	1559.794	1559.04	1558.187	1557.433	1556.613	1555.858	1555.038	1554.153	1553.398	1552.578	1551.758	1550.971	1550.02	1549.397	1548.61	1547.822	1547.002	1546.182	1545.395	1544.608	1543.788	1543.001	1542.214	1541.426	1540.639	1539.852	1538.966	1538.278	1537.425	1536.638	1535.883	1535.096	1534.342	1533.587	1532.8	1532.013	1531.226	1530.438	1529.651"
	fOut.write(newLine + '\n')
f.close()
fOut.close()