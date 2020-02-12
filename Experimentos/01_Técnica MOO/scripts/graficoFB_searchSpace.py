import os
import matplotlib.pyplot as plt
from scripts import FB_read_data as reader

fbDir = '../fb/'
graphDir = '../graphs/'
paretoDir = '../paretos/'

title = 'EDFA 1'
#pasta1 = 'fb_e2_2a'
#label1 = '2 Amps'
#pasta2 = 'fb_e2_3a'
#label2 = '3 Amps'
pasta2 = 'fb_e1_2a_woVOA'
label2 = '2 Amps'
pasta3 = 'fb_e1_2a'
label3 = '2 Amps with VOA'
figurePath = os.path.abspath(graphDir + 'fb_wVOA_woVOA_e1_2a.png')
#[osnrRipple1, osnr1] = reader.read_data(pasta1)
[osnrRipple2, osnr2] = reader.read_data(os.path.abspath(fbDir+pasta2))
[osnrRipple3, osnr3] = reader.read_data(os.path.abspath(fbDir+pasta3))

#moo1 = paretoDir + pasta1 + '_pareto.txt'
moo2 = paretoDir + pasta2 + '_pareto.txt'
moo3 = paretoDir + pasta3 + '_pareto.txt'
#[osnrRippleMOO1, osnrMOO1] = reader.read_data_file(os.path.abspath(moo1))
[osnrRipplePareto2, osnrPareto2] = reader.read_data_file(os.path.abspath(moo2))
[osnrRipplePareto3, osnrPareto3] = reader.read_data_file(os.path.abspath(moo3))

figure1 = plt.figure(1)
#plt.scatter(osnrRipple1, osnr1, c='lime', s=3, zorder=3, label=label1)
plt.scatter(osnrRipple2, osnr2, c='cyan', s=3, zorder=3, label=label2)
plt.scatter(osnrRipple3, osnr3, c='yellow', s=3, zorder=2, label=label3)
#plt.scatter(osnrRippleMOO1, osnrMOO1, marker='s', c='purple', s=3, zorder=3, label=label1+' Pareto')
plt.scatter(osnrRipplePareto2, osnrPareto2, marker='s', c='red', s=6, zorder=3, label=label2 + ' Pareto')
plt.scatter(osnrRipplePareto3, osnrPareto3, marker='s', c='orange', s=6, zorder=2, label=label3 + ' Pareto')
plt.ylabel('min(OSNR ASE+NLI) (dB)')
plt.xlabel('Ripple OSNR ASE+NLI(dB)')
plt.legend()
plt.title(title)
plt.grid(True, zorder=0)
plt.tight_layout(pad=0.5)
xLimts = plt.gca().get_xlim()
yLimts = plt.gca().get_ylim()
#figure1.show()
figure1.savefig(figurePath, dpi = 200)