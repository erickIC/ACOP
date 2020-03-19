'''
    Reaseacher group: EASY Group.
    Oriented by : Professor Erick Barboza.
    Students: Allan Bezerra, Jose Carlos Pinheiro, Wagner Williams.
    Programmer: Jose Carlos Pinheiro Filho.

    Description:
    First code to do a neural network with the new method of data separation.

    licensed under the GNU General Public License v3.0.
'''
import numpy as np
import matplotlib.pyplot as plt
import keras
from keras.models import Sequential
from keras.layers import Dense
from random import randint 



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
model_pout.add(Dense(167, activation='sigmoid'))
model_pout.add(Dense(40, activation='sigmoid'))

model_nf.add(Dense(83, input_dim = 41, activation='sigmoid'))
model_nf.add(Dense(167, activation='sigmoid'))
model_nf.add(Dense(40, activation='sigmoid'))


print(model_pout.summary())
print(model_nf.summary())

model_pout.compile(optimizer = 'adam', loss = 'mse', metrics = ['acc'])
model_nf.compile(optimizer = 'adam', loss = 'mse', metrics = ['acc'])
num_epochs = 100

history_pout = model_pout.fit(training_x, training_y_pout, validation_data=(test_x, test_y_pout), epochs = num_epochs)
history_nf = model_nf.fit(training_x, training_y_nf, validation_data=(test_x, test_y_nf), epochs = num_epochs)


#Plotting

plt.figure(figsize=(16,10))

plt.subplot(221)
plt.plot(history_pout.epoch, history_pout.history['val_loss'], label='loss val')
plt.plot(history_pout.epoch, history_pout.history['loss'],'--', label='loss train')
plt.xlabel('epochs')
plt.ylabel('MSE')
plt.title('Pout loss')
plt.legend()

plt.subplot(222)
plt.plot(history_pout.epoch, history_pout.history['val_acc'], label='acc val')
plt.plot(history_pout.epoch, history_pout.history['acc'],'--', label='acc train')
plt.xlabel('epochs')
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


plt.show()