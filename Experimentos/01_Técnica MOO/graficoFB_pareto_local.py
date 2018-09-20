import os
import matplotlib.pyplot as plt

def readData(pasta):
	osnrRipplePareto = []
	osnrPareto = []
	caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]
	arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
	par = [arq for arq in arquivos if arq.lower().endswith("_par.txt")]
	for file in par:
		f = open(file, 'r+')
		for line in f:
			str = line.split('\t')
			if file.lower().endswith("pareto_par.txt"):
				osnrRipplePareto.append(str[0].replace(',', '.'))
				osnrPareto.append(str[1].replace(',', '.'))
		f.close()
	return osnrRipplePareto, osnrPareto
	
#TODO: fazer uma implementação top-down
	
def compareByDominance(solution1, solution2):
	lostInAllDimensions = True
	winInAllDimensions = True
	for i in len(solution1):
		if i == 1: #OSNR
			solution1 *= -1
			solution2 *= -1
		
		if solution1[i] > solution2[i]: winInAllDimensions = False
		if solution1[i] < solution2[i]: lostInAllDimensions = False
		
		if i == 1: #OSNR
			solution1 *= -1
			solution2 *= -1
			
		if not winInAllDimensions and not lostInAllDimensions: return 0 #incomparable
	
	if winInAllDimensions and lostInAllDimensions: return -1 #equal
	if winInAllDimensions: return 1 #sl1 dominates sl2
	if lostInAllDimensions: return -1 #sl1 is dominated by sl2
	
	return 0
	
def addToPareto(candidateSolution, pareto):
	for i in len(pareto):		
		#A solution inside the pareto dominates the candidate solution
		if compareByDominance(pareto[i], candidateSolution) == 1: break
			
			#A solution inside the pareto is dominated by the candidate solution
			#Remove the dominated solution
			tempRipple = []
			tempOsnr = []
			if compareByDominance(candidateSolution, paretoSolution) != -1:
				tempRipple.append(candidateSolution[0])
				tempOsnr.append(candidateSolution[1])
			
			osnrRippleRet.append(osnrRipple)
			
		osnrRippleRetTemp = []
		osnrRetTemp = []
		for j in len(osnrRet):
			if i == 0: continue
			paretoSolution = [float(osnrRippleRet[i]), float(osnrRet[i])]
			candidateSolution = [float(osnrRipple[j]), float(osnr[j])]
			
			
			
		
			
	
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

title = 'EDFA 1 - 4 amplifiers'
stringFile = 'e1_4a'
#Pareto front
pasta1 = 'fb_' + stringFile
[osnrRipplePareto1, osnrPareto1] = readData(pasta1)
		
#Pareto MOO
moo1 = 'nsgaii_' + stringFile
[osnrRippleMOO1, osnrMOO1] = readMOOData(moo1+'.txt')

#Tecnicas locais
#e1_4a
maxGain = [0.475, 17.950]
adgc = [0.673, 25.739]
adgc_nli = [0.593, 26.722]
ashbflex = [0.607, 21.988]
ashbflex_nli = [0.090, 24.798]
losscomp = [2.111, 24.721]

figure1 = plt.figure(1)
plt.scatter(osnrRipplePareto1, osnrPareto1, color='r', s=3, linewidths=3, zorder=3, label='Pareto Front')
plt.scatter(osnrRippleMOO1, osnrMOO1, s=5, zorder=3, label=moo1)
plt.scatter(maxGain[0], maxGain[1], marker='o', zorder=3, label='MaxGain')
plt.scatter(adgc[0], adgc[1], marker='s', zorder=3, label='AdGC')
plt.scatter(adgc_nli[0], adgc_nli[1], marker='^', zorder=3, label='AdGC-NLI')
plt.scatter(ashbflex[0], ashbflex[1], marker='v', zorder=3, label='AsHBFlex')
plt.scatter(ashbflex_nli[0], ashbflex_nli[1], marker='D', zorder=3, label='AsHBFlex-NLI')
plt.scatter(losscomp[0], losscomp[1], marker='*', zorder=3, label='LossComp')
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
