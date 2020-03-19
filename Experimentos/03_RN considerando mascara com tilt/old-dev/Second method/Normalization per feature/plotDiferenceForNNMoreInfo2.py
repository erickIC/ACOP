'''
    Reaseacher group: EASY Group.
    Oriented by : Professor Erick Barboza.
    Students: Allan Bezerra, Jose Carlos Pinheiro Filho, Wagner Williams.
    Programmer: Jose Carlos Pinheiro Filho.

    Description:
    Code to create one neural network with only one hidden layer to Pout and one to NF too, using callback to previne the overfitting taking all the data.
    And plotting the difference between the signal predicted and the expected for non-normalized data with more information, boxplot of absolute error and the training curve. 

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
eighty_percent = int(1 * len(data))
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
        not_caught[current] = True
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
        if len(array_xt) ==  int(0.2 * len(data)):
            break 
         
training_x = np.array(array_x)
training_y_pout = np.array(array_y_pout)
training_y_nf = np.array(array_y_nf)

test_x = np.array(array_xt)
test_y_pout = np.array(array_yt_pout)           
test_y_nf = np.array(array_yt_nf)

#Create ta neural network to Pout and

model_pout = Sequential()
model_nf = Sequential()

model_pout.add(Dense(54, input_dim = 41, activation='sigmoid'))
model_pout.add(Dense(54, activation='sigmoid'))
model_pout.add(Dense(40, activation='sigmoid'))

model_nf.add(Dense(54, input_dim = 41, activation='sigmoid'))
model_nf.add(Dense(54, activation='sigmoid'))
model_nf.add(Dense(40, activation='sigmoid'))


print(model_pout.summary())
print(model_nf.summary())

model_pout.compile(optimizer = 'adam', loss = 'mse', metrics = ['acc'])
model_nf.compile(optimizer = 'adam', loss = 'mse', metrics = ['acc'])
num_epochs = 5000

cb = callbacks.EarlyStopping(monitor = 'val_loss', min_delta = 0, patience = 120, verbose = 0, mode='auto')

history_pout = model_pout.fit(training_x, training_y_pout, validation_data=(test_x, test_y_pout), epochs = num_epochs,callbacks=[cb])
history_nf = model_nf.fit(training_x, training_y_nf, validation_data=(test_x, test_y_nf), epochs = num_epochs, callbacks=[cb])

#saving the model
model_pout.save('model_pout4.h5')
model_nf.save('model_nf4.h5')

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

out_y_pout = model_pout.predict(test_x)
out_y_nf = model_nf.predict(test_x)

pout_pred = unnormalization(out_y_pout, min_pout, max_pout, range_a, range_b)
pout_test = unnormalization(test_y_pout, min_pout, max_pout, range_a, range_b)
nf_pred = unnormalization(out_y_nf, min_nf, max_nf, range_a, range_b)
nf_test = unnormalization(test_y_nf, min_nf, max_nf, range_a, range_b)
x_test = unnormalization_in(test_x, min_gset, max_gset, min_pin, max_pin, range_a, range_b)

#Calculating the absolute error

diff_pout = []
diff_nf = []
diff_pout_hist = []
diff_nf_hist = []
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
    diff_pout_hist.append((pout_current/pout_pred.shape[1], i))
    if pout_current/pout_pred.shape[1] < smallest_pout:
        smallest_pout = pout_current/pout_pred.shape[1]
    if pout_current/pout_pred.shape[1] > biggest_pout:
        biggest_pout = pout_current/pout_pred.shape[1]
    
    diff_nf.append(nf_current/pout_pred.shape[1])
    diff_nf_hist.append((nf_current/pout_pred.shape[1], i))
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


#To histogram
diff_pout_hist.sort(key=lambda x: x[0], reverse = True)
diff_nf_hist.sort(key=lambda x: x[0], reverse = True)

twenty_five_percent = int(0.25 * len(diff_pout_hist))

pout_gset_hist = []
pout_tilt_hist = []
nf_gset_hist = []
nf_tilt_hist = []
current_hist_pout= []
current_hist_nf= []
for i in range(0, twenty_five_percent - 1):
    current_hist_pout = diff_pout_hist[i][1]
    current_hist_nf = diff_nf_hist[i][1]

    pout_gset_hist.append(x_test[current_hist_pout][0])
    pout_tilt_hist.append(int(round((x_test[current_hist_pout][1] - x_test[current_hist_pout][len(x_test[current_hist_pout]) - 1]), 0)))
    nf_gset_hist.append(x_test[current_hist_nf][0])
    nf_tilt_hist.append(int(round((x_test[current_hist_nf][1] - x_test[current_hist_nf][len(x_test[current_hist_nf]) - 1]), 0)))


#Plotting

#Training plot
plt.figure(figsize=(16,10))

plt.subplot(221)
plt.plot(history_pout.epoch, history_pout.history['val_loss'], label='loss val')
plt.plot(history_pout.epoch, history_pout.history['loss'],'--', label='loss train')
plt.ylabel('MSE')
plt.title('Pout loss')
plt.legend()

plt.subplot(222)
plt.plot(history_pout.epoch, history_pout.history['val_acc'], label='acc val')
plt.plot(history_pout.epoch, history_pout.history['acc'],'--', label='acc train')
plt.ylabel('Accuracy')
plt.title('Pout accuracy')
plt.legend()

plt.subplot(223)
plt.plot(history_nf.epoch, history_nf.history['val_loss'], label='loss val')
plt.plot(history_nf.epoch, history_nf.history['loss'],'--', label='loss train')
plt.xlabel('epochs')
plt.ylabel('MSE')
plt.title('NF loss')
plt.legend()

plt.subplot(224)
plt.plot(history_nf.epoch, history_nf.history['val_acc'], label='acc val')
plt.plot(history_nf.epoch, history_nf.history['acc'],'--', label='acc train')
plt.xlabel('epochs')
plt.ylabel('Accuracy')
plt.title('NF accuracy')
plt.legend()

plt.savefig('TrainingPlot.png', dpi = 200)


#Original vs predicted
text = ''

plt.figure(figsize=(16,16))
plt.subplot(311)
text = 'Gset =' + str(int(x_test[biggest_pout_id][0])) + '(dB) ' + 'Tilt = '  + str(int(round((x_test[biggest_pout_id][1] - x_test[biggest_pout_id][len(x_test[biggest_pout_id]) - 1]), 0))) + '(dB)'
plt.plot(wavelength, pout_pred[biggest_pout_id], label='predicted pout')
plt.plot(wavelength, pout_test[biggest_pout_id], label='expected pout')
plt.ylabel('Pout (db)')
plt.title('Worst case Pout' + ' ' + text)
plt.legend()

plt.subplot(312)
text = 'Gset =' + str(int(x_test[median_pout_id][0])) + '(dB) ' + 'Tilt = '  + str(int(round((x_test[median_pout_id][1] - x_test[median_pout_id][len(x_test[median_pout_id]) - 1]), 0))) + '(dB)'
plt.plot(wavelength, pout_pred[median_pout_id], label='predicted pout')
plt.plot(wavelength, pout_test[median_pout_id], label='expected pout')
plt.ylabel('Pout (db)')
plt.title('Median case Pout' + ' ' + text)
plt.legend()

plt.subplot(313)
text = 'Gset =' + str(int(x_test[smallest_pout_id][0])) + '(dB) ' + 'Tilt = '  + str(int(round((x_test[smallest_pout_id][1] - x_test[smallest_pout_id][len(x_test[smallest_pout_id]) - 1]), 0))) + '(dB)'
plt.plot(wavelength, pout_pred[smallest_pout_id], label='predicted pout')
plt.plot(wavelength, pout_test[smallest_pout_id], label='expected pout')
plt.xlabel('wavelength')
plt.ylabel('Pout (db)')
plt.title('Best case Pout' + ' ' + text)
plt.legend()
plt.savefig('DiferencePlotPout.png', dpi = 200)


plt.figure(figsize=(16,16))
plt.subplot(311)
text = 'Gset =' + str(int(x_test[biggest_nf_id][0])) + '(dB) ' + 'Tilt = '  + str(int(round((x_test[biggest_nf_id][1] - x_test[biggest_nf_id][len(x_test[biggest_nf_id]) - 1]), 0))) + '(dB)'
plt.plot(wavelength, nf_pred[biggest_nf_id], label='predicted NF')
plt.plot(wavelength, nf_test[biggest_nf_id], label='expected NF')
plt.ylabel('NF (db)')
plt.title('Worst case NF' + ' ' + text)
plt.legend()

plt.subplot(312)
text = 'Gset =' + str(int(x_test[median_nf_id][0])) + '(dB) ' + 'Tilt = '  + str(int(round((x_test[median_nf_id][1] - x_test[median_nf_id][len(x_test[median_nf_id]) - 1]), 0))) + '(dB)'
plt.plot(wavelength, nf_pred[median_nf_id], label='predicted NF')
plt.plot(wavelength, nf_test[median_nf_id], label='expected NF')
plt.ylabel('NF (db)')
plt.title('Median case NF' + ' ' + text)
plt.legend()

plt.subplot(313)
text = 'Gset =' + str(int(x_test[smallest_nf_id][0])) + '(dB) ' + 'Tilt = '  + str(int(round((x_test[smallest_nf_id][1] - x_test[smallest_nf_id][len(x_test[smallest_nf_id]) - 1]), 0))) + '(dB)'
plt.plot(wavelength, nf_pred[smallest_nf_id], label='predicted NF')
plt.plot(wavelength, nf_test[smallest_nf_id], label='expected NF')
plt.xlabel('wavelength')
plt.ylabel('NF (db)')
plt.title('Best case NF' + ' ' + text)
plt.legend()

plt.savefig('DiferencePlotNF.png', dpi = 200)



#Boxplot
plt.figure(figsize=(16,10))
plt.boxplot([diff_pout, diff_nf])
plt.title('Absolute difference')
plt.xticks([1, 2], ['Diff Pout', 'Diff NF'])
plt.ylabel('(dB)')
plt.savefig('DiferenceBoxPlot.png', dpi = 200)


#Histogram
plt.figure(figsize=(16,10))
plt.subplot(211)
#plt.hist(pout_gset_hist, bins=12) 
plt.hist(pout_gset_hist, weights=np.ones(len(pout_gset_hist)) / len(pout_gset_hist), bins = 12)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.title('25% Worst cases Pout')
plt.xlabel('Gset (dB)')
plt.ylabel('Percentage')

plt.subplot(212)
#plt.hist(pout_tilt_hist, bins=55)
plt.hist(pout_tilt_hist, weights=np.ones(len(pout_tilt_hist)) / len(pout_tilt_hist), bins = 40)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.xlabel('Tilt (dB)')
plt.ylabel('Percentage')

plt.savefig('HistPoutPlot.png', dpi = 200)

plt.figure(figsize=(16,10))
plt.subplot(211)
#plt.hist(nf_gset_hist, bins=12)
plt.hist(nf_gset_hist, weights=np.ones(len(nf_gset_hist)) / len(nf_gset_hist), bins = 12)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.title('25% Worst cases NF')
plt.xlabel('Gset (dB)')
plt.ylabel('Percentage')

plt.subplot(212)
plt.hist(nf_tilt_hist, weights=np.ones(len(nf_tilt_hist)) / len(nf_tilt_hist), bins = 40)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.xlabel('Tilt (dB)')
plt.ylabel('Percentage')

plt.savefig('HistNFPlot.png', dpi = 200)