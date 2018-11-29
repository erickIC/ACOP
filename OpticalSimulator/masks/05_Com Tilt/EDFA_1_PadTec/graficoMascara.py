import matplotlib
import matplotlib.pyplot as plt

fontSize = 20
font = {'family' : 'normal',
        'size'   : fontSize}

matplotlib.rc('font', **font)

f = open('TotalInfo.txt', 'r+')

pin = []
pout = []
nf =[]
rp=[]

for line in f:
	columns = line.split()
	gain = int(columns[0])
	pinVal = float(columns[2])
	pin.append(pinVal)
	pout.append(gain+pinVal)
	nf.append(float(columns[4]))
	rp.append(float(columns[5]))
f.close()

nfMax = max(nf)
nfMin = min(nf)
rpMax = max(rp)
rpMin = min(rp)

fig1 = plt.figure(1)
plt.scatter(pin, pout, c=nf, cmap='jet', zorder=3)
plt.title('Power Mask: Noise Figure', fontsize=fontSize)
plt.xlabel('Total Input Power (dBm)', fontsize=fontSize)
plt.ylabel('Total Output Power (dBm)', fontsize=fontSize)
plt.grid(color='#d9d9d9', zorder=0)
xRef = plt.gca().get_xlim()[0] + 1
yRef = plt.gca().get_ylim()[1] - 5
text = "Max = %.2fdB\nMin = %.2fdB" % (nfMax, nfMin)
plt.text(xRef, yRef, text, fontsize=fontSize-1)
plt.tight_layout(pad=0.3)
clb = plt.colorbar()
#clb.set_label('Noise Figure (dB)')
#fig1.show()
fig1.savefig('EDFA_1_NF.pdf', fomat='pdf')

fig2 = plt.figure(2)
plt.scatter(pin, pout, c=rp, cmap='jet', zorder=3)
plt.title('Power Mask: Power Ripple', fontsize=fontSize)
plt.xlabel('Total Input Power (dBm)', fontsize=fontSize)
plt.ylabel('Total Output Power (dBm)', fontsize=fontSize)
xRef = plt.gca().get_xlim()[0] + 1
yRef = plt.gca().get_ylim()[1] - 5
text = "Max = %.2fdB\nMin = %.2fdB" % (rpMax, rpMin)
plt.text(xRef, yRef, text, fontsize=fontSize-1)
plt.grid(color='#d9d9d9', zorder=0)
plt.colorbar()
plt.tight_layout(pad=0.3)
#fig2.show()
fig2.savefig('EDFA_1_Rp.pdf', fomat='pdf')