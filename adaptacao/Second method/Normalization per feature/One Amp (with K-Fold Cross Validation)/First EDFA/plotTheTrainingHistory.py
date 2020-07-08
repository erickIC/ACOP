import numpy as np
from numpy import median
import keras
import pickle
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras import callbacks
from keras.layers import Dropout
from random import randint 
from matplotlib.ticker import PercentFormatter


smaller_size = 14
medium_size = 20
bigger_size = 26
plt.rc('font', size=bigger_size)             # controls default text sizes
plt.rc('axes', titlesize=medium_size)        # fontsize of the axes title
plt.rc('axes', labelsize=medium_size)        # fontsize of the x and y labels
plt.rc('xtick', labelsize=medium_size)      # fontsize of the tick labels
plt.rc('ytick', labelsize=medium_size)      # fontsize of the tick labels
plt.rc('legend', fontsize=medium_size)       # legend fontsize
plt.rc('figure', titlesize=bigger_size)      # fontsize of the figure title

#Read the file.  
file = open('models/nn-41-to-40-history.obj', 'rb')

model_41to40 = pickle.load(file)

file = open('models/nn-42-to-40-history.obj', 'rb')

model_42to40 = pickle.load(file)

file = open('models/nn-icton-history.obj', 'rb')

model_icton = pickle.load(file)

file = open('models/nn-icton-o-history.obj', 'rb')

model_icton_o = pickle.load(file)

######## plot the histories #######

forms = ['--', '-^', '-*', '-s', '-']

plt.figure()

epochs = model_41to40[0]
histories = model_41to40[1]

for i in range(0, len(epochs)):
    labelstr = 'Fold' + ' ' + str(i + 1)
    plt.semilogy(epochs[i], histories[i], forms[i], label= labelstr)


plt.ylabel('log(MSE)')
plt.xlabel('EPOCHS')

plt.legend()
plt.tight_layout()
plt.grid(True)
plt.savefig('Treinamento41to40.pdf', dpi = 200)


plt.figure()

epochs = model_42to40[0]
histories = model_42to40[1]

for i in range(0, len(epochs)):
    labelstr = 'Fold' + ' ' + str(i + 1)
    plt.semilogy(epochs[i], histories[i], forms[i], label= labelstr)


plt.ylabel('log(MSE)')
plt.xlabel('EPOCHS')

plt.legend()
plt.tight_layout()
plt.grid(True)
plt.savefig('Treinamento42to40.pdf', dpi = 200)

plt.figure()

epochs = model_icton[0]
histories = model_icton[1]

for i in range(0, len(epochs)):
    labelstr = 'Fold' + ' ' + str(i + 1)
    plt.semilogy(epochs[i], histories[i], forms[i], label= labelstr)


plt.ylabel('log(MSE)')
plt.xlabel('EPOCHS')

plt.legend()
plt.tight_layout()
plt.grid(True)
plt.savefig('TreinamentoICTON.pdf', dpi = 200)

plt.figure()

epochs = model_icton_o[0]
histories = model_icton_o[1]

for i in range(0, len(epochs)):
    labelstr = 'Fold' + ' ' + str(i + 1)
    plt.semilogy(epochs[i], histories[i], forms[i], label= labelstr)


plt.ylabel('log(MSE)')
plt.xlabel('EPOCHS')

plt.legend()
plt.tight_layout()
plt.grid(True, which='major', axis='both')
plt.gca().yaxis.grid(True)
ax = plt.gca()
ax.grid(which='major', axis='both', linestyle='--')
plt.savefig('TreinamentoICTON-O.pdf', dpi = 200)