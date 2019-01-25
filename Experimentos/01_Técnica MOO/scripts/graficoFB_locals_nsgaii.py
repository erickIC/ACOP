import os
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as plticker
from scripts import FB_read_data as reader
from scripts import locals

'''
Reading Data
'''
#Directories
fbDir = '../fb/'
graphDir = '../graphs/'
nsgaDir = '../nsgaii/'
#Data identification
title = 'EDFA 2 - 8 amplifiers'
stringFile = 'e2_8a'
#Local Approachs
[maxGain, adgc, adgc_nli, ashbflex, ashbflex_nli, lossComp] = locals.getLocalApproachResults(stringFile)
#NSGAII
file = 'nsgaii_' + stringFile + ".txt"
nsgaii = reader.read_data_file(os.path.abspath(nsgaDir+file))

'''
Creating Figure
'''
fontSize = 18
font = {'size'   : fontSize}

matplotlib.rc('font', **font)
mrk_size = 12

fig, ax = plt.subplots()
ax.plot(nsgaii[0], nsgaii[1], zorder=3, markersize=mrk_size, color='blue', marker='o', markerfacecolor='white', linestyle='none', label='MOO')
ax.plot(maxGain[0], maxGain[1], markersize=mrk_size, marker='s', linestyle='none', zorder=3, label='MaxGain')
ax.plot(adgc[0], adgc[1], markersize=mrk_size, marker='v', linestyle='none', zorder=3, label='AdGC')
ax.plot(adgc_nli[0], adgc_nli[1], markersize=mrk_size, marker='P', linestyle='none', zorder=3, label='AdGC NLI')
ax.plot(ashbflex[0], ashbflex[1], markersize=mrk_size, marker='D', linestyle='none', zorder=3, label='AsHB')
ax.plot(ashbflex_nli[0], ashbflex_nli[1], markersize=mrk_size, marker='^', linestyle='none', zorder=3, label='AsHB NLI')
ax.plot(lossComp[0], lossComp[1], markersize=mrk_size, marker='<', linestyle='none', zorder=3, label='LossComp')
if stringFile == 'e2_8a':
    ax.legend(ncol=2, shadow=True, fancybox=True, fontsize=(fontSize-1), loc=4)
plt.ylabel('min(OSNR ASE+NLI) (dB)')
plt.xlabel('Ripple OSNR ASE+NLI(dB)')
#plt.legend()
plt.title(title)

loc = plticker.MultipleLocator(base=2.5)
ax.yaxis.set_minor_locator(loc)
plt.grid(which='major', zorder=0)
plt.grid(which='minor', zorder=0, linestyle='--')
plt.tight_layout(pad=0.5)
xLimts = plt.gca().get_xlim()
yLimts = plt.gca().get_ylim()
if stringFile.split('_')[0] == 'e1':
    plt.xlim(-0.1, 4.7)  # edfa_1
    plt.ylim(13.5, 25.5)
else:
    plt.xlim(0.1, 1.12)  # edfa_2
    plt.ylim(0.5, 24.5)
#fig.show()
figurePath = os.path.abspath(graphDir + 'moo_locals_' + stringFile + '_.pdf')
fig.savefig(figurePath, fomat='pdf')