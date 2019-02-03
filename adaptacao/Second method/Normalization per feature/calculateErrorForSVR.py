import numpy as np
from random import randint
from sklearn.svm import SVR
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error
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

### Separating the data into training (80%) and testing set (20%)
eighty_percent = int(0.8 * data.shape[0])

# Training set
array_x = []
array_y = []

while len(array_x) != eighty_percent:
	current = randint(0, len(caught)-1)
	if caught[current] == 0:
		auxiliary = data[current]
		array_x.append(auxiliary[:41])
		array_y.append(auxiliary[41:])
		caught[current] = 1

# Test set
array_xt = []
array_yt = []

for i in range(0, len(caught)):
	if caught[i] == 0:
		auxiliary = data[i]
		array_xt.append(auxiliary[:41])
		array_yt.append(auxiliary[41:])
		caught[i] = 1

training_x = np.array(array_x)
training_y = np.array(array_y)
test_x = np.array(array_xt)
test_y = np.array(array_yt)

### Building SVR and running regression
svr = SVR(kernel='rbf', C=1e3, gamma=0.2)

svr_t = MultiOutputRegressor(svr)
y_out = svr_t.fit(training_x, training_y).predict(test_x)

### Calculating training error (MSE - Mean Squared Error)
print('Mean Squared Error Regression Loss:')

# P_Out
error = mean_squared_error(test_y[:, :40], y_out[:, :40], multioutput='uniform_average')
print('Gch:', error)

# Noise Figure
error = mean_squared_error(test_y[:, 40:], y_out[:, 40:], multioutput='uniform_average')
print('NF:', error)

### De-normalizing data
input_file = "min-max.txt"

with open(input_file, 'r') as f_in:
	lines = f_in.readlines()

	auxiliary = lines[0].split()
	max_gch = auxiliary[2]
	max_nf = auxiliary[3]

	auxiliary = lines[1].split()
	min_gch = auxiliary[2]
	min_nf = auxiliary[3]

	range_a = 0.15
	range_b = 0.85

gch_pred = unnormalization(y_out[:, :40], min_gch, max_gch, range_a, range_b)
gch_test = unnormalization(test_y[:, :40], min_gch, max_gch, range_a, range_b)
nf_pred = unnormalization(y_out[:, 40:], min_nf, max_nf, range_a, range_b)
nf_test = unnormalization(test_y[:, 40:], min_nf, max_nf, range_a, range_b)

### Calculating test error (absolute error)
diff_gch = []
diff_nf = []

for i in range(0, gch_pred.shape[0]):
	for j in range(0, gch_pred.shape[1]):
		diff_gch.append(abs(gch_pred[i][j] - gch_test[i][j]))
		diff_nf.append(abs(nf_pred[i][j] - nf_test[i][j]))

### Plotting results (boxplot)
plt.subplot(211)
plt.boxplot(diff_gch)
plt.title('Diff Gch')

plt.subplot(212)
plt.boxplot(diff_nf)
plt.title('Diff NF')

plt.show()