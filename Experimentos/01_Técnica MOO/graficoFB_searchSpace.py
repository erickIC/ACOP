import os
import matplotlib.pyplot as plt

def readData(pasta):
	osnrRipple = []
	osnr = []
	caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]
	arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
	par = [arq for arq in arquivos if arq.lower().endswith("_par.txt")]
	for file in par:
		f = open(file, 'r+')
		for line in f:
			str = line.split('\t')
			if not(file.lower().endswith("pareto_par.txt")):
				osnrRipple.append(str[0].replace(',', '.'))
				osnr.append(str[1].replace(',', '.'))
		f.close()
	return osnrRipple, osnr;
	
def readMOOData(arquivo):
	osnrRipple = []
	osnr = []
	f = open(arquivo, 'r+')
	for line in f:
		str = line.split('\t')
		osnrRipple.append(str[0].replace(',', '.'))
		osnr.append(str[1].replace(',', '.'))
	f.close()
	return osnrRipple, osnr
		

title = 'EDFA 2'
pasta1 = 'fb_e2_2a'
label1 = '2 Amps'
pasta2 = 'fb_e2_3a'
label2 = '3 Amps'
pasta3 = 'fb_e2_4a'
label3 = '4 Amps'
[osnrRipple1, osnr1] = readData(pasta1)
[osnrRipple2, osnr2] = readData(pasta2)
[osnrRipple3, osnr3] = readData(pasta3)

moo1 = 'nsgaii_e1_2a'
moo2 = 'nsgaii_e1_3a'
moo3 = 'nsgaii_e1_4a'
[osnrRippleMOO1, osnrMOO1] = readMOOData(moo1+'.txt')
[osnrRippleMOO2, osnrMOO2] = readMOOData(moo2+'.txt')
[osnrRippleMOO3, osnrMOO3] = readMOOData(moo3+'.txt')

figure1 = plt.figure(1)
plt.scatter(osnrRipple1, osnr1, c='lime', s=3, zorder=3, label=label1)
plt.scatter(osnrRipple2, osnr2, c='cyan', s=3, zorder=3, label=label2)
plt.scatter(osnrRipple3, osnr3, c='yellow', s=3, zorder=3, label=label3)
#plt.scatter(osnrRippleMOO1, osnrMOO1, c='purple', s=3, zorder=3, label=moo1)
#plt.scatter(osnrRippleMOO2, osnrMOO2, c='red', s=3, zorder=3, label=moo2)
#plt.scatter(osnrRippleMOO3, osnrMOO3, c='orange', s=3, zorder=3, label=moo3)
plt.ylabel('min(OSNR ASE+NLI) (dB)')
plt.xlabel('Ripple OSNR ASE+NLI(dB)')
plt.legend()
plt.title(title)
plt.grid(True, zorder=0)
plt.tight_layout(pad=0.5)
xLimts = plt.gca().get_xlim()
yLimts = plt.gca().get_ylim()
figure1.show()
#figure1.savefig(pasta+'.png', dpi = 200)
