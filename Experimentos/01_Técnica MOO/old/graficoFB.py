import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

font = {'size'   : 12}

matplotlib.rc('font', **font)

xLimts = [4,18]
yLimts = [20,26.5]

## Brute force without VOA ##
f = open('LI_edfa1_nliEase_-21_par.txt', 'r+')

ripple = []
osnrNLI = []
osnrASE = []

for line in f:
	str = line.split('\t')
	ripple.append(str[0].replace(',', '.'))
	osnrASE.append(str[1].replace(',', '.'))
	osnrNLI.append(str[2].replace(',', '.'))
f.close()

maxGain = [13.0938549041748, 25.80701799730836, 20.827602316706248]
adgc = [13.0938549041748, 25.80701799730836, 20.827602316706248]
ashb = [14.223958969116218, 23.120611514010776, 22.815980275684606]
lossComp = [17.498676300048825, 20.656265017165243, 20.5767313049875]

#figure1 = plt.figure(1)
ax1 = plt.subplot(221)
ax1.text(0.5,-0.12, "(a)", size=12, ha="center", transform=ax1.transAxes)
plt.scatter(ripple, osnrASE, c='lime', s=3, zorder=3, label='Exhaustive Method')
plt.scatter(adgc[0], adgc[1],  s=50, zorder=3, marker='s', label='AdGC')
plt.scatter(maxGain[0], maxGain[1], s=50, zorder=3, marker='o', label='MaxGain')
plt.scatter(ashb[0], ashb[1], s=50, zorder=3, marker='^', label='AsHB')
plt.scatter(lossComp[0], lossComp[1], s=50, zorder=3, marker='D', label='LossComp')
axes = plt.gca()
axes.xaxis.set_ticklabels([])
plt.ylabel('min(OSNR ASE) (dB)')
plt.title('Without VOA')
plt.grid(True, zorder=0)
plt.gca().set_xlim(xLimts)
plt.gca().set_ylim(yLimts)
plt.legend(bbox_to_anchor=(-0.2, 1.15, 2.5, .2), loc=3, ncol=3, mode="expand", borderaxespad=0.4)
#figure1.show()
#figure1.savefig(stringPath + 'semVOA-ASE.pdf', dpi = 300)

ax1 = plt.subplot(223)
plt.scatter(ripple, osnrNLI, c='aqua', s=3, zorder=3, label='Exhaustive Method')
plt.scatter(adgc[0], adgc[2],  s=50, zorder=3, marker='s', label='AdGC')
plt.scatter(maxGain[0], maxGain[2], s=50, zorder=3, marker='o', label='MaxGain')
plt.scatter(ashb[0], ashb[2], s=50, zorder=3, marker='^', label='AsHB')
plt.scatter(lossComp[0], lossComp[2], s=50, zorder=3, marker='D', label='LossComp')
axes = plt.gca()
plt.ylabel('min(OSNR ASE+NLI) (dB)')
plt.xlabel('Ripple (dB)')
ax1.text(0.5,-0.35, "(c)", size=12, ha="center", transform=ax1.transAxes)
plt.grid(True, zorder=0)
plt.gca().set_xlim(xLimts)
plt.gca().set_ylim(yLimts)

## Brute force with VOA ##
f = open('LI_edfa1_nliEase_-21_res0dBm_par.txt', 'r+')

ripple = []
osnrNLI = []
osnrASE = []

for line in f:
	str = line.split('\t')
	ripple.append(str[0].replace(',', '.'))
	osnrASE.append(str[1].replace(',', '.'))
	osnrNLI.append(str[2].replace(',', '.'))
f.close()

maxGain = [4.93381309509277, 25.943655095174126, 24.92082548970012]
adgc = [4.93381309509277, 25.943655095174126, 24.92082548970012]
ashb = [8.738229751586903, 24.363480874750195, 24.053976756380504]
lossComp = [17.498676300048825, 20.656265017165243, 20.5767313049875]

ax1 = plt.subplot(222)
plt.scatter(ripple, osnrASE, c='lime', s=3, zorder=3, label='Exhaustive Method')
plt.scatter(adgc[0], adgc[1],  s=50, zorder=3, marker='s', label='AdGC')
plt.scatter(maxGain[0], maxGain[1], s=50, zorder=3, marker='o', label='MaxGain')
plt.scatter(ashb[0], ashb[1], s=50, zorder=3, marker='^', label='AsHB')
plt.scatter(lossComp[0], lossComp[1], s=50, zorder=3, marker='D', label='LossComp')
axes = plt.gca()
axes.xaxis.set_ticklabels([])
axes.yaxis.set_ticklabels([])
plt.title('With VOA')
ax1.text(0.5,-0.12, "(b)", size=12, ha="center", transform=ax1.transAxes)
plt.grid(True, zorder=0)
plt.gca().set_xlim(xLimts)
plt.gca().set_ylim(yLimts)

ax1 = plt.subplot(224)
plt.scatter(ripple, osnrNLI, c='aqua', s=3, zorder=3, label='Exhaustive Method')
plt.scatter(adgc[0], adgc[2],  s=50, zorder=3, marker='s', label='AdGC')
plt.scatter(maxGain[0], maxGain[2], s=50, zorder=3, marker='o', label='MaxGain')
plt.scatter(ashb[0], ashb[2], s=50, zorder=3, marker='^', label='AsHB')
plt.scatter(lossComp[0], lossComp[2], s=50, zorder=3, marker='D', label='LossComp')
axes = plt.gca()
axes.yaxis.set_ticklabels([])
plt.xlabel('Ripple (dB)')
ax1.text(0.5,-0.35, "(d)", size=12, ha="center", transform=ax1.transAxes)
plt.grid(True, zorder=0)
plt.gca().set_xlim(xLimts)
plt.gca().set_ylim(yLimts)
plt.show()