import numpy as np
import matplotlib.pyplot as plt
import pickle

def unnormalization(data: np.array, min: float, max: float, range_a: float, range_b: float) -> np.array:
	unnormalized_data = []
	
	values = []
	for j in range(0, data.shape[0]):
		values.append(((float(data[j]) - float(range_a)) * (float(max)-float(min))) / (float(range_b) - float(range_a)) + float(min))
	unnormalized_data.append(values)
	return np.array(unnormalized_data)

def calculete_error_per_layers(number_of_hidden_layers: int, neurons: list, number_of_folds: int) -> list:
	biggests_per_model = []
	for neuron in neurons:
		file_name = 'models/nn-layers-'+ str(number_of_hidden_layers) + '-neurons-'+ str(neuron) + '-history.obj'
		with open(file_name, 'rb') as file:
			histories = pickle.load(file)
			errors = histories[1]
			biggest = -1
			for i in range(0, number_of_folds):
				if errors[i][len(errors[i])-1] > biggest:
					biggest = errors[i][len(errors[i])-1]

			biggests_per_model.append(biggest)

	return biggests_per_model


if __name__ == '__main__':

	#Set the font sizes to the plots
	smaller_size = 14
	medium_size = 16
	bigger_size = 24
	plt.rc('font', size=medium_size)             # controls default text sizes
	plt.rc('axes', titlesize=medium_size)        # fontsize of the axes title
	plt.rc('axes', labelsize=medium_size)        # fontsize of the x and y labels
	plt.rc('xtick', labelsize=smaller_size)      # fontsize of the tick labels
	plt.rc('ytick', labelsize=smaller_size)      # fontsize of the tick labels
	plt.rc('legend', fontsize=smaller_size)       # legend fontsize
	plt.rc('figure', titlesize=medium_size)      # fontsize of the figure title
	
	number_of_folds = 5
	number_of_hidden_layers = [2, 3, 4, 5]
	number_of_neurons = [32, 64, 128, 256, 512, 1024]

	ann_2_layer = calculete_error_per_layers(2, number_of_neurons, number_of_folds)
	ann_3_layer = calculete_error_per_layers(3, number_of_neurons, number_of_folds)
	ann_4_layer = calculete_error_per_layers(4, number_of_neurons, number_of_folds)
	ann_5_layer = calculete_error_per_layers(5, number_of_neurons, number_of_folds)

	plt.figure()

	plt.plot(number_of_neurons, ann_2_layer, '-*', label='2-layer ANN')
	plt.plot(number_of_neurons, ann_3_layer, '-o', label='3-layer ANN')
	plt.plot(number_of_neurons, ann_4_layer, '-<', label='4-layer ANN')
	plt.plot(number_of_neurons, ann_5_layer, '-p', label='5-layer ANN')
	plt.ylabel('MSE')
	plt.xlabel('number of neuros in each hidden layer')
	plt.legend()
	plt.tight_layout()
	plt.grid(True)

	plt.savefig('results/TrainingErrorBiggest.pdf', dpi = 200)


