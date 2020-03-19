import numpy as np
from random import randint
from sklearn.svm import SVR
import copy as cp
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

### Using all data for training set and 20% for the test set
twenty_percent = int(0.2 * data.shape[0])

# Training set
array_x = []
array_y = []

for i in range(0, data.shape[0]):
	auxiliary = data[i]
	array_x.append(auxiliary[:41])
	array_y.append(auxiliary[41:81])

training_x = np.array(array_x)
training_y = np.array(array_y)

# Test set
array_xt = []
array_yt = []

while len(array_xt) != twenty_percent:
	current = randint(0, len(caught)-1)
	if caught[current] == 0:
		auxiliary = data[current]
		array_xt.append(auxiliary[:41])
		array_yt.append(auxiliary[41:81])
		caught[current] = 1

test_x = np.array(array_xt)
test_y = np.array(array_yt)

### Building a SVR model for each channel
svr = SVR(kernel='poly', degree=3, gamma='auto', coef0=1, epsilon=0.01)

svr_model = [0] * training_y.shape[1]

for j in range(0, training_y.shape[1]):
	svr_model[j] = cp.deepcopy(svr.fit(training_x, training_y[:, j]))

### Running regression and capturing error for each instance
y_out = np.zeros((test_x.shape[0], test_y.shape[1]))

for i in range(0, test_x.shape[0]):
	for j in range(0, test_y.shape[1]):
		y_out[i, j] = svr_model[j].predict(test_x[i].reshape(1,-1))

# De-normalizing data
pout_pred = unnormalization(y_out[:], min_pout, max_pout, range_a, range_b)
pout_test = unnormalization(test_y[:], min_pout, max_pout, range_a, range_b)

### Calculating test error (absolute error) and saving best, average and worst cases
diff_pout = []

biggest_pout = 0
smallest_pout = float('inf')

biggest_pout_id = 0
median_pout_id = 0
smallest_pout_id = 0

for i in range(0, pout_pred.shape[0]):
	pout_current = float(0)
	for j in range(0, pout_pred.shape[1]):
		pout_current += abs(pout_pred[i][j] - pout_test[i][j])
	diff_pout.append(pout_current/pout_pred.shape[1])
	if pout_current/pout_pred.shape[1] < smallest_pout:
		smallest_pout = pout_current/pout_pred.shape[1]
		smallest_pout_id = i
	if pout_current/pout_pred.shape[1] > biggest_pout:
		biggest_pout = pout_current/pout_pred.shape[1]
		biggest_pout_id = i

for i in range(0, len(diff_pout)):
	if np.median(diff_pout) == diff_pout[i]:
		median_pout_id = i

wavelength = [1560.713, 1559.794, 1559.04, 1558.187, 1557.433, 1556.613, 
				1555.858, 1555.038, 1554.153, 1553.398, 1552.578, 1551.758,
				1550.971, 1550.02, 1549.397, 1548.61, 1547.822, 1547.002, 
				1546.182, 1545.395, 1544.608, 1543.788, 1543.001, 1542.214,
				1541.426, 1540.639, 1539.852, 1538.966, 1538.278, 1537.425, 
				1536.638, 1535.883, 1535.096, 1534.342, 1533.587, 1532.8, 
				1532.013, 1531.226, 1530.438, 1529.651]

### Set the font sizes to the plots
smaller_size = 8
medium_size = 10
bigger_size = 16
plt.rc('font', size=medium_size)             # controls default text sizes
plt.rc('axes', titlesize=medium_size)        # fontsize of the axes title
plt.rc('axes', labelsize=medium_size)        # fontsize of the x and y labels
plt.rc('xtick', labelsize=smaller_size)      # fontsize of the tick labels
plt.rc('ytick', labelsize=smaller_size)      # fontsize of the tick labels
plt.rc('legend', fontsize=smaller_size)       # legend fontsize
plt.rc('figure', titlesize=medium_size)      # fontsize of the figure title

### Plotting results (boxplot)
plt.boxplot(diff_pout)
plt.title('Potência de saída')
plt.xticks([])
plt.ylabel("dB")

plt.savefig('modelPerChannel_SVR_Boxplot.png', dpi = 200)
plt.show()

### Plotting best (lower average error), average (median average error) and worst (biggest average error) cases
plt.figure(figsize=(50,24))

plt.subplot(311)
plt.plot(wavelength, pout_pred[biggest_pout_id], label='prevista')
plt.plot(wavelength, pout_test[biggest_pout_id], label='esperada')
plt.xlabel('Comprimento de onda')
plt.ylabel('POut (dB)')
plt.title('Potência de saída (pior caso)')
plt.legend()

plt.subplot(312)
plt.plot(wavelength, pout_pred[median_pout_id], label='prevista')
plt.plot(wavelength, pout_test[median_pout_id], label='esperada')
plt.xlabel('Comprimento de onda')
plt.ylabel('POut (dB)')
plt.title('Potência de saída (caso mediano)')
plt.legend()

plt.subplot(313)
plt.plot(wavelength, pout_pred[smallest_pout_id], label='prevista')
plt.plot(wavelength, pout_test[smallest_pout_id], label='esperada')
plt.xlabel('Comprimento de onda')
plt.ylabel('POut (dB)')
plt.title('Potência de saída (melhor caso)')
plt.legend()

plt.savefig('modelPerChannel_SVR_Comparison.png', dpi = 200)
plt.show()