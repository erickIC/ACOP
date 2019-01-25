import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as mticker
from matplotlib import rcParams
rcParams['font.size'] = 14

#LossComp lauch power = 16,0206 dBm

f = open(os.path.abspath('launchPowers_e1.txt'), 'r+')
data = []
i = 0
fig = plt.figure(1)

for line in f:
	columns = line.split('\t')
	if columns[0] == '***' :
		ax = plt.subplot(2,1,i+1)
		plt.boxplot(data, 0, '')
		ax.text(.5, .9, columns[1], horizontalalignment='center', transform=ax.transAxes)
		#plt.xticks([1, 5, 10, 15, 20], [x[0], x[4], x[9], x[14], x[19]])
		#ax.set_xticklabels(x)
		i+=1
		data = []
	else:
		data.append(np.array([float(x) for x in line.split()]))
f.close()

fig.text(0.55, 0.04, 'Span Number', ha='center', va='center')
fig.text(0.04, 0.55, 'Span Lanch Power (dBm)', ha='center', va='center', rotation='vertical')
plt.subplots_adjust(left=0.13, bottom=0.15, right=0.96, top=1, wspace=0.18, hspace=0.2)
plt.show()
#figurePath = os.path.abspath('../graphs/IGD_8a.pdf')
#fig.savefig(figurePath, fomat='pdf')