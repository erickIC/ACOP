'''
	This script loads the NN convergence history objects for each tilt step and plot the data
	on a single figure.
'''

import pickle
import matplotlib.pyplot as plt
import numpy as np

groups = [2, 3]
mask_quantities = [5, 3]
histories = []

# Loading each step convergence history
for group in groups:
	input_object = 'models/nn-history-for-group-' + str(group) + '.obj'
	with open(input_object, 'rb') as history_obj:
		histories.append(pickle.load(history_obj))

# Plotting convergence curve for each step on a single figure
forms = ['--', '-^']
indexes = np.arange(0, len(histories))

font = {'size' : 24}
plt.rc('font', **font)
plt.figure()

for i, mask_quantity in zip(indexes, mask_quantities):
	history_epochs, history_data = histories[i][0], histories[i][1]
	label = str(mask_quantity) + ' masks'
	plt.semilogy(history_epochs, history_data, forms[i], label = label)

plt.ylabel('Log(MSE)')
plt.xlabel('Epochs')

plt.legend()
plt.tight_layout()
plt.grid(True)
plt.savefig('plots/ResultNNConvergenceHistoryPerGroup.pdf', dpi=200)