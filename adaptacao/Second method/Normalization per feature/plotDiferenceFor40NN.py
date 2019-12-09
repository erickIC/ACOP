'''
    Reaseacher group: EASY Group.
    Oriented by : Professor Erick Barboza.
    Students: Allan Bezerra, Jose Carlos Pinheiro Filho, Wagner Williams.
    Programmer: Jose Carlos Pinheiro Filho.

    Description:
    Code to create forty neural networks with only one output to Pout which each one is a diferente channel, using EarlyStoppping to previne the overfitting taking all the data to train.
    And plotting the difference between the signal predicted and the expected for non-normalized data with more information, boxplot of absolute error and the training curve. 

    licensed under the GNU General Public License v3.0.
'''

import numpy as np
from numpy import median
import matplotlib.pyplot as plt
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
from random import randint 
from keras import callbacks
from keras.layers import Dropout
from matplotlib.ticker import PercentFormatter

def unnormalization(data, min, max, range_a, range_b):
	unnormalized_data = []
	for i in range(0, data.shape[0]):
		values = []
		for j in range(0, data.shape[1]):
			values.append(((float(data[i][j]) - float(range_a)) * (float(max)-float(min))) / (float(range_b) - float(range_a)) + float(min))
		unnormalized_data.append(values)
	return np.array(unnormalized_data)
def unnormalization_in(data, min_gset, max_gset, min_pin, max_pin, range_a, range_b):
	unnormalized_data = []
	for i in range(0, data.shape[0]):
		values = []
		for j in range(0, data.shape[1]):
		    if j == 0:
		        values.append(((float(data[i][j]) - float(range_a)) * (float(max_gset)-float(min_gset))) / (float(range_b) - float(range_a)) + float(min_gset))
		    else:
			    values.append(((float(data[i][j]) - float(range_a)) * (float(max_pin)-float(min_pin))) / (float(range_b) - float(range_a)) + float(min_pin))
		unnormalized_data.append(values)
	return np.array(unnormalized_data)

#Set the font sizes to the plots
smaller_size = 12
medium_size = 20
bigger_size = 26
plt.rc('font', size=bigger_size)             # controls default text sizes
plt.rc('axes', titlesize=medium_size)        # fontsize of the axes title
plt.rc('axes', labelsize=medium_size)        # fontsize of the x and y labels
plt.rc('xtick', labelsize=smaller_size)      # fontsize of the tick labels
plt.rc('ytick', labelsize=smaller_size)      # fontsize of the tick labels
plt.rc('legend', fontsize=medium_size)       # legend fontsize
plt.rc('figure', titlesize=bigger_size)      # fontsize of the figure title


#Read the file. 
imput_file = 'mask-edfa1-padtec-modified-normalized.txt'

with open(imput_file, 'r') as file:
    data = []
    not_caught = []
    lines = file.readlines() 
    for i in range(0, len(lines)):
        auxiliary = lines[i].split('\t')
        x = []
        for j in range(0, len(auxiliary)-1):
            x.append(float(auxiliary[j]))
        data.append(x)
        not_caught.append(True)

#Separate the training set and the test set.
eighty_percent = int(1 * len(data))
number_channels = 40

array_x = []
array_xt = []

array_y_pout = []
array_yt_pout = []

for i in range(0, 40):
    array_y_pout.append([])
    array_yt_pout.append([])

      

while len(array_x) != eighty_percent: #While to set the training set.
    current = randint(0, len(not_caught) - 1)
    if  not_caught[current]:
        auxiliary = data[current]
        not_caught[current] = True
        x = [auxiliary[0]]
        for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            array_y_pout[i].append([auxiliary[41+i]])
        array_x.append(x)
 
for i in range(len(not_caught)):
    if not_caught[i]:
        auxiliary = data[i]
        not_caught[i] = False
        x = [auxiliary[0]]
        for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            array_yt_pout[i].append([auxiliary[41+i]])
        array_xt.append(x)
        if len(array_xt) ==  int(0.2 * len(data)):
            break 

            
training_x = np.array(array_x)
for i in range(0, len(array_y_pout)):
    array_y_pout[i] = np.array(array_y_pout[i])
training_y_pout = np.array(array_y_pout)

test_x = np.array(array_xt)
for i in range(0, len(array_y_pout)):
    array_yt_pout[i] = np.array(array_yt_pout[i])
test_y_pout = np.array(array_yt_pout)



#load models
models = []

for i in range(0, number_channels):
    model_name = 'model_single_channel' + str(i+1) + '.h5'
    model_current = load_model(model_name)
    models.append(model_current)

print(len(models))


#Unnormalizing the data
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


out_y_pout = []

for i in range(0, len(models)):
    out_y_pout.append(models[i].predict(test_x))


y_out = []
y_test = []
for i in range(0, len(out_y_pout)):
    y_out.append(unnormalization(out_y_pout[i], min_pout, max_pout, range_a, range_b))
    y_test.append(unnormalization(test_y_pout[i], min_pout, max_pout, range_a, range_b))

y_out = np.array(y_out)
y_test = np.array(y_test)
x_test = unnormalization_in(test_x, min_gset, max_gset, min_pin, max_pin, range_a, range_b)


#Calculating the absolute error

diff_pout = []
biggest_pout = 0
smallest_pout = float('inf')


for i in range(0, y_out.shape[1]):
    current = float(0)
    for j in range(0, y_out.shape[0]):
        current += abs(y_out[j][i][0] - y_test[j][i][0])
        #print(current, y_out[j][i][0], y_test[j][i][0])
    diff_pout.append(current/y_out.shape[0])
    if current/y_out.shape[0] < smallest_pout:
        smallest_pout = current/y_out.shape[0]
    if current/y_out.shape[0] > biggest_pout:
        biggest_pout = current/y_out.shape[0]

biggest_pout_id = 0
smallest_pout_id = 0
median_pout_id = 0

for i in range(0, len(diff_pout)):
    if median(diff_pout) == diff_pout[i]:
        median_pout_id = i
    if biggest_pout == diff_pout[i]:
        biggest_pout_id = i
    if smallest_pout == diff_pout[i]:
        smallest_pout_id = i



wavelength = [1560.713, 1559.794, 1559.04, 1558.187, 1557.433, 1556.613, 
               1555.858, 1555.038, 1554.153, 1553.398, 1552.578, 1551.758,
               1550.971, 1550.02, 1549.397, 1548.61, 1547.822, 1547.002, 
               1546.182, 1545.395, 1544.608, 1543.788, 1543.001, 1542.214,
               1541.426, 1540.639, 1539.852, 1538.966, 1538.278, 1537.425, 
               1536.638, 1535.883, 1535.096, 1534.342, 1533.587, 1532.8, 
               1532.013, 1531.226, 1530.438, 1529.651]


#Plotting






biggest_diff_out = []
biggest_diff_test = []
smallest_diff_out = []
smallest_diff_test = []
median_diff_out = []
median_diff_test = []

for i in range(0, y_out.shape[0]):
    biggest_diff_out.append(y_out[i][biggest_pout_id][0])
    biggest_diff_test.append(y_test[i][biggest_pout_id][0])

    smallest_diff_out.append(y_out[i][smallest_pout_id][0])
    smallest_diff_test.append(y_test[i][smallest_pout_id][0])

    median_diff_out.append(y_out[i][median_pout_id][0])
    median_diff_test.append(y_test[i][median_pout_id][0])

biggest_diff_out = np.array(biggest_diff_out)
biggest_diff_test = np.array(biggest_diff_test)
smallest_diff_out = np.array(smallest_diff_out)
smallest_diff_test = np.array(smallest_diff_test)
median_diff_out = np.array(median_diff_out)
median_diff_test = np.array(median_diff_test)



#Original vs predicted
text = ''

plt.figure(figsize=(16,16))
plt.subplot(311)
text = 'Gset =' + str(int(x_test[biggest_pout_id][0])) + '(dB) ' + 'Tilt = '  + str(int(round((x_test[biggest_pout_id][1] - x_test[biggest_pout_id][len(x_test[biggest_pout_id]) - 1]), 0))) + '(dBm)'
plt.plot(wavelength, biggest_diff_out, 'o-', label='predicted pout')
plt.plot(wavelength, biggest_diff_test, 'o-',label='expected pout')
plt.ylabel('Pout (dBm)')
plt.title('Worst case Pout' + ' ' + text)
plt.legend()

plt.subplot(312)
text = 'Gset =' + str(int(x_test[median_pout_id][0])) + '(dB) ' + 'Tilt = '  + str(int(round((x_test[median_pout_id][1] - x_test[median_pout_id][len(x_test[median_pout_id]) - 1]), 0))) + '(dBm)'
plt.plot(wavelength, median_diff_out, 'o-', label='predicted pout')
plt.plot(wavelength, median_diff_test, 'o-', label='expected pout')
plt.ylabel('Pout (dBm)')
plt.title('Median case Pout' + ' ' + text)
plt.legend()

plt.subplot(313)
text = 'Gset =' + str(int(x_test[smallest_pout_id][0])) + '(dB) ' + 'Tilt = '  + str(int(round((x_test[smallest_pout_id][1] - x_test[smallest_pout_id][len(x_test[smallest_pout_id]) - 1]), 0))) + '(dBm)'
plt.plot(wavelength, smallest_diff_out, 'o-', label='predicted pout')
plt.plot(wavelength, smallest_diff_test, 'o-', label='expected pout')
plt.xlabel('wavelength')
plt.ylabel('Pout (dBm)')
plt.title('Best case Pout' + ' ' + text)
plt.legend()
plt.savefig('Diference40PlotPout.png', dpi = 200)



#Boxplot
plt.figure(figsize=(16,10))
plt.boxplot(diff_pout)
plt.title('Absolute difference')
plt.xticks([1], ['Diff Pout'])
plt.ylabel('(dB)')
plt.savefig('Diference40BoxPlot.png', dpi = 200)

