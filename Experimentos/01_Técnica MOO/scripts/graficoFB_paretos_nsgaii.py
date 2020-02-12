import os
import matplotlib.pyplot as plt
import matplotlib.markers as mrk
from scripts import FB_read_data as reader
from matplotlib import rcParams
rcParams['font.size'] = 18

'''
Reading Data
'''
#Directories
nsgaDir = '../nsgaii/'
graphDir = '../graphs/'
paretoDir = '../paretos/'
#Data identification
title = 'EDFA 1'
stringFile2 = 'e1_2a'
stringFile3 = 'e1_3a'
stringFile4 = 'e1_4a'
#Pareto FB
sufix = '_pareto.txt'
file = 'fb_' + stringFile2 + sufix
[osnrRipple2, osnr2] = reader.read_data_file(os.path.abspath(paretoDir+file))
file = 'fb_' + stringFile3 + sufix
[osnrRipple3, osnr3] = reader.read_data_file(os.path.abspath(paretoDir+file))
file = 'fb_' + stringFile4 + sufix
[osnrRipple4, osnr4] = reader.read_data_file(os.path.abspath(paretoDir+file))
#Pareto nsgaii
file = 'nsgaii_' + stringFile2 + ".txt"
nsgaii2 = reader.read_data_file(os.path.abspath(nsgaDir+file))
file = 'nsgaii_' + stringFile3 + ".txt"
nsgaii3 = reader.read_data_file(os.path.abspath(nsgaDir+file))
file = 'nsgaii_' + stringFile4 + ".txt"
nsgaii4 = reader.read_data_file(os.path.abspath(nsgaDir+file))

'''
Creating Figure
'''

mrk_size = 10

fig, ax = plt.subplots()
ax.plot(osnrRipple2, osnr2, zorder=2, markersize=mrk_size, color='blue', marker='o', linestyle='none', label='2 Amps EM')
ax.plot(nsgaii2[0], nsgaii2[1], zorder=3, markersize=mrk_size-2, color='blue', marker='o', markerfacecolor='white', linestyle='none', label='2 Amps MOO')
ax.plot(osnrRipple3, osnr3, zorder=2, markersize=mrk_size, color='orange', marker='s', linestyle='none', label='3 Amps EM')
ax.plot(nsgaii3[0], nsgaii3[1], zorder=3, markersize=mrk_size-2, color='orange', marker='s', markerfacecolor='white', linestyle='none', label='3 Amps MOO')
ax.plot(osnrRipple4, osnr4, zorder=2, markersize=mrk_size, color='green', marker='^', linestyle='none', label='4 Amps EM')
ax.plot(nsgaii4[0], nsgaii4[1], zorder=3, markersize=mrk_size-2, color='green', marker='^', markerfacecolor='white', linestyle='none', label='4 Amps MOO')
plt.ylabel('min(OSNR ASE+NLI) (dB)')
plt.xlabel('Ripple OSNR ASE+NLI(dB)')
#plt.legend()
plt.title(title)
plt.grid(True, zorder=1)
plt.tight_layout(pad=0.5)
#fig.show()
figurePath = os.path.abspath(graphDir + 'paretos_moo_' + title + '.pdf')
fig.savefig(figurePath, format='pdf')