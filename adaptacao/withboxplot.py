import numpy as np
import matplotlib.pyplot as plt
import keras
from keras.models import Sequential
from keras.layers import Dense
from random import randint 

def unnormalization(x, min, max, range_a, range_b):
    z = []
    for i in range(0, len(x)):
        j = ((float(x[i]) - float(range_a))*(float(max)-float(min)))/ (float(range_b) - float(range_a)) + float(min)
        z.append(j)
    return z

#taking the file.

file = open('testew.txt', 'r')
file2 = open('max_min.txt', 'r')

lines = file.readlines()
data = []
caught = [] #it's going to be used to see which data has been taken already in separation.


#################################################Data in to a array with floats############################################################
for i in range(0, len(lines)):
	auxiliary = lines[i].split()	
	data.append([float(auxiliary[0]), float(auxiliary[1]), float(auxiliary[2]), float(auxiliary[3]), float(auxiliary[4]) ])
	caught.append(0)

###################################Separating the data into training set and testing set###################################################  
eighty_percent = int(0.8 * len(data))

array_x = []
array_y = []
array_xt = []
array_yt = []

while len(array_x) != eighty_percent: #While to set the training set.
    current = randint(0, len(caught) - 1)
  
    if  caught[current] == 0:
        auxiliary_2 = data[current]
        caught[current] = 1
        array_x.append([auxiliary_2[0], auxiliary_2[1], auxiliary_2[2]])
        array_y.append([auxiliary_2[3], auxiliary_2[4]])


for i in range(len(caught)): #For to set the testing set

    if caught[i] == 0:
        auxiliary_2 = data[i]
        caught[i] = 1
        array_xt.append([auxiliary_2[0], auxiliary_2[1], auxiliary_2[2]])
        array_yt.append([auxiliary_2[3], auxiliary_2[4]])

training_x = np.array(array_x)
training_y = np.array(array_y)
test_x = np.array(array_xt)
test_y = np.array(array_yt)


########################################Building the neural network#########################################################################

model = Sequential()

model.add(Dense(7, input_dim=3, activation='sigmoid'))
model.add(Dense(15, activation='sigmoid'))
model.add(Dense(2, activation ='sigmoid'))

print(model.summary())

#input()

model.compile(optimizer = 'adam', loss = 'mse', metrics = ['acc'])

history = model.fit(training_x, training_y, epochs = 150)

y_pred = model.predict(test_x)



########################################### Ploting ########################################################################################## 
lines = file2.readlines()
auxiliary = lines[0].split()
max_gch = auxiliary[3]
max_nf = auxiliary[4]
auxiliary = lines[1].split()
min_gch = auxiliary[3]
min_nf = auxiliary[4]
auxiliary = lines[2].split()
range_a = auxiliary[0]
range_b = auxiliary[1] 

gch_test = []
nf_test = []
gch_pred = []
nf_pred = []

for i in range(0, len(y_pred)):
    gch_test.append(test_y[i][0])
    nf_test.append(test_y[i][1])
    gch_pred.append(y_pred[i][0])
    nf_pred.append(y_pred[i][1])
    
gch_test = unnormalization(gch_test, max_gch, min_gch, range_a, range_b)
gch_pred = unnormalization(gch_pred, max_gch, min_gch, range_a, range_b)
nf_test = unnormalization(nf_test, max_nf, min_nf, range_a, range_b)
nf_pred = unnormalization(nf_pred, max_nf, min_nf, range_a, range_b)

diff_gch = []
diff_nf = []

for i in range(0, len(gch_test)):
    diff_gch.append(abs(gch_test[i] - gch_pred[i]))
    diff_nf.append(abs(nf_test[i] - nf_pred[i]))

#print(diff_gch[0], diff_nf[0])

plt.subplot(211)
plt.boxplot(diff_gch)
plt.title('Diff gch 7 - 15 - 2')
plt.subplot(212)
plt.boxplot(diff_nf)
plt.title('Diff NF')
plt.show()


file.close()
file2.close()