import numpy as np
from numpy import median
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from keras.models import load_model
import math
import pickle

def normalization(x, min, max, range_a, range_b):	
	z = ( (float(range_b) - float(range_a)) * ( (x - float(min))/(float(max) - float(min)) ) ) + float(range_a)
	return z

def unnormalization(data, min, max, range_a, range_b):
	unnormalized_data = []
	
	values = []
	for j in range(0, data.shape[0]):
		values.append(((float(data[j]) - float(range_a)) * (float(max)-float(min))) / (float(range_b) - float(range_a)) + float(min))
	unnormalized_data.append(values)
	return np.array(unnormalized_data)

smaller_size = 12
medium_size = 20
bigger_size = 30
plt.rc('font', size=bigger_size)             # controls default text sizes
plt.rc('axes', titlesize=bigger_size)        # fontsize of the axes title
plt.rc('axes', labelsize=bigger_size)        # fontsize of the x and y labels
plt.rc('xtick', labelsize=bigger_size)      # fontsize of the tick labels
plt.rc('ytick', labelsize=bigger_size)      # fontsize of the tick labels
plt.rc('legend', fontsize=medium_size)       # legend fontsize
plt.rc('figure', titlesize=bigger_size)      # fontsize of the figure title

input_file = "masks/mask-edfa1-padtec-new-models-infov2.txt"

with open(input_file, 'r') as f_in:

    lines = f_in.readlines()
    auxiliary = lines[0].split()
    max_gset = float(auxiliary[0])
    max_pin = float(auxiliary[1])
    max_tilt = float(auxiliary[2])
    max_pout = float(auxiliary[3])

    auxiliary = lines[1].split()
    min_gset = float(auxiliary[0])
    min_pin = float(auxiliary[1])
    min_tilt = float(auxiliary[2])
    min_pout = float(auxiliary[3])

    auxiliary = lines[2].split()
    range_a = auxiliary[0]
    range_b = auxiliary[1]

    print(max_gset, min_gset, max_pout, min_pout, range_a, range_b)



file = open('biggestTIP.obj', 'rb')

worstcase = pickle.load(file)

print(worstcase['biggest_global'])
x_input = worstcase['biggest_input']
print(x_input)

x_input_norm = [normalization(x_input[0], min_gset, max_gset, range_a, range_b)]
x_input_norm1 = [normalization(x_input[0], min_gset, max_gset, range_a, range_b)]

for i in range(1, len(x_input)):
    x_input_norm.append(normalization(x_input[i], min_pin, max_pin, range_a, range_b))
    x_input_norm1.append(normalization(x_input[i], min_pin, max_pin, range_a, range_b))


x_input_norm.append(normalization((x_input[1] - x_input[40]), min_tilt, max_tilt, range_a, range_b))

print('Tilt é' + str(x_input[1] - x_input[40]))
print(x_input_norm)

x_input_norm = np.array([x_input_norm])
x_input_norm2 = np.array([x_input_norm1])

model_name = 'models/nn-42to40v21.h5'
model_current = load_model(model_name)

model_name = 'models/nn-41to40v21.h5'
model_current2 = load_model(model_name)

y = model_current.predict(x_input_norm)
y2 = model_current2.predict(x_input_norm2)

print(y)
out_42to40 = unnormalization(model_current.predict(x_input_norm)[0], min_pout, max_pout, range_a, range_b)[0]
print(out_42to40)

out_41to40 = unnormalization(model_current2.predict(x_input_norm2)[0], min_pout, max_pout, range_a, range_b)[0]
print(out_42to40)




plt.figure(figsize=(10,8))
plt.plot(worstcase['wavelength'], worstcase['biggest_pred'],'o-' ,label='TIP', linewidth=4, markersize = 10)
plt.plot(worstcase['wavelength'], out_42to40,'o-' ,label='Spectrum', linewidth=4, markersize = 10)
plt.plot(worstcase['wavelength'], out_41to40,'o-' ,label='Spectrum-tilt', linewidth=4, markersize = 10)
plt.plot(worstcase['wavelength'], worstcase['biggest_test'],'o-' ,label='Expected', linewidth=4, markersize = 10)

plt.ylabel('Output Power (dBm)')
plt.xlabel('Wavelenght (nm)')
plt.tight_layout()
plt.legend()
plt.grid(True)
plt.savefig('plots/EDFA1TIPWorst.png', dpi = 200)
