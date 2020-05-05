import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import keras
from keras.models import load_model

def unnormalization(data: np.array, min: float, max: float, range_a: float, range_b: float) -> np.array:
	unnormalized_data = []
	
	values = []
	for j in range(0, data.shape[0]):
		values.append(((float(data[j]) - float(range_a)) * (float(max)-float(min))) / (float(range_b) - float(range_a)) + float(min))
	unnormalized_data.append(values)
	return np.array(unnormalized_data)
	
def normalization(x: float, min: float, max: float, range_a: float, range_b: float) -> float:	
	z = ( (float(range_b) - float(range_a)) * ( (x - float(min))/(float(max) - float(min)) ) ) + float(range_a)
	return z


def first_scenario():
    ##TO DO
    pass

def second_scenario():
    ##TO DO
    pass

def third_scenario():
    ##TO DO
    pass

if __name__ == '__main__':
    smaller_size = 8
    medium_size = 10
    bigger_size = 16
    plt.rc('font', size=medium_size)             # controls default text sizes
    plt.rc('axes', titlesize=medium_size)        # fontsize of the axes title
    plt.rc('axes', labelsize=medium_size)        # fontsize of the x and y labels
    plt.rc('xtick', labelsize=smaller_size)      # fontsize of the tick labels
    plt.rc('ytick', labelsize=smaller_size)      # fontsize of the tick labels
    plt.rc('legend', fontsize=smaller_size)       # legend fontsize
    plt.rc('figure', titlesize=medium_size)      # fontsize of the figure title

    ## Taking information to normalization.

    input_file = "masks/mask-edfa1-padtec-new-models-infov2.txt"

    with open(input_file, 'r') as f_in:

        lines = f_in.readlines()
        auxiliary = lines[0].split()
        max_gset = float(auxiliary[0])
        max_pin = float(auxiliary[1])
        max_pout = float(auxiliary[3])

        auxiliary = lines[1].split()
        min_gset = float(auxiliary[0])
        min_pin = float(auxiliary[1])
        min_pout = float(auxiliary[3])

        auxiliary = lines[2].split()
        range_a = auxiliary[0]
        range_b = auxiliary[1]

        print(max_gset, min_gset, max_pout, min_pout, range_a, range_b)

    number_of_folds = 5
    number_of_hidden_layers = [2, 3, 4, 5]
    number_of_neurons = [32, 64, 128, 256, 512, 1024]