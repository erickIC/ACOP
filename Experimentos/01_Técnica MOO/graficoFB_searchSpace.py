import os
import matplotlib.pyplot as plt
import FB_read_data as reader

title = 'EDFA 1'
pasta1 = 'fb_e1_2a'
label1 = '2 Amps'
pasta2 = 'fb_e1_3a'
label2 = '3 Amps'
pasta3 = 'fb_e1_4a'
label3 = '4 Amps'
[osnrRipple1, osnr1] = reader.read_data(pasta1)
[osnrRipple2, osnr2] = reader.read_data(pasta2)
[osnrRipple3, osnr3] = reader.read_data(pasta3)

moo1 = pasta1+'_pareto.txt'
moo2 = pasta2+'_pareto.txt'
moo3 = pasta3+'_pareto.txt'
[osnrRippleMOO1, osnrMOO1] = reader.read_data_file(moo1)
[osnrRippleMOO2, osnrMOO2] = reader.read_data_file(moo2)
[osnrRippleMOO3, osnrMOO3] = reader.read_data_file(moo3)

figure1 = plt.figure(1)
plt.scatter(osnrRipple1, osnr1, c='lime', s=3, zorder=3, label=label1)
plt.scatter(osnrRipple2, osnr2, c='cyan', s=3, zorder=3, label=label2)
plt.scatter(osnrRipple3, osnr3, c='yellow', s=3, zorder=3, label=label3)
plt.scatter(osnrRippleMOO1, osnrMOO1, marker='s', c='purple', s=3, zorder=3, label=moo1)
plt.scatter(osnrRippleMOO2, osnrMOO2, marker='s', c='red', s=3, zorder=3, label=moo2)
plt.scatter(osnrRippleMOO3, osnrMOO3, marker='s', c='orange', s=3, zorder=3, label=moo3)
plt.ylabel('min(OSNR ASE+NLI) (dB)')
plt.xlabel('Ripple OSNR ASE+NLI(dB)')
plt.legend()
plt.title(title)
plt.grid(True, zorder=0)
plt.tight_layout(pad=0.5)
xLimts = plt.gca().get_xlim()
yLimts = plt.gca().get_ylim()
#figure1.show()
figure1.savefig(title+'.png', dpi = 200)
