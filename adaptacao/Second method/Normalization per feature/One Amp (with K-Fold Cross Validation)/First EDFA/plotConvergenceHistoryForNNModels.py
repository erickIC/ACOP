'''
	This script loads the NN convergence history objects for each tilt step and plot the data
	on a single figure.
'''

import pickle
import matplotlib.pyplot as plt
import numpy as np

dB_steps = [2, 4, 7, 14]
histories = []

# Loading each step convergence history
for step in dB_steps:
	input_object = 'models/nn-history-for-' + str(step) + 'dB-step.obj'
	with open(input_object, 'rb') as history_obj:
		histories.append(pickle.load(history_obj))

# Plotting convergence curve for each step on a single figure
forms = ['--', '-^', '-*', '-s']
indexes = np.arange(0, len(histories))

plt.figure()

for i, step in zip(indexes, dB_steps):
	history_epochs, history_data = histories[i][0], histories[i][1]
	label = str(step) + 'dB'
	plt.semilogy(history_epochs, history_data, forms[i], label = label)

plt.ylabel('Log(MSE)')
plt.xlabel('Epochs')

plt.legend()
plt.tight_layout()
plt.savefig('plots/ResultNNConvergenceHistoryPerStep.pdf', dpi=200)