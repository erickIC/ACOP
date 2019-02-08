'''
    Reaseacher group: EASY Group.
    Oriented by : Professor Erick Barboza.
    Students: Allan Bezerra, Jose Carlos Pinheiro Filho, Wagner Williams.
    Programmer: Jose Carlos Pinheiro Filho.

    Description:
    Code to create one neural network with only one hidden layer to Pout and one to NF too, using Dropout and callback to previne the overfitting.
    And plotting the diference between the sinal predicted and the expected for non-normalized data. 

    licensed under the GNU General Public License v3.0.
'''
import numpy as np
from numpy import median
import matplotlib.pyplot as plt
import keras
from keras.models import Sequential
from keras.layers import Dense
from random import randint 
from keras import callbacks
from keras.layers import Dropout

def unnormalization(data, min, max, range_a, range_b):
	unnormalized_data = []
	for i in range(0, data.shape[0]):
		values = []
		for j in range(0, data.shape[1]):
			values.append(((float(data[i][j]) - float(range_a)) * (float(max)-float(min))) / (float(range_b) - float(range_a)) + float(min))
		unnormalized_data.append(values)
	return np.array(unnormalized_data)


#Read the file. 
imput_file = 'mask-edfa1-padtec-modified-normalized.txt'

#Data into a array with floats.
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
eighty_percent = int(0.8 * len(data))
number_channels = 40

array_x = []
array_xt = []

array_y_pout = []
array_yt_pout = []
      
array_y_nf = []
array_yt_nf = []

while len(array_x) != eighty_percent: #While to set the training set.
    current = randint(0, len(not_caught) - 1)
    if  not_caught[current]:
        auxiliary = data[current]
        not_caught[current] = False
        x = [auxiliary[0]]
        ypout = []
        ynf= []
        for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            ypout.append(auxiliary[41+i])
            ynf.append(auxiliary[81 + i])
        array_x.append(x)  
        array_y_pout.append(ypout)
        array_y_nf.append(ynf)  
 
for i in range(len(not_caught)):
    if not_caught[i]:
        auxiliary = data[i]
        not_caught[i] = False
        x = [auxiliary[0]]
        ypout = []
        ynf= []
        for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            ypout.append(auxiliary[41+i])
            ynf.append(auxiliary[81 + i])
        array_xt.append(x)  
        array_yt_pout.append(ypout)
        array_yt_nf.append(ynf)     
         
training_x = np.array(array_x)
training_y_pout = np.array(array_y_pout)
training_y_nf = np.array(array_y_nf)

test_x = np.array(array_xt)
test_y_pout = np.array(array_yt_pout)           
test_y_nf = np.array(array_yt_nf)

#Create ta neural network to Pout and

model_pout = Sequential()
model_nf = Sequential()

model_pout.add(Dense(83, input_dim = 41, activation='sigmoid'))
model_pout.add(Dropout(0.1))
model_pout.add(Dense(40, activation='sigmoid'))

model_nf.add(Dense(83, input_dim = 41, activation='sigmoid'))
model_nf.add(Dropout(0.1))
model_nf.add(Dense(40, activation='sigmoid'))


print(model_pout.summary())
print(model_nf.summary())

model_pout.compile(optimizer = 'adam', loss = 'mse', metrics = ['acc'])
model_nf.compile(optimizer = 'adam', loss = 'mse', metrics = ['acc'])
num_epochs = 2000

cb = callbacks.EarlyStopping(monitor = 'val_loss', min_delta = 0, patience = 10, verbose = 0, mode='auto')

history_pout = model_pout.fit(training_x, training_y_pout, validation_data=(test_x, test_y_pout), epochs = num_epochs,callbacks=[cb])
history_nf = model_nf.fit(training_x, training_y_nf, validation_data=(test_x, test_y_nf), epochs = num_epochs, callbacks=[cb])

#saving the model
model_pout.save('model_pout.h5')
model_nf.save('model_nf.h5')

#Unnormalizing the data
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

out_y_pout = model_pout.predict(test_x)
out_y_nf = model_nf.predict(test_x)

pout_pred = unnormalization(out_y_pout, min_pout, max_pout, range_a, range_b)
pout_test = unnormalization(test_y_pout, min_pout, max_pout, range_a, range_b)
nf_pred = unnormalization(out_y_nf, min_nf, max_nf, range_a, range_b)
nf_test = unnormalization(test_y_nf, min_nf, max_nf, range_a, range_b)

#Calculating the absolute error

diff_pout = []
diff_nf = []
biggest_pout = 0
biggest_nf = 0
smallest_pout = float('inf')
smallest_nf = float('inf')


for i in range(0, pout_pred.shape[0]):
    pout_current = float(0)
    nf_current = float(0)
    for j in range(0, pout_pred.shape[1]):
	    pout_current += abs(pout_pred[i][j] - pout_test[i][j])
	    nf_current += abs(nf_pred[i][j] - nf_test[i][j])
    diff_pout.append(pout_current/pout_pred.shape[1])
    if pout_current/pout_pred.shape[1] < smallest_pout:
        smallest_pout = pout_current/pout_pred.shape[1]
    if pout_current/pout_pred.shape[1] > biggest_pout:
        biggest_pout = pout_current/pout_pred.shape[1]
    diff_nf.append(nf_current/pout_pred.shape[1])
    if nf_current/pout_pred.shape[1] < smallest_nf:
        smallest_nf = nf_current/pout_pred.shape[1]
    if nf_current/pout_pred.shape[1] > biggest_nf:
        biggest_nf = nf_current/pout_pred.shape[1]      
      
biggest_pout_id = 0
biggest_nf_id = 0
smallest_pout_id = 0
smallest_nf_id = 0
median_pout_id = 0
median_nf_id = 0

for i in range(0, len(diff_pout)):
    if median(diff_pout) == diff_pout[i]:
        median_pout_id = i
    if biggest_pout == diff_pout[i]:
        biggest_pout_id = i
    if smallest_pout == diff_pout[i]:
        smallest_pout_id = i
    if median(diff_nf) == diff_nf[i]:
        median_nf_id = i
    if biggest_nf == diff_nf[i]:
        biggest_nf_id = i
    if smallest_nf == diff_nf[i]:
        smallest_nf_id = i

frequencies = [1/1560.713, 1/1559.794, 1/1559.04, 1/1558.187, 1/1557.433, 1/1556.613, 
               1/1555.858, 1/1555.038, 1/1554.153, 1/1553.398, 1/1552.578, 1/1551.758,
               1/1550.971, 1/1550.02, 1/1549.397, 1/1548.61, 1/1547.822, 1/1547.002, 
               1/1546.182, 1/1545.395, 1/1544.608, 1/1543.788, 1/1543.001, 1/1542.214,
               1/1541.426, 1/1540.639, 1/1539.852, 1/1538.966, 1/1538.278, 1/1537.425, 
               1/1536.638, 1/1535.883, 1/1535.096, 1/1534.342, 1/1533.587, 1/1532.8, 
               1/1532.013, 1/1531.226, 1/1530.438, 1/1529.651]
wavelength = [1560.713, 1559.794, 1559.04, 1558.187, 1557.433, 1556.613, 
               1555.858, 1555.038, 1554.153, 1553.398, 1552.578, 1551.758,
               1550.971, 1550.02, 1549.397, 1548.61, 1547.822, 1547.002, 
               1546.182, 1545.395, 1544.608, 1543.788, 1543.001, 1542.214,
               1541.426, 1540.639, 1539.852, 1538.966, 1538.278, 1537.425, 
               1536.638, 1535.883, 1535.096, 1534.342, 1533.587, 1532.8, 
               1532.013, 1531.226, 1530.438, 1529.651]

#Plotting
plt.figure(figsize=(50,24))

plt.subplot(321)
plt.plot(wavelength, pout_pred[biggest_pout_id], label='predicted pout')
plt.plot(wavelength, pout_test[biggest_pout_id], label='expected pout')
plt.ylabel('Pout (db)')
plt.title('Worst case Pout')
plt.legend()

plt.subplot(322)
plt.plot(wavelength, nf_pred[biggest_nf_id], label='predicted NF')
plt.plot(wavelength, nf_test[biggest_nf_id], label='expected NF')
plt.ylabel('NF (db)')
plt.title('Worst case NF')
plt.legend()

plt.subplot(323)
plt.plot(wavelength, pout_pred[median_pout_id], label='predicted pout')
plt.plot(wavelength, pout_test[median_pout_id], label='expected pout')
plt.ylabel('Pout (db)')
plt.title('Median case Pout')
plt.legend()

plt.subplot(324)
plt.plot(wavelength, nf_pred[median_nf_id], label='predicted NF')
plt.plot(wavelength, nf_test[median_nf_id], label='expected NF')
plt.ylabel('NF (db)')
plt.title('Median case NF')
plt.legend()

plt.subplot(325)
plt.plot(wavelength, pout_pred[smallest_pout_id], label='predicted pout')
plt.plot(wavelength, pout_test[smallest_pout_id], label='expected pout')
plt.xlabel('wavelength')
plt.ylabel('Pout (db)')
plt.title('Best case Pout')
plt.legend()

plt.subplot(326)
plt.plot(wavelength, nf_pred[smallest_nf_id], label='predicted NF')
plt.plot(wavelength, nf_test[smallest_nf_id], label='expected NF')
plt.xlabel('wavelength')
plt.ylabel('NF (db)')
plt.title('Best case NF')
plt.legend()

plt.show()
