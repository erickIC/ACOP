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
paretoDir = '../paretos/'
#Data identification
title = 'EDFA 1 - 2 amplifiers'
stringFile = 'e1_2a'
#Pareto without VOA
wo_VOA_file = 'fb_' + stringFile + '_woVOA_pareto.txt'
[osnrRipple1, osnr1] = reader.read_data_file(os.path.abspath(paretoDir+ wo_VOA_file))
#Pareto with VOA
VOA_file = 'fb_' + stringFile + '_pareto.txt'
[osnrRipple2, osnr2] = reader.read_data_file(os.path.abspath(paretoDir+ VOA_file))
#Local Approachs
[maxGain, adgc, adgc_nli, ashbflex, ashbflex_nli, lossComp] = locals.getLocalApproachResults(stringFile)

'''
Creating Figure
'''
fontSize = 18
font = {'family' : 'normal',
        'size'   : fontSize}

matplotlib.rc('font', **font)
mrk_size = 12

fig, ax = plt.subplots()
ax.plot(osnrRipple1, osnr1, markersize=mrk_size, marker='o', linestyle='none', zorder=1, label='EM Without VOA')
ax.plot(osnrRipple2, osnr2, markersize=mrk_size, marker='*', linestyle='none', zorder=2, label='EM With VOA')
ax.plot(maxGain[0], maxGain[1], markersize=mrk_size, marker='s', linestyle='none', zorder=3, label='MaxGain')
ax.plot(adgc[0], adgc[1], markersize=mrk_size, marker='v', linestyle='none', zorder=3, label='AdGC')
ax.plot(adgc_nli[0], adgc_nli[1], markersize=mrk_size, marker='P', linestyle='none', zorder=3, label='AdGC NLI')
ax.plot(ashbflex[0], ashbflex[1], markersize=mrk_size, marker='D', linestyle='none', zorder=3, label='AsHB')
ax.plot(ashbflex_nli[0], ashbflex_nli[1], markersize=mrk_size, marker='^', linestyle='none', zorder=3, label='AsHB NLI')
ax.plot(lossComp[0], lossComp[1], markersize=mrk_size, marker='<', linestyle='none', zorder=3, label='LossComp')
if stringFile == 'e2_2a':
    ax.legend(ncol=2, shadow=True, fancybox=True, fontsize=(fontSize-1), loc=4)
plt.ylabel('min(OSNR ASE+NLI) (dB)')
plt.xlabel('Ripple OSNR ASE+NLI(dB)')
#plt.legend()
plt.title(title)

#loc = plticker.MultipleLocator(base=2.5)
#ax.yaxis.set_minor_locator(loc)
plt.grid(which='major', zorder=0)
plt.grid(which='minor', zorder=0, linestyle='--')
plt.tight_layout(pad=0.5)
xLimts = plt.gca().get_xlim()
yLimts = plt.gca().get_ylim()
if stringFile.split('_')[0] == 'e1':
    plt.xlim(-0.1, 1.1)  # edfa_1
    plt.ylim(17.5, 31.5)
else:
    plt.xlim(0.16, 1.12)  # edfa_2
    plt.ylim(12, 30)
#figure1.show()
figurePath = os.path.abspath(graphDir + 'paretos_locals_' + stringFile + '_.pdf')
fig.savefig(figurePath, fomat='pdf')