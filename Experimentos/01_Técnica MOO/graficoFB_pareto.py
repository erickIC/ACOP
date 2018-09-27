import os
import matplotlib.pyplot as plt

title = 'EDFA 2'
pasta1 = 'fb_e2_2a'
label1 = '2 Amps'
pasta2 = 'fb_e2_3a'
label2 = '3 Amps'
pasta3 = 'fb_e2_4a'
label3 = '4 Amps'
[osnrRipplePareto1, osnrPareto1] = readData(pasta1)
[osnrRipplePareto2, osnrPareto2] = readData(pasta2)
[osnrRipplePareto3, osnrPareto3] = readData(pasta3)

moo1 = 'nsgaii_e2_2a'
moo2 = 'nsgaii_e2_3a'
moo3 = 'nsgaii_e2_4a'
[osnrRippleMOO1, osnrMOO1] = readMOOData(moo1+'.txt')
[osnrRippleMOO2, osnrMOO2] = readMOOData(moo2+'.txt')
[osnrRippleMOO3, osnrMOO3] = readMOOData(moo3+'.txt')

figure1 = plt.figure(1)
plt.scatter(osnrRipplePareto1, osnrPareto1, c='green', s=5, zorder=3, label=label1+'_Pareto')
plt.scatter(osnrRipplePareto2, osnrPareto2, c='blue', s=5, zorder=3, label=label2+'_Pareto')
plt.scatter(osnrRipplePareto3, osnrPareto3, c='gold', s=5, zorder=3, label=label3+'_Pareto')
plt.scatter(osnrRippleMOO1, osnrMOO1, c='purple', marker='s',  s=5, zorder=3, label=moo1)
plt.scatter(osnrRippleMOO2, osnrMOO2, c='red', marker='s', s=5, zorder=3, label=moo2)
plt.scatter(osnrRippleMOO3, osnrMOO3, c='orange', marker='s', s=5, zorder=3, label=moo3)
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
