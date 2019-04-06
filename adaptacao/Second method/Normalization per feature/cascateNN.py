'''
    Reaseacher group: EASY Group.
    Oriented by : Professor Erick Barboza.
    Students: Allan Bezerra, Jose Carlos Pinheiro, Wagner Williams.
    Programmers: Allan Bezerra and Jose Carlos Pinheiro Filho.

    Description:
        Create a cascate using the model already trained in different scenarios.

    licensed under the GNU General Public License v3.0.
'''
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
from random import randint 
from keras import callbacks
from keras.layers import Dropout

def unnormalization(data, min, max, range_a, range_b):
	unnormalized_data = []
	
	values = []
	for j in range(0, data.shape[0]):
		values.append(((float(data[j]) - float(range_a)) * (float(max)-float(min))) / (float(range_b) - float(range_a)) + float(min))
	unnormalized_data.append(values)
	return np.array(unnormalized_data)
def normalization(x, min, max, range_a, range_b):	
	z = ( (float(range_b) - float(range_a)) * ( (x - float(min))/(float(max) - float(min)) ) ) + float(range_a)
	return z

wavelength = [1560.713, 1559.794, 1559.04, 1558.187, 1557.433, 1556.613, 
               1555.858, 1555.038, 1554.153, 1553.398, 1552.578, 1551.758,
               1550.971, 1550.02, 1549.397, 1548.61, 1547.822, 1547.002, 
               1546.182, 1545.395, 1544.608, 1543.788, 1543.001, 1542.214,
               1541.426, 1540.639, 1539.852, 1538.966, 1538.278, 1537.425, 
               1536.638, 1535.883, 1535.096, 1534.342, 1533.587, 1532.8, 
               1532.013, 1531.226, 1530.438, 1529.651]

## Taking information to normalization.

input_file = "min-max.txt"

with open(input_file, 'r') as f_in:
	lines = f_in.readlines()

	auxiliary = lines[0].split()
	max_gset = auxiliary[0]
	max_pin = auxiliary[1]
	max_pout = auxiliary[2]
	max_nf = auxiliary[3]

	auxiliary = lines[1].split()
	min_gset = auxiliary[0]
	min_pin = auxiliary[1]
	min_pout = auxiliary[2]
	min_nf = auxiliary[3]

	range_a = 0.15
	range_b = 0.85

## Load the model
model = load_model("model_pout.h5")

### First scenario

## Dataset 1 (G_set = 14 dB)
input_set_1 = "EDFA1STG_G=14dB@16dBm_Tilt=3.9_Maior_Precisão.xlsx"
dataframe_1 = pd.read_excel(input_set_1, usecols=range(0, 12), skiprows=range(0, 1), skipfooter=3)
#print(dataframe_1)

columns_1 = list(dataframe_1)
#print(len(dataframe_1[columns_1[1]]))



gain_1 = 14
loss_1 = gain_1

signal_current = []
gset_current = []

for i in range(0, len(dataframe_1[columns_1[1]])):
    signal_current.append(normalization(dataframe_1[columns_1[1]][i], min_pin, max_pin, range_a, range_b))
gset_current.append(normalization(gain_1, min_gset, max_gset, range_a, range_b))

gset_current = np.array([gset_current])
signal_current = np.array([signal_current])
diff_scenario1 = []
for i in range(2, len(columns_1)):
	
	#print(gset_current, signal_current)

	x_current = np.concatenate((gset_current,signal_current),axis=1)
	y_out = model.predict(x_current)

	y_out = unnormalization(y_out[0], min_pout, max_pout, range_a, range_b)

	#print(y_out)
	for j in range(0, y_out.shape[0]):
		diff_current = []
		for k in range(0, y_out.shape[1]):
			diff_current.append(abs(float(y_out[j][k]) - dataframe_1[columns_1[i]][k]))
		diff_scenario1.append(diff_current)
	signal_current = []
	gset_current = []
	for j in range(0, len(y_out)):
		signal_current.append(normalization((y_out[j] - loss_1), min_pin, max_pin, range_a, range_b))
	gset_current.append(normalization(gain_1, min_gset, max_gset, range_a, range_b))
	gset_current = np.array([gset_current])
	signal_current = np.array(signal_current)
#print(diff_scenario1)
plt.subplot(221)
plt.boxplot(diff_scenario1)
plt.title('Absolute difference First scenario')
plt.ylabel('(dB)')

plt.subplot(223)

plt.plot(wavelength, y_out[0], label='predicted pout')
plt.plot(wavelength, dataframe_1[columns_1[len(columns_1) - 1]], label='expected pout')
plt.ylabel('Pout (db)')
plt.legend()




### Second scenario


## Dataset 2 (G_set = 20dB)
input_set_2 = "EDFA1STG_G=20dB@16dBm_Tilt=-1.09_Maior_Precisão.xlsx"
dataframe_2 = pd.read_excel(input_set_2, usecols=range(0, 22), skiprows=range(0, 1))
#print(dataframe_2)

columns_2 = list(dataframe_2)
#print(columns_2)

gain_2 = 20
loss_2 = gain_2

signal_current = []
gset_current = []

for i in range(0, len(dataframe_2[columns_2[1]])):
    signal_current.append(normalization(dataframe_2[columns_2[1]][i], min_pin, max_pin, range_a, range_b))
gset_current.append(normalization(gain_2, min_gset, max_gset, range_a, range_b))

gset_current = np.array([gset_current])
signal_current = np.array([signal_current])
diff_scenario2 = []
for i in range(2, len(columns_2)):
	
	#print(gset_current, signal_current)

	x_current = np.concatenate((gset_current,signal_current),axis=1)
	y_out = model.predict(x_current)

	y_out = unnormalization(y_out[0], min_pout, max_pout, range_a, range_b)

	#print(y_out)
	for j in range(0, y_out.shape[0]):
		diff_current = []
		for k in range(0, y_out.shape[1]):
			diff_current.append(abs(float(y_out[j][k]) - dataframe_2[columns_2[i]][k]))
		diff_scenario2.append(diff_current)
	signal_current = []
	gset_current = []
	for j in range(0, len(y_out)):
		signal_current.append(normalization((y_out[j] - loss_2), min_pin, max_pin, range_a, range_b))
	gset_current.append(normalization(gain_2, min_gset, max_gset, range_a, range_b))
	gset_current = np.array([gset_current])
	signal_current = np.array(signal_current)
#print(diff_scenario1)
plt.subplot(222)
plt.boxplot(diff_scenario2)
plt.title('Absolute difference Second scenario')
plt.ylabel('(dB)')

plt.subplot(224)

plt.plot(wavelength, y_out[0], label='predicted pout')
plt.plot(wavelength, dataframe_2[columns_2[len(columns_2) - 1]], label='expected pout')
plt.ylabel('Pout (db)')
plt.legend()


plt.show()
### Third scenario


## Dataset 3 (variable G_set)
input_set_3 = "EDFA1STG_diferentes_Ganhos_G=14,24,...,14,24....xlsx"
dataframe_3 = pd.read_excel(input_set_3, usecols=range(0, 22), skiprows=range(0, 1))
#print(dataframe_3)

columns_3 = list(dataframe_3)
#print(columns_3)

# Getting gains and losses for each amplifier in the cascade
i = 0
gains_3 = [i] * (len(columns_3)-2)
losses_3 = [i] * (len(columns_3)-2)

gain_3 = re.findall('\d+', columns_3[2])
gains_3[i] = int(gain_3[0])
for amplifier in columns_3[3:]:
	i += 1
	loss_3, gain_3 = re.findall('\d+', amplifier[:-1])
	losses_3[i], gains_3[i] = int(loss_3), int(gain_3)

#print(gains_3)
#print(losses_3)