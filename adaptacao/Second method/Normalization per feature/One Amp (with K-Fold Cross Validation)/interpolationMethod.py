import math
import numpy as np

# This is the function 'm' from the article
def getPoutInMask (frequency, Pin, Gset, tilt, PowerMask):
    # Find the channel that has the same frequency, Pin, Gset and tilt
    Frequencys = PowerMask[:40, 2]

    for i in range(0, len(Frequencys)):
        if Frequencys[i] == frequency:
            for j in range(i, len(PowerMask), 40):
                if PowerMask[j][0] == Pin and PowerMask[j][1] == Gset and PowerMask[j][3] == tilt:
                    return PowerMask[j][4]  # return the 'pout_ch' of this channel

# This is the function 's' from the article
def getPoutAnyFrequency (frequency, Pin, Gset, tilt, PowerMask):
    # Get each Frequency from PowerMask and find closest values to it (f_1 and f_2)
    Frequencys = PowerMask[:40, 2]
    closest_lower = np.min(Frequencys)
    closest_higher = np.max(Frequencys)

    for i in range(0, len(Frequencys)):
        if Frequencys[i] > frequency and Frequencys[i] < closest_higher and Frequencys[i] != closest_lower:
            closest_higher = Frequencys[i]
        if Frequencys[i] < frequency and Frequencys[i] > closest_lower and Frequencys[i] != closest_higher:
            closest_lower = Frequencys[i]
    
    f_1 = closest_lower
    f_2 = closest_higher
    
    # # Get Gset from PowerMask with the same Pin
    # Pins = PowerMask[::40, 0]
    
    # for i in range(0, len(Pins)):
    #     if Pins[i] == Pin:
    #         Gset = PowerMask[(i*40)][1]

    factorX = (frequency - f_1) / (f_2 - f_1)
    return (1-factorX)*getPoutInMask(f_1,Pin,Gset,tilt,PowerMask) + factorX*getPoutInMask(f_2,Pin,Gset,tilt,PowerMask)

# This is the function 'g' from the article
def getPoutAnyPin (frequency, Pin, Gset, tilt, PowerMask):
    # Get each Pin from PowerMask and find closest values to it (Pin_1 and Pin_2)
    Pins = PowerMask[::40, 0]
    closest_lower = np.min(Pins)
    closest_higher = np.max(Pins)

    for i in range(0, len(Pins)):
        if Pins[i] > Pin and Pins[i] < closest_higher and Pins[i] != closest_lower:
            closest_higher = Pins[i]
        if Pins[i] < Pin and Pins[i] > closest_lower and Pins[i] != closest_higher:
            closest_lower = Pins[i]
    
    Pin_1 = closest_lower
    Pin_2 = closest_higher

    factorX = (Pin - Pin_1) / (Pin_2 - Pin_1)
    return (1-factorX)*getPoutAnyFrequency(frequency,Pin_1,Gset,tilt,PowerMask) + factorX*getPoutAnyFrequency(frequency,Pin_2,Gset,tilt,PowerMask)

# This function is the adaptation of this method to consider the tilt
# Proposed by us
def getPoutAnyTilt (frequency, Pin, Gset, tilt, PowerMask):
    # Get each tilt from PowerMask and find closest values to it (tilt_1 and tilt_2)
    tilts = PowerMask[::40, 3]
    closest_lower = np.min(tilts)
    closest_higher = np.max(tilts)

    for i in range(0, len(tilts)):
        if tilts[i] > tilt and tilts[i] < closest_higher and tilts[i] != closest_lower:
            closest_higher = tilts[i]
        if tilts[i] < tilt and tilts[i] > closest_lower and tilts[i] != closest_higher:
            closest_lower = tilts[i]
    
    tilt_1 = closest_lower
    tilt_2 = closest_higher

    factorX = (tilt - tilt_1) / (tilt_2 - tilt_1)
    return (1-factorX)*getPoutAnyPin(frequency,Pin,Gset,tilt_1,PowerMask) + factorX*getPoutAnyPin(frequency,Pin,Gset,tilt_2,PowerMask)

#TODO: Maybe we could implement a function that finds the closest values for any parameter (tilt,Pin,frequency). 
# The code would be more reusable

def getOutputSpectrum (frequencys, Pin, Gset, tilt, PowerMask):
    ### No need to calculate Pin_total because it's already in the PowerMask
    # dB_to_mW = lambda x : pow(10, x/10)
    
    # #Calculates Pin (total input power) using 'TIP algorithm'
    # pins_mW = list(map(dB_to_mW,pins))
    # Pin_mW = sum(pins_mW)
    # Pin = 10*math.log10(Pin_mW) #mW to dB

    # print('Wave: ', frequencys)
    # print('Pin: ', Pin)
    # print('Gset: ', Gset)
    # print('Tilt: ', tilt)
    # print(PowerMask[0])
    # return

    # Calculates pout for each channel
    pouts = []
    for frequency in frequencys:
        pouts.append(getPoutAnyTilt(frequency,Pin,Gset,tilt,PowerMask))
    
    # Apply gain matching algorithm
    return applyGainMatching(Pin, Gset, pouts)

def applyGainMatching(Pin, Gset, pouts):
    dB_to_mW = lambda x : pow(10, x/10)
    mW_to_dB = lambda x : 10*math.log10(x)

    ### No need to calculate Pin_total because it's already in the PowerMask
    # pins_mW = list(map(dB_to_mW,pins))
    # Pin_mW = sum(pins_mW)

    # Convert Pin and Gset from dB to mW:
    Pin_mW = pow(10, Pin/10)
    Gset_mW = pow(10, Gset/10)

    pouts_mW = list(map(dB_to_mW,pouts))
    Pout_mW = sum(pouts_mW)
    
    adj_factor = (Pout_mW / Pin_mW) / Gset_mW # Total Gain / Gain desired
    gain_matching = lambda x : x*adj_factor
    pouts_mW = list(map(gain_matching,pouts_mW))
    pouts = list(map(mW_to_dB,pouts_mW))
    
    return pouts

# Main
input_fold_1 = "masks/mask-edfa1-padtec-icton17-fold-1.txt"
input_fold_2 = "masks/mask-edfa1-padtec-icton17-fold-2.txt"
input_fold_3 = "masks/mask-edfa1-padtec-icton17-fold-3.txt"
input_fold_4 = "masks/mask-edfa1-padtec-icton17-fold-4.txt"
input_fold_5 = "masks/mask-edfa1-padtec-icton17-fold-5.txt"
info_file = "masks/mask-edfa1-padtec-icton17-info"

# Splitting data into training and test groups
training_group_1 = [input_fold_2, input_fold_3, input_fold_4, input_fold_5]
test_group_1 = [input_fold_1]

training_group_2 = [input_fold_1, input_fold_3, input_fold_4, input_fold_5]
test_group_2 = [input_fold_2]

training_group_3 = [input_fold_1, input_fold_2, input_fold_4, input_fold_5]
test_group_3 = [input_fold_3]

training_group_4 = [input_fold_1, input_fold_2, input_fold_3, input_fold_5]
test_group_4 = [input_fold_4]

training_group_5 = [input_fold_1, input_fold_2, input_fold_3, input_fold_4]
test_group_5 = [input_fold_5]

training_groups = [training_group_1, training_group_2, training_group_3, training_group_4, training_group_5]
test_groups = [test_group_1, test_group_2, test_group_3, test_group_4, test_group_5]

# Reading groups and estimating P_out using k-Fold Cross Validation (k = 5)
for training_group, test_group in zip(training_groups, test_groups):
    training_data = []
    test_data = []

    for training_fold in training_group:
        with open(training_fold, 'r') as f_in:
            lines = f_in.readlines()
            for i in range(0, len(lines)):
                aux = lines[i].split()
                for j in range(0, len(aux)):
                    aux[j] = float(aux[j])
                training_data.append(aux)
    training_data = np.array(training_data)

    for test_fold in test_group:
        with open(test_fold, 'r') as f_in:
            lines = f_in.readlines()
            for i in range(0, len(lines)):
                aux = lines[i].split()
                for j in range(0, len(aux)):
                    aux[j] = float(aux[j])
                test_data.append(aux)
    test_data = np.array(test_data)

    # print('Training data:')
    # print(training_data)
    # print('Test data:')
    # print(test_data)

    # Loop to get each input signal from test data mask
    for i in range(0, len(test_data), 40):
        pin_total = test_data[i][0]
        # print('Pin: ', pin_total)
        gset = test_data[i][1]
        # print('Gset: ', gset)
        wavelengths = test_data[i:(i+40), 2]    # using wavelength instead of frequency because it's already in the mask
        # print('Wave: ', wavelengths)
        tilt = test_data[i][3]
        # print('Tilt: ', tilt)
        pouts = getOutputSpectrum(wavelengths, pin_total, gset, tilt, training_data)
        print(pouts)
        break
    break