import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rcParams
rcParams['font.size'] = 14


markers = ['o', 'v', '^', '<', '>', 's', 'P']
plt.figure()

f = open(os.path.abspath('../hypervolume-2.txt'), 'r+')
y = []
yerr = [] 
i = 0
x = []
for line in f:
	columns = line.split('\t')
	if len(x) == 0:
		x = np.array([float(xL) for xL in line.split()])
		continue
		
	if columns[0] == '***' :
		plt.errorbar(x, y, yerr=yerr, fmt=markers[i], label=columns[1])
		i+=1
		x = []
		y = []
		yerr = [] 
	else:
		iterationTemp = np.array([float(x) for x in line.split()])
		y.append(np.mean(iterationTemp))
		yerr.append(np.std(iterationTemp))
f.close()

plt.xlabel('Number of Fitness Evaluations')
plt.ylabel('Inverted Generational Distance')
plt.grid(which='major', color='#d9d9d9', zorder=0)
plt.grid(which='minor', color='#d9d9d9', zorder=0, linestyle='--')
plt.legend()
plt.tight_layout(pad=0.5)
plt.show()