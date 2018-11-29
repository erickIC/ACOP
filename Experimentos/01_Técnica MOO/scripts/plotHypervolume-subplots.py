import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as mticker
from matplotlib import rcParams
rcParams['font.size'] = 14


markers = ['o', 'v', '^', '<', '>', 's', 'P']
plt.figure()

f = open(os.path.abspath('../hypervolume-e1-e2-8a.txt'), 'r+')
y = []
yerr = [] 
i = 0
x = []

fig = plt.figure(1)
for line in f:
	columns = line.split('\t')
	if len(x) == 0:
		x = np.array([float(xL) for xL in line.split()])
		continue
		
	if columns[0] == '***' :
		plt.subplot(2,1,i+1)
		plt.errorbar(x, y, yerr=yerr, fmt=markers[i], label=columns[1])
		fo = mticker.ScalarFormatter(useOffset=False, useMathText=True)
		g = lambda x,pos : "${}$".format(fo._formatSciNotation('%1.10e' % x))
		plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(g))
		plt.legend()
		plt.grid(which='major', color='#d9d9d9', zorder=0)
		plt.grid(which='minor', color='#d9d9d9', zorder=0, linestyle='--')
		i+=1
		x = []
		y = []
		yerr = [] 
	else:
		iterationTemp = np.array([float(x) for x in line.split()])
		y.append(np.mean(iterationTemp))
		yerr.append(np.std(iterationTemp))
f.close()

fig.text(0.5, 0.04, 'Number of Fitness Evaluations', ha='center', va='center')
fig.text(0.04, 0.55, 'Inverted Generational Distance', ha='center', va='center', rotation='vertical')
plt.subplots_adjust(left=0.16, bottom=0.15, right=0.95, top=0.98, wspace=0.2, hspace=0.36)
#plt.show()
figurePath = os.path.abspath('../graphs/IGD_8a.pdf')
fig.savefig(figurePath, fomat='pdf')