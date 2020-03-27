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
import math
import pickle

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

def unnormalization(data, min, max, range_a, range_b):
	unnormalized_data = []
	for i in range(0, data.shape[0]):
		values = []
		for j in range(0, data.shape[1]):
			values.append(((float(data[i][j]) - float(range_a)) * (float(max)-float(min))) / (float(range_b) - float(range_a)) + float(min))
		unnormalized_data.append(values)
	return np.array(unnormalized_data)

def unnormalizationic(data, min_gch, max_gch, min_nf, max_nf, range_a, range_b):
	unnormalized_data = []
	for i in range(0, data.shape[0]):
		values = []
		values.append(((float(data[i][0]) - float(range_a)) * (float(max_gch)-float(min_gch))) / (float(range_b) - float(range_a)) + float(min_gch))
		values.append(((float(data[i][1]) - float(range_a)) * (float(max_nf)-float(min_nf))) / (float(range_b) - float(range_a)) + float(min_nf))
		unnormalized_data.append(values)
	return np.array(unnormalized_data)

def unnormalizationicin(data, min_pinto, max_pinto, min_gain, max_gain, range_a, range_b):
	unnormalized_data = []
	for i in range(0, data.shape[0]):
		values = []
		values.append(((float(data[i][0]) - float(range_a)) * (float(max_pinto)-float(min_pinto))) / (float(range_b) - float(range_a)) + float(min_pinto))
		values.append(((float(data[i][1]) - float(range_a)) * (float(max_gain)-float(min_gain))) / (float(range_b) - float(range_a)) + float(min_gain))
		unnormalized_data.append(values)
	return np.array(unnormalized_data)

#Set the font sizes to the plots
smaller_size = 12
medium_size = 20
bigger_size = 48
plt.rc('font', size=bigger_size)             # controls default text sizes
plt.rc('axes', titlesize=bigger_size)        # fontsize of the axes title
plt.rc('axes', labelsize=bigger_size)        # fontsize of the x and y labels
plt.rc('xtick', labelsize=bigger_size)      # fontsize of the tick labels
plt.rc('ytick', labelsize=bigger_size)      # fontsize of the tick labels
plt.rc('legend', fontsize=bigger_size)       # legend fontsize
plt.rc('figure', titlesize=bigger_size)      # fontsize of the figure title

#### Getting the folds
input_folder1 = "masks/mask-edfa1-padtec-new-models-fold-1v2.txt"
input_folder2 = "masks/mask-edfa1-padtec-new-models-fold-2v2.txt"
input_folder3 = "masks/mask-edfa1-padtec-new-models-fold-3v2.txt"
input_folder4 = "masks/mask-edfa1-padtec-new-models-fold-4v2.txt"
input_folder5 = "masks/mask-edfa1-padtec-new-models-fold-5v2.txt"

DEBUG = False
wavelength = [1560.713, 1559.794, 1559.04, 1558.187, 1557.433, 1556.613, 
               1555.858, 1555.038, 1554.153, 1553.398, 1552.578, 1551.758,
               1550.971, 1550.02, 1549.397, 1548.61, 1547.822, 1547.002, 
               1546.182, 1545.395, 1544.608, 1543.788, 1543.001, 1542.214,
               1541.426, 1540.639, 1539.852, 1538.966, 1538.278, 1537.425, 
               1536.638, 1535.883, 1535.096, 1534.342, 1533.587, 1532.8, 
               1532.013, 1531.226, 1530.438, 1529.651]

############################## 41 to 40 #############################################

#Data into a array with floats.
with open(input_folder1, 'r') as file:
    data1 = []
    lines = file.readlines() 
    for i in range(0, len(lines)):
        auxiliary = lines[i].split('\t')
        x = []
        for j in range(0, len(auxiliary)-1):
            x.append(float(auxiliary[j]))
        data1.append(x)

with open(input_folder2, 'r') as file:
    data2 = []
    lines = file.readlines() 
    for i in range(0, len(lines)):
        auxiliary = lines[i].split('\t')
        x = []
        for j in range(0, len(auxiliary)-1):
            x.append(float(auxiliary[j]))
        data2.append(x)

with open(input_folder3, 'r') as file:
    data3 = []
    lines = file.readlines() 
    for i in range(0, len(lines)):
        auxiliary = lines[i].split('\t')
        x = []
        for j in range(0, len(auxiliary)-1):
            x.append(float(auxiliary[j]))
        data3.append(x)

with open(input_folder4, 'r') as file:
    data4 = []
    lines = file.readlines() 
    for i in range(0, len(lines)):
        auxiliary = lines[i].split('\t')
        x = []
        for j in range(0, len(auxiliary)-1):
            x.append(float(auxiliary[j]))
        data4.append(x)

with open(input_folder5, 'r') as file:
    data5 = []
    lines = file.readlines() 
    for i in range(0, len(lines)):
        auxiliary = lines[i].split('\t')
        x = []
        for j in range(0, len(auxiliary)-1):
            x.append(float(auxiliary[j]))
        data5.append(x)



number_channels = 40

fold_x1 = []
fold_y1 = []

fold_x2 = []
fold_y2 = []

fold_x3 = []
fold_y3 = []

fold_x4 = []
fold_y4 = []

fold_x5 = []
fold_y5 = []

for i in range(0, len(data1)):
    auxiliary = data1[i]
    x = [auxiliary[0]]
    y = []
    for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            y.append(auxiliary[42+i]) #42 because 41 is tilt.
    fold_x1.append(x)
    fold_y1.append(y)

for i in range(0, len(data2)):
    auxiliary = data2[i]
    x = [auxiliary[0]]
    y = []
    for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            y.append(auxiliary[42+i]) #42 because 41 is tilt.
    fold_x2.append(x)
    fold_y2.append(y)

for i in range(0, len(data3)):
    auxiliary = data3[i]
    x = [auxiliary[0]]
    y = []
    for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            y.append(auxiliary[42+i]) #42 because 41 is tilt.
    fold_x3.append(x)
    fold_y3.append(y)

for i in range(0, len(data4)):
    auxiliary = data4[i]
    x = [auxiliary[0]]
    y = []
    for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            y.append(auxiliary[42+i]) #42 because 41 is tilt.
    fold_x4.append(x)
    fold_y4.append(y)

for i in range(0, len(data5)):
    auxiliary = data5[i]
    x = [auxiliary[0]]
    y = []
    for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            y.append(auxiliary[42+i]) #42 because 41 is tilt.
    fold_x5.append(x)
    fold_y5.append(y)

#print(len(fold_y1[0]), fold_y1[0])

fold41_x1 = np.array(fold_x1)
fold41_y1 = np.array(fold_y1)

fold41_x2 = np.array(fold_x2)
fold41_y2 = np.array(fold_y2)

fold41_x3 = np.array(fold_x3)
fold41_y3 = np.array(fold_y3)

fold41_x4 = np.array(fold_x4)
fold41_y4 = np.array(fold_y4)

fold41_x5 = np.array(fold_x5)
fold41_y5 = np.array(fold_y5)

fold41_x = [fold41_x1, fold41_x2, fold41_x3, fold41_x4, fold41_x5]
fold41_y = [fold41_y1, fold41_y2, fold41_y3, fold41_y4, fold41_y5]


########################### 42 to 40 ##################################################

fold_x1 = []
fold_y1 = []

fold_x2 = []
fold_y2 = []

fold_x3 = []
fold_y3 = []

fold_x4 = []
fold_y4 = []

fold_x5 = []
fold_y5 = []

for i in range(0, len(data1)):
    auxiliary = data1[i]
    x = [auxiliary[0]]
    y = []
    for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            y.append(auxiliary[42+i]) #42 because 41 is tilt.
    x.append(auxiliary[41])
    fold_x1.append(x)
    fold_y1.append(y)

for i in range(0, len(data2)):
    auxiliary = data2[i]
    x = [auxiliary[0]]
    y = []
    for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            y.append(auxiliary[42+i]) #42 because 41 is tilt.
    x.append(auxiliary[41])
    fold_x2.append(x)
    fold_y2.append(y)

for i in range(0, len(data3)):
    auxiliary = data3[i]
    x = [auxiliary[0]]
    y = []
    for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            y.append(auxiliary[42+i]) #42 because 41 is tilt.
    x.append(auxiliary[41])
    fold_x3.append(x)
    fold_y3.append(y)

for i in range(0, len(data4)):
    auxiliary = data4[i]
    x = [auxiliary[0]]
    y = []
    for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            y.append(auxiliary[42+i]) #42 because 41 is tilt.
    x.append(auxiliary[41])
    fold_x4.append(x)
    fold_y4.append(y)

for i in range(0, len(data5)):
    auxiliary = data5[i]
    x = [auxiliary[0]]
    y = []
    for i in range(0, number_channels):
            x.append(auxiliary[1+i])
            y.append(auxiliary[42+i]) #42 because 41 is tilt.
    x.append(auxiliary[41])
    fold_x5.append(x)
    fold_y5.append(y)


fold42_x1 = np.array(fold_x1)
fold42_y1 = np.array(fold_y1)

fold42_x2 = np.array(fold_x2)
fold42_y2 = np.array(fold_y2)

fold42_x3 = np.array(fold_x3)
fold42_y3 = np.array(fold_y3)

fold42_x4 = np.array(fold_x4)
fold42_y4 = np.array(fold_y4)

fold42_x5 = np.array(fold_x5)
fold42_y5 = np.array(fold_y5)

fold42_x = [fold42_x1, fold42_x2, fold42_x3, fold42_x4, fold42_x5]
fold42_y = [fold42_y1, fold42_y2, fold42_y3, fold42_y4, fold42_y5]


#################################### ICTON 17 with tilt ##################################################


input_folder1 = "masks/mask-edfa1-padtec-icton17-fold-1v2.txt"
input_folder2 = "masks/mask-edfa1-padtec-icton17-fold-2v2.txt"
input_folder3 = "masks/mask-edfa1-padtec-icton17-fold-3v2.txt"
input_folder4 = "masks/mask-edfa1-padtec-icton17-fold-4v2.txt"
input_folder5 = "masks/mask-edfa1-padtec-icton17-fold-5v2.txt"

with open(input_folder1, 'r') as f_in:
	data1 = []
	lines = f_in.readlines()
	for i in range(0, len(lines)):
		auxiliary = lines[i].split()
		data1.append([float(auxiliary[0]), float(auxiliary[1]), float(auxiliary[2]), float(auxiliary[3]), float(auxiliary[4]), float(auxiliary[5])])

with open(input_folder2, 'r') as f_in:
	data2 = []
	lines = f_in.readlines()
	for i in range(0, len(lines)):
		auxiliary = lines[i].split()
		data2.append([float(auxiliary[0]), float(auxiliary[1]), float(auxiliary[2]), float(auxiliary[3]), float(auxiliary[4]), float(auxiliary[5])])

with open(input_folder3, 'r') as f_in:
	data3 = []
	lines = f_in.readlines()
	for i in range(0, len(lines)):
		auxiliary = lines[i].split()
		data3.append([float(auxiliary[0]), float(auxiliary[1]), float(auxiliary[2]), float(auxiliary[3]), float(auxiliary[4]), float(auxiliary[5])])

with open(input_folder4, 'r') as f_in:
	data4 = []
	lines = f_in.readlines()
	for i in range(0, len(lines)):
		auxiliary = lines[i].split()
		data4.append([float(auxiliary[0]), float(auxiliary[1]), float(auxiliary[2]), float(auxiliary[3]), float(auxiliary[4]), float(auxiliary[5])])

with open(input_folder5, 'r') as f_in:
	data5 = []
	lines = f_in.readlines()
	for i in range(0, len(lines)):
		auxiliary = lines[i].split()
		data5.append([float(auxiliary[0]), float(auxiliary[1]), float(auxiliary[2]), float(auxiliary[3]), float(auxiliary[4]), float(auxiliary[5])])

### Splitting data into training and testing set, and then using k-Fold Cross Validation to calculate error

fold_x1 = []
fold_y1 = []

fold_x2 = []
fold_y2 = []

fold_x3 = []
fold_y3 = []

fold_x4 = []
fold_y4 = []

fold_x5 = []
fold_y5 = []

for i in range(0, len(data1)):
	fold_x1.append([data1[i][0], data1[i][1], data1[i][2], data1[i][3]])
	fold_y1.append([data1[i][4], data1[i][5]])

	fold_x2.append([data2[i][0], data2[i][1], data2[i][2], data2[i][3]])
	fold_y2.append([data2[i][4], data2[i][5]])

	fold_x3.append([data3[i][0], data3[i][1], data3[i][2], data3[i][3]])
	fold_y3.append([data3[i][4], data3[i][5]])

	fold_x4.append([data4[i][0], data4[i][1], data4[i][2], data4[i][3]])
	fold_y4.append([data4[i][4], data4[i][5]])

	fold_x5.append([data5[i][0], data5[i][1], data5[i][2], data5[i][3]])
	fold_y5.append([data5[i][4], data5[i][5]])

foldic_x1 = np.array(fold_x1)
foldic_y1 = np.array(fold_y1)

foldic_x2 = np.array(fold_x2)
foldic_y2 = np.array(fold_y2)

foldic_x3 = np.array(fold_x3)
foldic_y3 = np.array(fold_y3)

foldic_x4 = np.array(fold_x4)
foldic_y4 = np.array(fold_y4)

foldic_x5 = np.array(fold_x5)
foldic_y5 = np.array(fold_y5)

foldic_x = [foldic_x1, foldic_x2, foldic_x3, foldic_x4, foldic_x5]
foldic_y = [foldic_y1, foldic_y2, foldic_y3, foldic_y4, foldic_y5]



#################################### ICTON 17 original ##################################################


fold_x1 = []
fold_y1 = []

fold_x2 = []
fold_y2 = []

fold_x3 = []
fold_y3 = []

fold_x4 = []
fold_y4 = []

fold_x5 = []
fold_y5 = []

for i in range(0, len(data1)):
	fold_x1.append([data1[i][0], data1[i][1], data1[i][2]])
	fold_y1.append([data1[i][4], data1[i][5]])

	fold_x2.append([data2[i][0], data2[i][1], data2[i][2]])
	fold_y2.append([data2[i][4], data2[i][5]])

	fold_x3.append([data3[i][0], data3[i][1], data3[i][2]])
	fold_y3.append([data3[i][4], data3[i][5]])

	fold_x4.append([data4[i][0], data4[i][1], data4[i][2]])
	fold_y4.append([data4[i][4], data4[i][5]])

	fold_x5.append([data5[i][0], data5[i][1], data5[i][2]])
	fold_y5.append([data5[i][4], data5[i][5]])

foldico_x1 = np.array(fold_x1)
foldico_y1 = np.array(fold_y1)

foldico_x2 = np.array(fold_x2)
foldico_y2 = np.array(fold_y2)

foldico_x3 = np.array(fold_x3)
foldico_y3 = np.array(fold_y3)

foldico_x4 = np.array(fold_x4)
foldico_y4 = np.array(fold_y4)

foldico_x5 = np.array(fold_x5)
foldico_y5 = np.array(fold_y5)

foldico_x = [foldico_x1, foldico_x2, foldico_x3, foldico_x4, foldico_x5]
foldico_y = [foldico_y1, foldico_y2, foldico_y3, foldico_y4, foldico_y5]




######## Loading models ###########


k = 5
models41to40 = []
models42to40 = []

modelsicton = []
modelsictono = []


for i in range(0, k):
    model_name = 'models/nn-icon17v2' + str(i + 1) + '.h5'
    model_current = load_model(model_name)
    modelsicton.append(model_current)

    model_name = 'models/nn-icon17-ov2' + str(i + 1) + '.h5'
    model_current = load_model(model_name)
    modelsictono.append(model_current)

    model_name = 'models/nn-41to40v2' + str(i + 1) + '.h5'
    model_current = load_model(model_name)
    models41to40.append(model_current)

    model_name = 'models/nn-42to40v2' + str(i + 1) + '.h5'
    model_current = load_model(model_name)
    models42to40.append(model_current)

   




if DEBUG: 
    print(len(modelsicton), len(modelsictono), len(models41to40), len(models42to40))


########### Predicting ################

pred_ic = []
pred_io = []
pred_41 = []
pred_42 = []


for i in range(0, k):
    pred_ic.append(modelsicton[i].predict(foldic_x[(k-1)-i])) #Becausa the first model was trained with fold 5.
    pred_io.append(modelsictono[i].predict(foldico_x[(k-1)-i]))
    pred_41.append(models41to40[i].predict(fold41_x[(k-1)-i]))
    pred_42.append(models42to40[i].predict(fold42_x[(k-1)-i]))
    



if DEBUG:
    print(pred_ic[0][0], pred_io[0][0], pred_41[0][0], pred_42[0][0])

########### Take the infos to unnormalize the data #####################

info_file = "masks/mask-edfa1-padtec-icton17-infov2.txt"

file = open( info_file, 'r')

lines = file.readlines()
auxiliary = lines[0].split()
max_gch = auxiliary[4]
max_nf = auxiliary[5]
max_pinto = auxiliary[0]
max_gain = auxiliary[1]
auxiliary = lines[1].split()
min_gch = auxiliary[4]
min_nf = auxiliary[5]
min_pinto = auxiliary[0]
min_gain = auxiliary[1]
auxiliary = lines[2].split()
range_a = auxiliary[0]
range_b = auxiliary[1] 

file.close()

if DEBUG:
    print(max_gch, max_nf, min_gch, min_gch, range_a, range_b)


info_file = 'masks/mask-edfa1-padtec-new-models-infov2.txt'

file = open( info_file, 'r')

lines = file.readlines()

auxiliary = lines[0].split()
max_gset = float(auxiliary[0])
max_pin = float(auxiliary[1])
max_pout = float(auxiliary[3])

auxiliary = lines[1].split()
min_gset = float(auxiliary[0])
min_pin = float(auxiliary[1])
min_pout = float(auxiliary[3])

file.close()


if DEBUG:
    print(max_gset, min_gset, max_pout, min_pout)

########## Calcule the error ############

pred_y41 = []
pred_y42 = []
pred_yic = []
pred_yio = []

pred_x41 = []
pred_x42 = []
pred_xic = []
pred_xio = []

test_y41 = []
test_y42 = []
test_yic = []
test_yio = []

for i in range(0, len(pred_41)):
    pred_y41.append(unnormalization(pred_41[i], min_pout, max_pout, range_a, range_b))
    pred_y42.append(unnormalization(pred_42[i], min_pout, max_pout, range_a, range_b))
    pred_yic.append(unnormalizationic(pred_ic[i], min_gch, max_gch, min_nf, max_nf, range_a, range_b))
    pred_yio.append(unnormalizationic(pred_io[i], min_gch, max_gch, min_nf, max_nf, range_a, range_b))
    
    pred_x41.append(unnormalization_in(fold41_x[(k-1)-i], min_gset, max_gset, min_pin, max_pin, range_a, range_b))
    pred_x42.append(unnormalization_in(fold42_x[(k-1)-i], min_gset, max_gset, min_pin, max_pin, range_a, range_b))
    pred_xic.append(unnormalizationicin(foldic_x[(k-1)-i], min_pinto, max_pinto, min_gain, max_gain, range_a, range_b))
    pred_xio.append(unnormalizationicin(foldico_x[(k-1)-i], min_pinto, max_pinto, min_gain, max_gain, range_a, range_b))
    
    test_y41.append(unnormalization(fold41_y[(k-1)-i], min_pout, max_pout, range_a, range_b))
    test_y42.append(unnormalization(fold42_y[(k-1)-i], min_pout, max_pout, range_a, range_b))
    test_yic.append(unnormalizationic(foldic_y[(k-1)-i], min_gch, max_gch, min_nf, max_nf, range_a, range_b))
    test_yio.append(unnormalizationic(foldico_y[(k-1)-i], min_gch, max_gch, min_nf, max_nf, range_a, range_b))

print(pred_xic[0])


if DEBUG:
    print(pred_y41[4][0], test_y41[4][0], test_yic[0][0])
    print(pred_x41[0][0], len(pred_x41[0]))


diffs_41 = []
diffs_42 = []
diffs_ic = []
diffs_io = []


for i in range(0 , len(pred_y41)):
    diff_current = []
    for j in range(0, len(pred_y41[i])):
        current = pred_y41[i][j]

        current_in = pred_x41[i][j]
        biggest_current = 0
        diff = int(0)
        for k in range(0, len(current)):
            diff = abs(current[k] - test_y41[i][j][k])
            if diff > biggest_current:
                biggest_current = diff
            if DEBUG:
                print(current[k], test_y41[i][j][k])
        diff_current.append(biggest_current)
    diffs_41.append(diff_current)



if DEBUG:
    print(len(diffs_41))

for i in range(0 , len(pred_y42)):
    diff_current = []
    for j in range(0, len(pred_y42[i])):
        current = pred_y42[i][j]
        current_in = pred_x42[i][j]
        biggest_current = 0
        diff = int(0)
        for k in range(0, len(current)):
            diff = abs(current[k] - test_y42[i][j][k])
            if diff > biggest_current:
                biggest_current = diff
            if DEBUG:
                print(current[k], test_y42[i][j][k])
        diff_current.append(biggest_current)
    diffs_42.append(diff_current)

if DEBUG:
    print(len(diffs_42))



diffs_nf = []

for i in range(0 , len(pred_yic)):
    diff_current = []
    diff_current2 = []
    j = 0
    while j < len(pred_yic[i]):
        
        current_in = [[pred_xic[i][j][0], 0], pred_xic[i][j][1]]
        current = []
        current_t = []
        for step in range(0, number_channels):
            current.append(pred_yic[i][j + step][0]) 
            current_t.append(test_yic[i][j + step][0])
        
        j += step + 1
        
        biggest_current = 0
        diff = int(0)
        for p in range(0, len(current)):
            diff = abs(current[p] - current_t[p])
            if diff > biggest_current:
                biggest_current = diff

        diff_current.append(biggest_current)
    diffs_ic.append(diff_current)
    diffs_nf.append(diff_current2)

if DEBUG:
    print(len(diffs_ic[0]))


diffs_nf2 = []

for i in range(0 , len(pred_yio)):
    diff_current = []
    diff_current2 = []
    j = 0
    while j < len(pred_yio[i]):
        
        current_in = [[pred_xio[i][j][0], 0], pred_xio[i][j][1]]
        current = []
        current_t = []
        for step in range(0, number_channels):
            current.append(pred_yio[i][j + step][0]) 
            current_t.append(test_yio[i][j + step][0])
        
        j += step + 1
        
        biggest_current = 0
        diff = int(0)
        for p in range(0, len(current)):
            diff = abs(current[p] - current_t[p])
            if diff > biggest_current:
                biggest_current = diff

        diff_current.append(biggest_current)
        
    diffs_io.append(diff_current)
    diffs_nf2.append(diff_current2)

if DEBUG:
    print(len(diffs_io[0]))


########## Boxplot #######################

plt.figure(figsize=(15,12))


plt.boxplot([
            np.concatenate((diffs_io[0], diffs_io[1], diffs_io[2], diffs_io[3], diffs_io[4]), axis = 0),
            np.concatenate((diffs_ic[0], diffs_ic[1], diffs_ic[2], diffs_ic[3], diffs_ic[4]), axis = 0),         #icton17 with tilt 
            np.concatenate((diffs_41[0], diffs_41[1], diffs_41[2], diffs_41[3], diffs_41[4]), axis = 0),         #41to40 
            np.concatenate((diffs_42[0], diffs_42[1], diffs_42[2], diffs_42[3], diffs_42[4]), axis = 0),         #42to40 with tilt
            ])        

plt.xticks([1, 2, 3, 4], ['PerChannel', 'PerChannel-Tilt', 'Spectrum', 'Spectrum-Tilt'], rotation=45)
plt.ylabel('Maximum Error (dB)')
plt.tight_layout()

plt.savefig('plots/BiggestErrorNNsBoxPlot.pdf', dpi = 200)

plt.figure(figsize=(10,8))

plt.boxplot([
            np.concatenate((diffs_41[0], diffs_41[1], diffs_41[2], diffs_41[3], diffs_41[4]), axis = 0),         #41to40 
            np.concatenate((diffs_42[0], diffs_42[1], diffs_42[2], diffs_42[3], diffs_42[4]), axis = 0),         #42to40 with tilt
            ])        

plt.xticks([1, 2], ['Spectrum', 'Spectrum-Tilt'])
plt.ylabel('MSE (dB)')


plt.savefig('plots/BiggestErrorNNsBoxPlotZoom.pdf', dpi = 200)

plt.figure(figsize=(8,6))

io = np.concatenate((diffs_io[0], diffs_io[1], diffs_io[2], diffs_io[3], diffs_io[4]), axis = 0)
ic = np.concatenate((diffs_ic[0], diffs_ic[1], diffs_ic[2], diffs_ic[3], diffs_ic[4]), axis = 0)
n4140 = np.concatenate((diffs_41[0], diffs_41[1], diffs_41[2], diffs_41[3], diffs_41[4]), axis = 0)
n4240 = np.concatenate((diffs_42[0], diffs_42[1], diffs_42[2], diffs_42[3], diffs_42[4]), axis = 0)

errors = [io, ic, n4140, n4240]

pickle_out = open("errors/edfa1-biggest.obj","wb")
pickle.dump(errors, pickle_out)
pickle_out.close()


col_labels = ['mean', 'std']
row_labels = ['ICTON', 'ICTONwT', '41-to-40', '42-to-40']

table_vals = [[round(np.mean(io), 4), round(np.std(io), 4)], 
              [round(np.mean(ic), 4), round(np.std(ic), 4)], 
              [round(np.mean(n4140), 4), round(np.std(n4140), 4)],
              [round(np.mean(n4240), 4), round(np.std(n4240), 4)]] 

# Draw table
the_table = plt.table(cellText=table_vals,
                      colWidths=[0.1] * 3,
                      rowLabels=row_labels,
                      colLabels=col_labels,
                      loc='center')
the_table.auto_set_font_size(False)
the_table.set_fontsize(20)
the_table.scale(4, 4)
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
for pos in ['right','top','bottom','left']:
    plt.gca().spines[pos].set_visible(False)

plt.savefig('plots/BiggestErrorTableNNsBoxPlot.pdf', dpi = 200)

