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

def unnormalizationic(data, min_gch, max_gch, min_nf, max_nf, range_a, range_b):
	unnormalized_data = []
	for i in range(0, data.shape[0]):
		values = []
		values.append(((float(data[i][0]) - float(range_a)) * (float(max_gch)-float(min_gch))) / (float(range_b) - float(range_a)) + float(min_gch))
		values.append(((float(data[i][1]) - float(range_a)) * (float(max_nf)-float(min_nf))) / (float(range_b) - float(range_a)) + float(min_nf))
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

#### Getting the folds
input_folder1 = "masks/mask-edfa1-padtec-new-models-fold-1.txt"
input_folder2 = "masks/mask-edfa1-padtec-new-models-fold-2.txt"
input_folder3 = "masks/mask-edfa1-padtec-new-models-fold-3.txt"
input_folder4 = "masks/mask-edfa1-padtec-new-models-fold-4.txt"
input_folder5 = "masks/mask-edfa1-padtec-new-models-fold-5.txt"

DEBUG = False

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

#################################### ICTON 17 ##################################################


input_folder1 = "masks/mask-edfa1-padtec-icton17-fold-1.txt"
input_folder2 = "masks/mask-edfa1-padtec-icton17-fold-2.txt"
input_folder3 = "masks/mask-edfa1-padtec-icton17-fold-3.txt"
input_folder4 = "masks/mask-edfa1-padtec-icton17-fold-4.txt"
input_folder5 = "masks/mask-edfa1-padtec-icton17-fold-5.txt"

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

######## Loading models ###########

k = 5
models41to40 = []
models42to40 = []
modelsicton = []



for i in range(0, k):
    model_name = 'models/nn-icon17' + str(i + 1) + '.h5'
    model_current = load_model(model_name)
    modelsicton.append(model_current)

    model_name = 'models/nn-41to40' + str(i + 1) + '.h5'
    model_current = load_model(model_name)
    models41to40.append(model_current)

    model_name = 'models/nn-42to40' + str(i + 1) + '.h5'
    model_current = load_model(model_name)
    models42to40.append(model_current)

if DEBUG: 
    print(len(modelsicton), len(models41to40), len(models42to40))


########### Predicting ################

pred_ic = []
pred_41 = []
pred_42 = []

for i in range(0, k):
    pred_ic.append(modelsicton[i].predict(foldic_x[(k-1)-i])) #Becausa the first model was trained with fold 5.
    pred_41.append(models41to40[i].predict(fold41_x[(k-1)-i]))
    pred_42.append(models42to40[i].predict(fold42_x[(k-1)-i]))

if DEBUG:
    print(pred_ic[0][0], pred_41[0][0], pred_42[0][0])

########### Take the infos to unnormalize the data #####################

info_file = "masks/mask-edfa1-padtec-icton17-info.txt"

file = open( info_file, 'r')

lines = file.readlines()
auxiliary = lines[0].split()
max_gch = auxiliary[4]
max_nf = auxiliary[5]
auxiliary = lines[1].split()
min_gch = auxiliary[4]
min_nf = auxiliary[5]
auxiliary = lines[2].split()
range_a = auxiliary[0]
range_b = auxiliary[1] 

file.close()

if DEBUG:
    print(max_gch, max_nf, min_gch, min_gch, range_a, range_b)


info_file = 'masks/mask-edfa1-padtec-new-models-info.txt'

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

test_y41 = []
test_y42 = []
test_yic = []

for i in range(0, len(pred_41)):
    pred_y41.append(unnormalization(pred_41[i], min_pout, max_pout, range_a, range_b))
    pred_y42.append(unnormalization(pred_42[i], min_pout, max_pout, range_a, range_b))
    pred_yic.append(unnormalizationic(pred_ic[i], min_gch, max_gch, min_nf, max_nf, range_a, range_b))

    test_y41.append(unnormalization(fold41_y[(k-1)-i], min_pout, max_pout, range_a, range_b))
    test_y42.append(unnormalization(fold42_y[(k-1)-i], min_pout, max_pout, range_a, range_b))
    test_yic.append(unnormalizationic(foldic_y[(k-1)-i], min_gch, max_gch, min_nf, max_nf, range_a, range_b))

if DEBUG:
    print(pred_y41[4][0], test_y41[4][0], test_yic[0][0])


diffs_41 = []
diffs_42 = []
diffs_ic = []


for i in range(0 , len(pred_y41)):
    diff_current = []
    for j in range(0, len(pred_y41[i])):
        current = pred_y41[i][j]
        diff = int(0)
        for k in range(0, len(current)):
            diff += abs(current[k] - test_y41[i][j][k])
            if DEBUG:
                print(current[k], test_y41[i][j][k])
        diff_current.append(diff/len(current))
    diffs_41.append(diff_current)

if DEBUG:
    print(len(diffs_41))

for i in range(0 , len(pred_y42)):
    diff_current = []
    for j in range(0, len(pred_y42[i])):
        current = pred_y42[i][j]
        diff = int(0)
        for k in range(0, len(current)):
            diff += abs(current[k] - test_y42[i][j][k])
            if DEBUG:
                print(current[k], test_y42[i][j][k])
        diff_current.append(diff/len(current))
    diffs_42.append(diff_current)

if DEBUG:
    print(len(diffs_42))

diffs_nf = []

for i in range(0 , len(pred_yic)):
    diff_current = []
    diff_current2 = []
    for j in range(0, len(pred_yic[i])):
        
        
        current = pred_yic[i][j]
        

        diff = int(0)
        diff2 = int(0)
        
        diff += abs(current[0] - test_yic[i][j][0])
        diff2 += abs(current[1] - test_yic[i][j][1])
        if DEBUG:
            print(current[0], test_yic[i][j][0])

        diff_current.append(diff)
        diff_current2.append(diff2)
    diffs_ic.append(diff_current)
    diffs_nf.append(diff_current2)

if DEBUG:
    print(len(diffs_ic[0]))


########## Boxplot #######################

plt.figure(figsize=(16,10))

plt.subplot(211)
plt.boxplot([diffs_ic[0], diffs_ic[1], diffs_ic[2], diffs_ic[3], diffs_ic[4], np.concatenate((diffs_ic[0], diffs_ic[1], diffs_ic[2], diffs_ic[3], diffs_ic[4]), axis = 0)])
plt.title('Absolute difference Gch ICTON')
plt.xticks([1, 2, 3, 4, 5, 6], ['Fold5', 'Fold4', 'Fold3', 'Fold2', 'Fold1', 'all'])
plt.ylabel('(dB)')

plt.subplot(212)
plt.boxplot([diffs_41[0], diffs_41[1], diffs_41[2], diffs_41[3], diffs_41[4], np.concatenate((diffs_41[0], diffs_41[1], diffs_41[2], diffs_41[3], diffs_41[4]), axis = 0), 
diffs_42[0], diffs_42[1], diffs_42[2], diffs_42[3], diffs_42[4], np.concatenate((diffs_42[0], diffs_42[1], diffs_42[2], diffs_42[3], diffs_42[4]), axis = 0)])
plt.title('Absolute difference Pout')
plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], ['41-Fold5', '41-Fold4', '41-Fold3', '41-Fold2', '41-Fold1', '41-all', '42-Fold5', '42-Fold4', '42-Fold3', '42-Fold2', '42-Fold1', '42-all'])

plt.savefig('DifferentsNNsBoxPlot.png', dpi = 200)