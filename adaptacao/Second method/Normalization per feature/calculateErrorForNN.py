'''
    Reaseacher group: EASY Group.
    Oriented by : Professor Erick Barboza.
    Students: Allan Bezerra, Jose Carlos Pinheiro, Wagner Williams.
    Programmer: Jose Carlos Pinheiro Filho.

    Description:
    Code to create one neural network with only one hidden layer to Pout and one to NF too, using Dropout and callback to previne the overfitting.
    And plotting the Error for non-normalized data. 

    licensed under the GNU General Public License v3.0.
'''
import numpy as np
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

for i in range(0, pout_pred.shape[0]):
    pout_current = float(0)
    nf_current = float(0)
    for j in range(0, pout_pred.shape[1]):
	    pout_current += abs(pout_pred[i][j] - pout_test[i][j])
	    nf_current += abs(nf_pred[i][j] - nf_test[i][j])
    diff_pout.append(pout_current/pout_pred.shape[1])
    diff_nf.append(nf_current/pout_pred.shape[1])            


#Plotting

plt.figure(figsize=(16,10))
plt.subplot(211)
plt.boxplot(diff_pout)
plt.title('Diff Pout')

plt.subplot(212)
plt.boxplot(diff_nf)
plt.title('Diff NF')
plt.show()