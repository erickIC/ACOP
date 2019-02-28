import numpy as np
import matplotlib.pyplot as plt
from random import randint 
from sklearn.svm import SVR
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error

def unnormalization(x, min, max, range_a, range_b):
        z = []
        for i in range(0, len(x)):
                j = ((float(x[i]) - float(range_a))*(float(max)-float(min)))/ (float(range_b) - float(range_a)) + float(min)
                z.append(j)
        return z

### Reading file with normalized data
file = open('testew.txt', 'r')
lines = file.readlines()
data = []
caught = []

### Putting data in an matrix
for i in range(0, len(lines)):
	auxiliary = lines[i].split()
	data.append([float(auxiliary[0]), float(auxiliary[1]), float(auxiliary[2]), float(auxiliary[3]), float(auxiliary[4])])
	caught.append(0)

### Separating the data into training (80%) and testing set (20%)
eighty_percent = int(0.8 * len(data))

# Training set
array_x = []
array_y = []

while len(array_x) != eighty_percent:
    current = randint(0, len(caught)-1)
    if  caught[current] == 0:
        auxiliary = data[current]
        array_x.append([auxiliary[0], auxiliary[1], auxiliary[2]])
        array_y.append([auxiliary[3], auxiliary[4]])
        caught[current] = 1

# Test set
array_xt = []
array_yt = []

for i in range(len(caught)):
    if caught[i] == 0:
        auxiliary = data[i]
        array_xt.append([auxiliary[0], auxiliary[1], auxiliary[2]])
        array_yt.append([auxiliary[3], auxiliary[4]])
        caught[i] = 1

training_x = np.array(array_x)
training_y = np.array(array_y)
test_x = np.array(array_xt)
test_y = np.array(array_yt)

### Building SVR and running regression
svr = SVR(gamma='auto')

svr_t = MultiOutputRegressor(svr)
y_out = svr_t.fit(training_x, training_y).predict(test_x)

### Calculating training error (MSE - Mean Squared Error)
error = mean_squared_error(test_y, y_out, multioutput='raw_values')
print('Mean Squared Error Regression Loss:')
print('Gch:', error[0])
print('NF:', error[1])

file.close()

### De-normalizing data
file = open('max_min.txt', 'r')
lines = file.readlines()

auxiliary = lines[0].split()
max_gch = auxiliary[3]
max_nf = auxiliary[4]

auxiliary = lines[1].split()
min_gch = auxiliary[3]
min_nf = auxiliary[4]

auxiliary = lines[2].split()
range_a = auxiliary[0]
range_b = auxiliary[1]

gch_pred = []
nf_pred = []
gch_test = []
nf_test = []

for i in range(0, len(y_out)):
        gch_pred.append(y_out[i][0])
        nf_pred.append(y_out[i][1])
        gch_test.append(test_y[i][0])
        nf_test.append(test_y[i][1])

gch_pred = unnormalization(gch_pred, min_gch, max_gch, range_a, range_b)
gch_test = unnormalization(gch_test, min_gch, max_gch, range_a, range_b)
nf_pred = unnormalization(nf_pred, min_nf, max_nf, range_a, range_b)
nf_test = unnormalization(nf_test, min_nf, max_nf, range_a, range_b)

### Calculating test error (absolute error)
diff_gch = []
diff_nf = []

for i in range(0, len(y_out)):
        diff_gch.append(abs(gch_pred[i]-gch_test[i]))
        diff_nf.append(abs(nf_pred[i]-nf_test[i]))

### Plotting results (boxplot)
plt.subplot(211)
plt.boxplot(diff_gch)
plt.title('Ganho real')
plt.xticks([])
plt.ylabel("dB")

plt.subplot(212)
plt.boxplot(diff_nf)
plt.title('Noise Figure')
plt.xticks([])
plt.ylabel("dB")

plt.show()

file.close()