import numpy as np
from random import randint
from sklearn.svm import SVR
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error
import pickle
import matplotlib.pyplot as plt

def unnormalization(data, min, max, range_a, range_b):
	unnormalized_data = []
	for i in range(0, data.shape[0]):
		values = []
		for j in range(0, data.shape[1]):
			values.append(((float(data[i][j]) - float(range_a)) * (float(max)-float(min))) / (float(range_b) - float(range_a)) + float(min))
		unnormalized_data.append(values)
	return np.array(unnormalized_data)

### Reading file with normalized data and putting data in an matrix
input_file = "mask-edfa1-padtec-modified-normalized.txt"

with open(input_file, 'r') as f_in:
	data = []
	caught = []
	lines = f_in.readlines()
	for i in range(0, len(lines)):
		aux = lines[i].split()
		for j in range(0, len(aux)):
			aux[j] = float(aux[j])
		data.append(aux)
		caught.append(0)
data = np.array(data)

### FIRST METHOD
# ### Separating the data into training (80%) and testing set (20%)
# eighty_percent = int(0.8 * data.shape[0])

# # Training set
# array_x = []
# array_y = []

# while len(array_x) != eighty_percent:
# 	current = randint(0, len(caught)-1)
# 	if caught[current] == 0:
# 		auxiliary = data[current]
# 		array_x.append(auxiliary[:41])
# 		array_y.append(auxiliary[41:])
# 		caught[current] = 1

# # Test set
# array_xt = []
# array_yt = []

# for i in range(0, len(caught)):
# 	if caught[i] == 0:
# 		auxiliary = data[i]
# 		array_xt.append(auxiliary[:41])
# 		array_yt.append(auxiliary[41:])
# 		caught[i] = 1

### SECOND METHOD
### Using all data for training set and 20% for the test set
twenty_percent = int(0.2 * data.shape[0])

# Training set 1
array_x = []
array_y = []

for i in range(0, data.shape[0]):
	auxiliary = data[i]
	array_x.append(auxiliary[:41])
	array_y.append(auxiliary[41:])

training_x1 = np.array(array_x)
training_y1 = np.array(array_y)

# Training set 2
array_x = []
array_y = []

for i in range(2):
	for j in range(i, data.shape[0], 2):
		auxiliary = data[j]
		array_x.append(auxiliary[:41])
		array_y.append(auxiliary[41:])

training_x2 = np.array(array_x)
training_y2 = np.array(array_y)

# Training set 3
array_x = []
array_y = []

for i in range(3):
	for j in range(i, data.shape[0], 3):
		auxiliary = data[j]
		array_x.append(auxiliary[:41])
		array_y.append(auxiliary[41:])

training_x3 = np.array(array_x)
training_y3 = np.array(array_y)

# Training set 4
array_x = []
array_y = []

for i in range(4):
	for j in range(i, data.shape[0], 4):
		auxiliary = data[j]
		array_x.append(auxiliary[:41])
		array_y.append(auxiliary[41:])

training_x4 = np.array(array_x)
training_y4 = np.array(array_y)

# Training set 5
array_x = []
array_y = []

for i in range(5):
	for j in range(i, data.shape[0], 5):
		auxiliary = data[j]
		array_x.append(auxiliary[:41])
		array_y.append(auxiliary[41:])

training_x5 = np.array(array_x)
training_y5 = np.array(array_y)

# Training set 6
array_x = []
array_y = []

for i in range(6):
	for j in range(i, data.shape[0], 6):
		auxiliary = data[j]
		array_x.append(auxiliary[:41])
		array_y.append(auxiliary[41:])

training_x6 = np.array(array_x)
training_y6 = np.array(array_y)

# Training set 7
array_x = []
array_y = []

for i in range(7):
	for j in range(i, data.shape[0], 7):
		auxiliary = data[j]
		array_x.append(auxiliary[:41])
		array_y.append(auxiliary[41:])

training_x7 = np.array(array_x)
training_y7 = np.array(array_y)

# Test set
array_xt = []
array_yt = []

while len(array_xt) != twenty_percent:
	current = randint(0, len(caught)-1)
	if caught[current] == 0:
		auxiliary = data[current]
		array_xt.append(auxiliary[:41])
		array_yt.append(auxiliary[41:])
		caught[current] = 1

test_x = np.array(array_xt)
test_y = np.array(array_yt)

### Building SVR and running regression
svr = SVR(kernel='poly', degree=3, gamma='auto', coef0=1, epsilon=0.01)
svr_t = MultiOutputRegressor(svr)

svr_t1 = svr_t.fit(training_x1, training_y1)
svr_t2 = svr_t.fit(training_x2, training_y2)
svr_t3 = svr_t.fit(training_x3, training_y3)
svr_t4 = svr_t.fit(training_x4, training_y4)
svr_t5 = svr_t.fit(training_x5, training_y5)
svr_t6 = svr_t.fit(training_x6, training_y6)
svr_t7 = svr_t.fit(training_x7, training_y7)

# Saving models for later use
with open('svr_model_1.pkl', 'wb') as f:
	pickle.dump(svr_t1, f)

with open('svr_model_2.pkl', 'wb') as f:
	pickle.dump(svr_t2, f)

with open('svr_model_3.pkl', 'wb') as f:
	pickle.dump(svr_t3, f)

with open('svr_model_4.pkl', 'wb') as f:
	pickle.dump(svr_t4, f)

with open('svr_model_5.pkl', 'wb') as f:
	pickle.dump(svr_t5, f)

with open('svr_model_6.pkl', 'wb') as f:
	pickle.dump(svr_t6, f)

with open('svr_model_7.pkl', 'wb') as f:
	pickle.dump(svr_t7, f)

y_out = svr_t1.predict(test_x)

### Calculating training error (MSE - Mean Squared Error)
print('Mean Squared Error Regression Loss:')

# P_Out
error = mean_squared_error(test_y[:, :40], y_out[:, :40], multioutput='uniform_average')
print('Pout:', error)

# Noise Figure
error = mean_squared_error(test_y[:, 40:], y_out[:, 40:], multioutput='uniform_average')
print('NF:', error)

### De-normalizing data
input_file = "min-max.txt"

with open(input_file, 'r') as f_in:
	lines = f_in.readlines()

	auxiliary = lines[0].split()
	max_pout = auxiliary[2]
	max_nf = auxiliary[3]

	auxiliary = lines[1].split()
	min_pout = auxiliary[2]
	min_nf = auxiliary[3]

	range_a = 0.15
	range_b = 0.85

pout_pred = unnormalization(y_out[:, :40], min_pout, max_pout, range_a, range_b)
pout_test = unnormalization(test_y[:, :40], min_pout, max_pout, range_a, range_b)
nf_pred = unnormalization(y_out[:, 40:], min_nf, max_nf, range_a, range_b)
nf_test = unnormalization(test_y[:, 40:], min_nf, max_nf, range_a, range_b)

### Calculating test error (absolute error) and saving best, average and worst cases
diff_pout = []
diff_nf = []

biggest_pout = 0
smallest_pout = float('inf')
biggest_nf = 0
smallest_nf = float('inf')

biggest_pout_id = 0
biggest_nf_id = 0
median_pout_id = 0
median_nf_id = 0
smallest_pout_id = 0
smallest_nf_id = 0

for i in range(0, pout_pred.shape[0]):
	pout_current = float(0)
	nf_current = float(0)
	for j in range(0, pout_pred.shape[1]):
		pout_current += abs(pout_pred[i][j] - pout_test[i][j])
		nf_current += abs(nf_pred[i][j] - nf_test[i][j])
	diff_pout.append(pout_current/pout_pred.shape[1])
	if pout_current/pout_pred.shape[1] < smallest_pout:
		smallest_pout = pout_current/pout_pred.shape[1]
		smallest_pout_id = i
	if pout_current/pout_pred.shape[1] > biggest_pout:
		biggest_pout = pout_current/pout_pred.shape[1]
		biggest_pout_id = i
	diff_nf.append(nf_current/pout_pred.shape[1])
	if nf_current/pout_pred.shape[1] < smallest_nf:
		smallest_nf = nf_current/pout_pred.shape[1]
		smallest_nf_id = i
	if nf_current/pout_pred.shape[1] > biggest_nf:
		biggest_nf = nf_current/pout_pred.shape[1]
		biggest_nf_id = i

for i in range(0, len(diff_pout)):
	if np.median(diff_pout) == diff_pout[i]:
		median_pout_id = i
	if np.median(diff_nf) == diff_nf[i]:
		median_nf_id = i

wavelength = [1560.713, 1559.794, 1559.04, 1558.187, 1557.433, 1556.613, 
				1555.858, 1555.038, 1554.153, 1553.398, 1552.578, 1551.758,
				1550.971, 1550.02, 1549.397, 1548.61, 1547.822, 1547.002, 
				1546.182, 1545.395, 1544.608, 1543.788, 1543.001, 1542.214,
				1541.426, 1540.639, 1539.852, 1538.966, 1538.278, 1537.425, 
				1536.638, 1535.883, 1535.096, 1534.342, 1533.587, 1532.8, 
				1532.013, 1531.226, 1530.438, 1529.651]

### Plotting results (boxplot)
plt.subplot(211)
plt.boxplot(diff_pout)
plt.title('Potência de saída')
plt.xticks([])
plt.ylabel("dB")

plt.subplot(212)
plt.boxplot(diff_nf)
plt.title('Noise Figure')
plt.xticks([])
plt.ylabel("dB")

plt.show()

### Plotting best (lower average error), average (median average error) and worst (biggest average error) cases
plt.figure(figsize=(50,24))

plt.subplot(321)
plt.plot(wavelength, pout_pred[biggest_pout_id], label='prevista')
plt.plot(wavelength, pout_test[biggest_pout_id], label='esperada')
plt.xlabel('Comprimento de onda')
plt.ylabel('POut (dB)')
plt.title('Potência de saída (pior caso)')
plt.legend()

plt.subplot(322)
plt.plot(wavelength, nf_pred[biggest_nf_id], label='prevista')
plt.plot(wavelength, nf_test[biggest_nf_id], label='esperada')
plt.xlabel('Comprimento de onda')
plt.ylabel('NF (dB)')
plt.title('Noise Figure (pior caso)')
plt.legend()

plt.subplot(323)
plt.plot(wavelength, pout_pred[median_pout_id], label='prevista')
plt.plot(wavelength, pout_test[median_pout_id], label='esperada')
plt.xlabel('Comprimento de onda')
plt.ylabel('POut (dB)')
plt.title('Potência de saída (caso mediano)')
plt.legend()

plt.subplot(324)
plt.plot(wavelength, nf_pred[median_nf_id], label='prevista')
plt.plot(wavelength, nf_test[median_nf_id], label='esperada')
plt.xlabel('Comprimento de onda')
plt.ylabel('NF (dB)')
plt.title('Noise Figure (caso mediano)')
plt.legend()

plt.subplot(325)
plt.plot(wavelength, pout_pred[smallest_pout_id], label='prevista')
plt.plot(wavelength, pout_test[smallest_pout_id], label='esperada')
plt.xlabel('Comprimento de onda')
plt.ylabel('POut (dB)')
plt.title('Potência de saída (melhor caso)')
plt.legend()

plt.subplot(326)
plt.plot(wavelength, nf_pred[smallest_nf_id], label='prevista')
plt.plot(wavelength, nf_test[smallest_nf_id], label='esperada')
plt.xlabel('Comprimento de onda')
plt.ylabel('NF (dB)')
plt.title('Noise Figure (melhor caso)')
plt.legend()

plt.show()