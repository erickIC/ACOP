import numpy as np
import keras as ks

number_of_channels = 40

'''
	This method is used to normalize data. It takes a value, with min and max of the respective parameter
	and the desired range of the output.
'''
def normalization(x, min, max, range_a, range_b):
	z = ((float(range_b) - float(range_a)) * ((x - float(min))/(float(max) - float(min)))) + float(range_a)
	return z

'''
	This method is used to unnormalize data. It takes a matrix, with min and max of the respective parameter
	and the range at which the data was normalized.
'''
def unnormalization(data, min, max, range_a, range_b):
	unnormalized_data = []
	for i in range(0, data.shape[0]):
		values = []
		for j in range(0, data.shape[1]):
			values.append(((float(data[i][j]) - float(range_a)) * (float(max)-float(min))) / (float(range_b) - float(range_a)) + float(min))
		unnormalized_data.append(values)
	return np.array(unnormalized_data)

'''
	Main
'''
def neuralNetworkMethod(training_data, test_data):
	## Normalizing 'training_data', saving it's info for further use
	# Max and Min of Gset
	max_gset = training_data[0][0]
	min_gset = training_data[0][0]

	for i in range(1, training_data.shape[0]):
		if training_data[i][0] > max_gset:
			max_gset = training_data[i][0]
			continue
		if training_data[i][0] < min_gset:
			min_gset = training_data[i][0]

	# Max and Min of Pin
	max_pin = training_data[0][1]
	min_pin = training_data[0][1]

	for i in range(0, training_data.shape[0]):
		for j in range(1, 41):
			if training_data[i][j] > max_pin:
				max_pin = training_data[i][j]
				continue
			if training_data[i][j] < min_pin:
				min_pin = training_data[i][j]

	# Max and Min of Tilt
	max_tilt = training_data[0][41]
	min_tilt = training_data[0][41]

	for i in range(1, training_data.shape[0]):
		if training_data[i][41] > max_tilt:
			max_tilt = training_data[i][41]
			continue
		if training_data[i][41] < min_tilt:
			min_tilt = training_data[i][41]

	# Max and Min of Pout
	max_pout = training_data[0][42]
	min_pout = training_data[0][42]

	for i in range(0, training_data.shape[0]):
		for j in range(42, 82):
			if training_data[i][j] > max_pout:
				max_pout = training_data[i][j]
				continue
			if training_data[i][j] < min_pout:
				min_pout = training_data[i][j]

	# Max and Min of Noise Figure
	max_nf = training_data[0][82]
	min_nf = training_data[0][82]

	for i in range(0, training_data.shape[0]):
		for j in range(82, training_data.shape[1]):
			if training_data[i][j] > max_nf:
				max_nf = training_data[i][j]
				continue
			if training_data[i][j] < min_nf:
				min_nf = training_data[i][j]
	
	# Define normalization range
	range_a = 0.15
	range_b = 0.85

	# Normalizing
	normalized_training_data = np.empty_like(training_data)

	for i in range(0, training_data.shape[0]):
		normalized_training_data[i][0] = normalization(training_data[i][0], min_gset, max_gset, range_a, range_b)
		for j in range(1, 1+number_of_channels):
			normalized_training_data[i][j] = normalization(training_data[i][j], min_pin, max_pin, range_a, range_b)
		normalized_training_data[i][41] = normalization(training_data[i][41], min_tilt, max_tilt, range_a, range_b)
		for j in range(42, 42+number_of_channels):
			normalized_training_data[i][j] = normalization(training_data[i][j], min_pout, max_pout, range_a, range_b)
		for j in range(82, training_data.shape[1]):
			normalized_training_data[i][j] = normalization(training_data[i][j], min_nf, max_nf, range_a, range_b)
	
	## Normalizing 'test_data' for prediction
	normalized_test_data = np.empty_like(test_data)

	for i in range(0, test_data.shape[0]):
		normalized_test_data[i][0] = normalization(test_data[i][0], min_gset, max_gset, range_a, range_b)
		for j in range(1, 1+number_of_channels):
			normalized_test_data[i][j] = normalization(test_data[i][j], min_pin, max_pin, range_a, range_b)
		normalized_test_data[i][41] = normalization(test_data[i][41], min_tilt, max_tilt, range_a, range_b)
		for j in range(42, 42+number_of_channels):
			normalized_test_data[i][j] = normalization(test_data[i][j], min_pout, max_pout, range_a, range_b)
		for j in range(82, test_data.shape[1]):
			normalized_test_data[i][j] = normalization(test_data[i][j], min_nf, max_nf, range_a, range_b)
	
	## Building Neural Network
	training_input = normalized_training_data[:, :42]
	training_output = normalized_training_data[:, 42:42+number_of_channels]
	test_input = normalized_test_data[:, :42]
	test_output = normalized_test_data[:, 42:42+number_of_channels]

	num_epochs = 5000
	
	model = ks.models.Sequential()

	model.add(ks.layers.Dense(55, input_dim = 42, activation='sigmoid'))
	model.add(ks.layers.Dropout(0.1))
	model.add(ks.layers.Dense(55, activation='sigmoid'))
	model.add(ks.layers.Dense(40, activation='sigmoid'))

	model.compile(optimizer = 'adam', loss = 'mse', metrics = ['acc'])

	cb = ks.callbacks.EarlyStopping(monitor = 'val_loss', min_delta = 0, patience = 120, verbose = 0, mode='auto')

	model.fit(training_input, training_output, validation_data=(test_input, test_output), epochs = num_epochs, callbacks=[cb])

	# Executing prediction
	normalized_p_out = model.predict(test_input)

	# Unnormalizing predicted data
	p_out = unnormalization(normalized_p_out, min_pout, max_pout, range_a, range_b)

	# Returning P_out prediction
	return p_out