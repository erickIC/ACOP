import pandas as pd
import pickle
import re
import numpy as np
import matplotlib.pyplot as plt

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

### Load SVR model
with open('svr_model.pkl', 'rb') as f:
	svr_t = pickle.load(f)

### Load info for normalization
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

# Wavelength for use in plot
wavelength = [1560.713, 1559.794, 1559.04, 1558.187, 1557.433, 1556.613, 
               1555.858, 1555.038, 1554.153, 1553.398, 1552.578, 1551.758,
               1550.971, 1550.02, 1549.397, 1548.61, 1547.822, 1547.002, 
               1546.182, 1545.395, 1544.608, 1543.788, 1543.001, 1542.214,
               1541.426, 1540.639, 1539.852, 1538.966, 1538.278, 1537.425, 
               1536.638, 1535.883, 1535.096, 1534.342, 1533.587, 1532.8, 
               1532.013, 1531.226, 1530.438, 1529.651]

### Dataset 1 (G_set = 14 dB)
input_set_1 = "EDFA1STG_G=14dB@16dBm_Tilt=3.9_Maior_Precisão.xlsx"
dataframe_1 = pd.read_excel(input_set_1, usecols=range(0, 12), skiprows=range(0, 1), skipfooter=3)

columns_1 = list(dataframe_1)

gain_1 = 14
loss_1 = gain_1

# Normalizing first input data
g_set = []
g_set.append(normalization(gain_1, min_gset, max_gset, range_a, range_b))

p_in = []
for i in range(0, len(dataframe_1[columns_1[1]])):
    p_in.append(normalization(dataframe_1[columns_1[1]][i], min_pin, max_pin, range_a, range_b))

g_set = np.array([g_set])
p_in = np.array([p_in])

diff_dataframe1 = []

# Cascade
for i in range(2, len(columns_1)):
	# Building input
	x_in = np.concatenate((g_set, p_in), axis=1)

	# Predicting P_out
	y_out = svr_t.predict(x_in)
	y_out = y_out[:, :40]
	
	# De-normalizing data
	y_out = unnormalization(y_out[0], min_pout, max_pout, range_a, range_b)

	# Calculating error at current amplifier
	diff_current = []
	for j in range(0, y_out.shape[1]):
		diff_current.append(abs(float(y_out[0][j]) - dataframe_1[columns_1[i]][j]))
	diff_dataframe1.append(diff_current)

	# Normalizing next input in cascade
	p_in = []
	for j in range(0, y_out.shape[1]):
		p_in.append(normalization((y_out[0][j] - loss_1), min_pin, max_pin, range_a, range_b))
	p_in = np.array([p_in])

# Plotting results (boxplot cascade)
plt.subplot(231)
plt.boxplot(diff_dataframe1)
plt.title('Absolute difference (scenario 1)')
plt.ylabel('P_Out (dB)')
plt.xlabel('Amplifier')

plt.subplot(234)
plt.plot(wavelength, y_out[0], label='predicted')
plt.plot(wavelength, dataframe_1[columns_1[len(columns_1) - 1]], label='expected')
plt.ylabel('P_Out (dB)')
plt.xlabel('Wavelenght')
plt.legend()

## Dataset 2 (G_set = 20dB)
input_set_2 = "EDFA1STG_G=20dB@16dBm_Tilt=-1.09_Maior_Precisão.xlsx"
dataframe_2 = pd.read_excel(input_set_2, usecols=range(0, 22), skiprows=range(0, 1))

columns_2 = list(dataframe_2)

gain_2 = 20
loss_2 = gain_2

# Normalizing first input data
g_set = []
g_set.append(normalization(gain_2, min_gset, max_gset, range_a, range_b))

p_in = []
for i in range(0, len(dataframe_2[columns_2[1]])):
    p_in.append(normalization(dataframe_2[columns_2[1]][i], min_pin, max_pin, range_a, range_b))

g_set = np.array([g_set])
p_in = np.array([p_in])

diff_dataframe2 = []

# Cascade
for i in range(2, len(columns_2)):
	# Building input
	x_in = np.concatenate((g_set, p_in), axis=1)

	# Predicting P_out
	y_out = svr_t.predict(x_in)
	y_out = y_out[:, :40]
	
	# De-normalizing data
	y_out = unnormalization(y_out[0], min_pout, max_pout, range_a, range_b)

	# Calculating error at current amplifier
	diff_current = []
	for j in range(0, y_out.shape[1]):
		diff_current.append(abs(float(y_out[0][j]) - dataframe_2[columns_2[i]][j]))
	diff_dataframe2.append(diff_current)

	# Normalizing next input in cascade
	p_in = []
	for j in range(0, y_out.shape[1]):
		p_in.append(normalization((y_out[0][j] - loss_2), min_pin, max_pin, range_a, range_b))
	p_in = np.array([p_in])

# Plotting results (boxplot cascade)
plt.subplot(232)
plt.boxplot(diff_dataframe2)
plt.title('Absolute difference (scenario 2)')
plt.ylabel('P_Out (dB)')
plt.xlabel('Amplifier')

plt.subplot(235)
plt.plot(wavelength, y_out[0], label='predicted')
plt.plot(wavelength, dataframe_2[columns_2[len(columns_2) - 1]], label='expected')
plt.ylabel('P_Out (dB)')
plt.xlabel('Wavelenght')
plt.legend()

## Dataset 3 (variable G_set)
input_set_3 = "EDFA1STG_diferentes_Ganhos_G=14,24,...,14,24....xlsx"
dataframe_3 = pd.read_excel(input_set_3, usecols=range(0, 22), skiprows=range(0, 1))

columns_3 = list(dataframe_3)

# Getting gains and losses for each amplifier in the cascade
i = 0
gains_3 = [i] * (len(columns_3)-1)
losses_3 = [i] * (len(columns_3)-1)

gain_3 = re.findall('\d+', columns_3[2])
gains_3[i] = int(gain_3[0])
for amplifier in columns_3[3:]:
	i += 1
	loss_3, gain_3 = re.findall('\d+', amplifier[:-1])
	losses_3[i], gains_3[i] = int(loss_3), int(gain_3)

# Normalizing first input data
g_set = []
g_set.append(normalization(gains_3[0], min_gset, max_gset, range_a, range_b))

p_in = []
for i in range(0, len(dataframe_3[columns_3[1]])):
    p_in.append(normalization(dataframe_3[columns_3[1]][i], min_pin, max_pin, range_a, range_b))

g_set = np.array([g_set])
p_in = np.array([p_in])

diff_dataframe3 = []

# Cascade
for i in range(2, len(columns_3)):
	# Building input
	x_in = np.concatenate((g_set, p_in), axis=1)

	# Predicting P_out
	y_out = svr_t.predict(x_in)
	y_out = y_out[:, :40]
	
	# De-normalizing data
	y_out = unnormalization(y_out[0], min_pout, max_pout, range_a, range_b)

	# Calculating error at current amplifier
	diff_current = []
	for j in range(0, y_out.shape[1]):
		diff_current.append(abs(float(y_out[0][j]) - dataframe_3[columns_3[i]][j]))
	diff_dataframe3.append(diff_current)

	# Normalizing next input in cascade
	g_set = []
	g_set.append(normalization(gains_3[i-1], min_gset, max_gset, range_a, range_b))
	g_set = np.array([g_set])

	p_in = []
	for j in range(0, y_out.shape[1]):
		p_in.append(normalization((y_out[0][j] - losses_3[i-1]), min_pin, max_pin, range_a, range_b))
	p_in = np.array([p_in])

# Plotting results (boxplot cascade)
plt.subplot(233)
plt.boxplot(diff_dataframe3)
plt.title('Absolute difference (scenario 3)')
plt.ylabel('P_Out (dB)')
plt.xlabel('Amplifier')

plt.subplot(236)
plt.plot(wavelength, y_out[0], label='predicted')
plt.plot(wavelength, dataframe_3[columns_3[len(columns_3) - 1]], label='expected')
plt.ylabel('P_Out (dB)')
plt.xlabel('Wavelenght')
plt.legend()

plt.show()