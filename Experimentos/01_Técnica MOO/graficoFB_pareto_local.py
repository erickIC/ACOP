import os
from typing import List

import matplotlib.pyplot as plt
import FB_read_data as reader

title = 'EDFA 1 - 4 amplifiers'
stringFile = 'e1_4a'
#Pareto front
pasta1 = 'fb_' + stringFile
[osnrRipplePareto1, osnrPareto1] = reader.read_pareto(pasta1)
		
#Pareto MOO
moo1 = 'nsgaii_' + stringFile
[osnrRippleMOO1, osnrMOO1] = reader.read_data_file(moo1 + '.txt')

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
