import matplotlib.pyplot as plt

#Definir g e a
g = '27'
a = '5'

freq = []
pin =[]
pout=[]
nf=[]
gain=[]

#Ler arquivos Pin, Pout e NF
pinFile = open("PinPeak_G"+g+"_A"+a+".txt", 'r')
for line in pinFile:
	str = line.split('\t')
	freq.append(3e8/(float(str[0])*1e3))
	pin.append(float(str[1]))
pinFile.close()

poutFile = open("PoutPeak_G"+g+"_A"+a+".txt", 'r')
for line in poutFile:
	str = line.split('\t')
	pout.append(float(str[1]))
poutFile.close()

nfFile = open("NF_G"+g+"_A"+a+".txt", 'r')
for line in nfFile:
	str = line.split('\t')
	nf.append(str[1])
nfFile.close()		

#Plotar os gráficos
fig1 = plt.figure(1)
pinPlot, = plt.plot(freq, pin, 'o-', linewidth=2, label='Input Power')
poutPlot, = plt.plot(freq, pout, 'o-', linewidth=2, label='Output Power')
plt.legend(handles=[pinPlot, poutPlot])
plt.title('Power Spectrum')
plt.xlabel('Frequency (THz)')
plt.ylabel('Power (dBm)')
fig1.show()

fig2 = plt.figure(2)
gain = [i - j for i, j in zip(pout, pin)]
plt.plot(freq, gain, 'o-', linewidth=2)
plt.title('Gain')
plt.xlabel('Frequency (THz)')
plt.ylabel('Gain (dB)')
fig2.show()

fig3 = plt.figure(3)
plt.plot(freq, nf, 'o-', linewidth=2)
plt.title('Noise Figure')
plt.xlabel('Frequency (THz)')
plt.ylabel('NF (dB)')
fig3.show()

input()