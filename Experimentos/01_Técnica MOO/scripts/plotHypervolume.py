import numpy as np
import matplotlib.pyplot as plt
import matplotlib

fontSize = 14
font = {'family' : 'normal',
        'size'   : fontSize}

matplotlib.rc('font', **font)

x = [100, 200, 300, 400, 500, 750, 1000]
markers = ['o', 'v', '^', '<', '>']
plt.figure()

f = open('hypervolume.txt', 'r+')
y = []
yerr = [] 
i = 0
for line in f:
	columns = line.split('\t')
	if columns[0] == '***' :
		plt.errorbar(x, y, yerr=yerr, fmt=markers[i], label=columns[1])
		i+=1
		y = []
		yerr = [] 
	else:
		iterationTemp = np.array([float(x) for x in line.split()])
		y.append(np.mean(iterationTemp))
		yerr.append(np.std(iterationTemp))
f.close()

plt.xlabel('Iterations', fontsize=fontSize)
plt.ylabel('Hypervolume', fontsize=fontSize)
plt.grid(which='major', color='#d9d9d9', zorder=0)
plt.grid(which='minor', color='#d9d9d9', zorder=0, linestyle='--')
plt.legend()
plt.tight_layout(pad=0.3)
plt.show()