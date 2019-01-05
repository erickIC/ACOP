import numpy as np
import matplotlib.pyplot as plt
from random import randint 
from sklearn.svm import SVR
from sklearn.multioutput import MultiOutputRegressor

#taking the file.

file = open('testew.txt', 'r')
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

#Y_train = np.argmax(Y_train, axis=1)
training_x = np.array(array_x)
training_y = np.array(array_y)
test_x = np.array(array_xt)
test_y = np.array(array_yt)

##################################################### Building SVR #############################################################################

svr = SVR(kernel='rbf', C=1e3, gamma=0.2)

svr_t = MultiOutputRegressor(svr)

y_out = svr_t.fit(training_x, training_y).predict(test_x)


################################################# Printing the result ##########################################################################
print(y_out)
print("\n")
print(test_y)