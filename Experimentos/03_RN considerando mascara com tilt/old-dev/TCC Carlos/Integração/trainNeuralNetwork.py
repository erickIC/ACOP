import numpy as np
from numpy import median
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
from keras import callbacks
from keras.layers import Dropout
from random import randint 

def normalization(x, min, max, range_a, range_b):
	z = ((float(range_b) - float(range_a)) * ((x - float(min))/(float(max) - float(min)))) + float(range_a)
	return z

def unnormalization(data, min, max, range_a, range_b):
	unnormalized_data = []
	for i in range(0, data.shape[0]):
		values = []
		for j in range(0, data.shape[1]):
			values.append(((float(data[i][j]) - float(range_a)) * (float(max)-float(min))) / (float(range_b) - float(range_a)) + float(min))
			#print(((float(data[i][j]) - float(range_a)) * (float(max)-float(min))), (float(range_b) - float(range_a)), float(min))
			#print(data[i][j], min, max, range_a, range_b, ((float(data[i][j]) - float(range_a)) * (float(max)-float(min))) / (float(range_b) - float(range_a)) + float(min))
		unnormalized_data.append(values)
	return np.array(unnormalized_data)


class TrainNeuralNetwork(object):
    def __init__(self, mask_name):
        self.mask_name = mask_name
        self.__channels = 0
        self.__x_input = []
        self.__x_norm = []
        self.__y_norm = []
        self.__y_pure = []
        self.range_a = 0.15
        self.range_b = 0.85
        self.__max_gset = 0
        self.__max_pin = 0
        self.__max_pout = 0
        self.__min_gset = 0
        self.__min_pin = 0
        self.__min_pout = 0
        self.__x_train = []
        self.__y_train = []
        self.__x_test = []
        self.__y_test = []
        self.__y_test_pure = []
        self.history = []
        self.errors = []


    def take_the_input(self):
        f = open(self.mask_name, 'r+')
        entries = f.readlines()
        header = entries[0].split(';')

        self.__pin_init = 0
        self.__pout_init = 0
        self.__gset_init = 0

        got_pin_init = False
        got_pout_init = False
        got_gset_init = False

        for i in range(0, len(header)):
            if header[i] == 'Ganho Total Set (dB)' and not got_gset_init:
                self.__gset_init = i
                got_gset_init = True

            if header[i] == 'Pin Canal (dBm)' and not got_pin_init:
                self.__pin_init = i
                got_pin_init = True

            if header[i] == 'Pout Canal (dBm)' and not got_pout_init:
                self.__pout_init = i
                got_pout_init = True

            if header[i] == 'Pin Canal (dBm)':
                self.__channels = self.__channels + 1
    
        print(self.__gset_init, self.__pin_init, self.__pout_init, self.__channels)
        print(header[self.__gset_init], header[self.__pin_init], header[self.__pout_init])

        for l in range(1, len(entries)):
            line = entries[l].split(';')
            aux1 = []
            aux2 = []
            aux3 = []
            for i in range(0, self.__channels):
                aux1.append(line[self.__pin_init + i])
                aux2.append(line[self.__pout_init + i])

            aux3 = [line[self.__gset_init]] + aux1 + aux2

            if '' in aux3:
                for i in range(0, len(aux3)):
                    if aux3[i] == '':
                        aux3[i] = '0'
                        
            self.__x_input.append(aux3)    


        print(len(self.__x_input))
        for i in range(0, len(self.__x_input)):
            for j in range(0, len(self.__x_input[i])):
                if ',' in self.__x_input[i][j]:
                    u = self.__x_input[i][j].split(',')
                    self.__x_input[i][j] = u[0] + '.' + u[1]    

                self.__x_input[i][j] = float(self.__x_input[i][j])

    def normalizing_data(self):
        self.__max_gset = self.__x_input[0][0]
        self.__max_pin = self.__x_input[0][1]
        self.__max_pout = self.__x_input[0][self.__channels + 1]

        self.__min_gset = self.__x_input[0][0]
        self.__min_pin = self.__x_input[0][1]
        self.__min_pout = self.__x_input[0][self.__channels + 1]

        for i in range(1, len(self.__x_input)):
            if self.__x_input[i][0] > self.__max_gset:
                self.__max_gset = self.__x_input[i][0]
            
            if self.__x_input[i][0] < self.__min_gset:
                self.__min_gset = self.__x_input[i][0]
        
        for i in range(0, len(self.__x_input)):
            for j in range(0, self.__channels):
                if self.__x_input[i][1 + j] > self.__max_pin:
                    self.__max_pin = self.__x_input[i][1 + j]
                
                if self.__x_input[i][1 + j] < self.__min_pin:
                    self.__min_pin = self.__x_input[i][1 + j]
                
                if self.__x_input[i][self.__channels + 1 + j] > self.__max_pout:
                    self.__max_pout = self.__x_input[i][self.__channels + 1 + j]
                
                if self.__x_input[i][self.__channels + 1 + j] < self.__min_pout:
                    self.__min_pout = self.__x_input[i][self.__channels + 1 + j]
        
        print(self.__max_gset, self.__max_pin, self.__max_pout)
        print(self.__min_gset, self.__min_pin, self.__min_pout)

        for i in range(0, len(self.__x_input)):
            pins = []
            pouts = []
            pouts_pure = []

            for j in range(0, self.__channels):
                pins.append(normalization(self.__x_input[i][1 + j], self.__min_pin, self.__max_pin, self.range_a, self.range_b))
                pouts.append(normalization(self.__x_input[i][self.__channels + 1 + j], self.__min_pout, self.__max_pout, self.range_a, self.range_b))
                pouts_pure.append(self.__x_input[i][self.__channels + 1 + j])

            self.__x_norm.append([normalization(self.__x_input[i][0], self.__min_gset, self.__max_gset, self.range_a, self.range_b)] + pins)
            self.__y_norm.append(pouts)
            self.__y_pure.append(pouts_pure)
        
        print(len(self.__x_norm), len(self.__y_norm), len(self.__x_norm[0]), len(self.__y_norm[0]))
        self.__x_norm = np.array(self.__x_norm)
        self.__y_norm = np.array(self.__y_norm)
        self.__y_pure = np.array(self.__y_pure)

    def split_train_and_test(self):
        caught = [False] * len(self.__x_norm)
        eighty_percent = int(0.8 * len(self.__x_norm))

        while len(self.__x_train) != eighty_percent:
            current = randint(0, len(caught) - 1)
            
            if not caught[current]:
                self.__x_train.append(self.__x_norm[current])
                self.__y_train.append(self.__y_norm[current])
                caught[current] = True

        for i in range(0, len(caught)):
            if not caught[i]:
                self.__x_test.append(self.__x_norm[i])
                self.__y_test.append(self.__y_norm[i])
                self.__y_test_pure.append(self.__y_pure[i])
                caught[current] = True

        self.__x_train = np.array(self.__x_train)
        self.__y_train = np.array(self.__y_train)
        self.__x_test = np.array(self.__x_test)
        self.__y_test = np.array(self.__y_test)

    def train_neural_network(self):
        self.take_the_input()
        self.normalizing_data()
        self.split_train_and_test()

        num_epochs = 5000

        self.model = Sequential()
        num_neurons_hidden = int((len(self.__x_train[0]) + len(self.__y_train[0])) * 2/3)
        self.model.add(Dense(num_neurons_hidden, input_dim=len(self.__x_train[0]), activation='sigmoid'))
        self.model.add(Dropout(0.1))
        self.model.add(Dense(num_neurons_hidden, activation='sigmoid'))
        self.model.add(Dense(len(self.__y_train[0]), activation='sigmoid'))
        
        self.model.compile(optimizer = 'adam', loss = 'mse', metrics = ['acc'])
        cb = callbacks.EarlyStopping(monitor = 'val_loss', min_delta = 0, patience = 120, verbose = 0, mode='auto')

        self.model.summary()

        self.history = self.model.fit(self.__x_train, self.__y_train, validation_data=(self.__x_test, self.__y_test), epochs = num_epochs,callbacks=[cb])

        self.model.save(self.mask_name.split('.')[0] + '-model.h5')

        y_pred_norm = self.model.predict(self.__x_test)
        y_pred = unnormalization(y_pred_norm, self.__min_pout, self.__max_pout, self.range_a, self.range_b)
        y_test = unnormalization(self.__y_test, self.__min_pout, self.__max_pout, self.range_a, self.range_b)
        

        for i in range(0, len(y_pred)):
            diff = (0)
            for j in range(0, len(y_pred[i])):
                diff += abs(y_pred[i][j] - y_test[i][j])
                
            
            self.errors.append(diff/len(y_pred[i]))
        
        output_file = self.mask_name.split('.')[0] + '-info.txt'
        with open(output_file, 'w') as f_out:
            new_line = str(self.__max_gset) + '\t' + str(self.__max_pin) + '\t' + str(self.__max_pout) + '\n'
            new_line += str(self.__min_gset) + '\t' + str(self.__min_pin) + '\t' + str(self.__min_pout) + '\n'
            new_line += str(self.range_a) + '\t' + str(self.range_b)
            f_out.write(new_line + '\n')

            new_line = ''
            new_line2 = ''
            
            loss = self.history.history['val_loss']
            epoch = self.history.epoch
            
            for i in range(0, len(loss)):
                new_line += str(loss[i]) + '\t'
                new_line2 += str(epoch[i]) + '\t'
            
            new_line += '\n' + new_line2

            f_out.write(new_line + '\n')

            new_line = ''


            for i in range(0, len(self.errors)):
                new_line += str(self.errors[i]) + '\t'

            
            f_out.write(new_line + '\n')



if __name__ == '__main__':
    string_path = "mascara.csv"   
    nn = TrainNeuralNetwork(string_path)
    nn.train_neural_network()
    



