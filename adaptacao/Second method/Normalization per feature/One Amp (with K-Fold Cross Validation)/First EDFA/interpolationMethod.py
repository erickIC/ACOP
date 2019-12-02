import math
import numpy as np
from collections import defaultdict

number_of_channels = 40
max_tilt = 14
min_tilt = -14

'''
	This is the function 'm' from the article.
	This method search in the signal chosen from the PowerMask for the output power
	of the respective channel.
'''
def getPoutInMask (Gset, Pin, Frequency, PowerMask):
	# Return output power value of the asked channel
	P_outs = PowerMask[42:42+number_of_channels]
	return P_outs[Frequency]

'''
	This is the function 's' from the article.
	This method search for frequency values in the PowerMask near the frequency of the channel
	from which we want the output power.
'''
def getPoutAnyFrequency (Gset, Pin, Frequency, PowerMask):
	# Since all signals are in the same frequency range, we can use channel value
	return getPoutInMask(Gset, Pin, Frequency, PowerMask)

'''
	This is the function 'g' from the article.
	This method search for total input power values in the PowerMask equal to the value estimated
	for the input signal, with the same gain value. If they exist, use the for intepolation;
	otherwise, it looks for total input power values near the estimated.
'''
def getPoutAnyPin (Gset, Pin, Frequency, PowerMask):
	# Calculates Pin for each signal in Power Mask
	closest_lower = float('-inf')
	signal_1 = None
	closest_higher = float('inf')
	signal_2 = None

	for signal in PowerMask:
		Pins = signal[1:1+number_of_channels]
		dB_to_mW = lambda x : pow(10, x/10)
		pins_mW = list(map(dB_to_mW,Pins))
		Pin_mW = sum(pins_mW)
		Pin_signal = 10*math.log10(Pin_mW)

		Gset_signal = signal[0]

		# If estimated Pin exists in the Power Mask, use it
		if Pin_signal == Pin and Gset_signal == Gset:
			return getPoutAnyFrequency(Gset, Pin_signal, Frequency, signal)
		# Otherwise, search for closest higher and closest lower Pin values
		else:
			if Pin_signal > closest_lower and Pin_signal < Pin:
				closest_lower = Pin_signal
				signal_1 = signal
				continue
			if Pin_signal < closest_higher and Pin_signal > Pin:
				closest_higher = Pin_signal
				signal_2 = signal
				
	# Check which of the masks are used and return predicted P_out
	if signal_1 is not None:
		if signal_2 is not None:
			# If both tilts (higher and lower) exists, calculate factorX and return result
			factorX = (Pin - closest_lower) / (closest_higher - closest_lower)
			return ((1 - factorX) * getPoutAnyFrequency(Gset, closest_lower, Frequency, signal_1) + factorX * getPoutAnyFrequency(Gset, closest_higher, Frequency, signal_2))
		else:
			# If only closest lower exists, return its prediction
			return getPoutAnyFrequency(Gset, closest_lower, Frequency, signal_1)
	else:
		# If only closest higher exists, return its prediction
		return getPoutAnyFrequency(Gset, closest_higher, Frequency, signal_2)

'''
	This method calculates the total input power of the input signal and call a method
	to estimate the output power for each frequency channel.
'''
def getOutputSpectrum (Gset, Pins, Frequencies, PowerMask):
	# Calculates Pin (total input power) using 'TIP algorithm'
	dB_to_mW = lambda x : pow(10, x/10)
	pins_mW = list(map(dB_to_mW,Pins))
	Pin_mW = sum(pins_mW)
	Pin = 10*math.log10(Pin_mW)

	# Estimates Pout for each channel (frequency)
	p_outs = []
	for frequency in Frequencies:
		Channel = Frequencies.index(frequency)
		p_outs.append(getPoutAnyPin(Gset, Pin, Channel, PowerMask))

	# Apply Gain Matching Algorithm and return Pout for each channel of the input signal
	# p_outs = applyGainMatching(Gset, Pin, p_outs)
	
	return p_outs

'''
	This method apply the Gain Matching Algorthm to correct the estimated gain computed
	by the technique.
'''
def applyGainMatching(Gset, Pin, Pouts):
	dB_to_mW = lambda x : pow(10, x/10)
	mW_to_dB = lambda x : 10*math.log10(x)

	# Convert Pin (total input power) and Gset from dB to mW
	Pin_mW = pow(10, Pin/10)
	Gset_mW = pow(10, Gset/10)

	# Convert Pout of each channel from dB to mW and calculate Pout (total output power)
	pouts_mW = list(map(dB_to_mW, Pouts))
	Pout_mW = sum(pouts_mW)

	# Execute Gain Matching
	adj_factor = (Pout_mW / Pin_mW) / Gset_mW
	gain_matching = lambda x : x * adj_factor
	pouts_mW = list(map(gain_matching, pouts_mW))

	# Convert Pout of each channel from mW to dB
	p_outs = list(map(mW_to_dB, pouts_mW))

	# Return corrected Pout values
	return p_outs

'''
	This method estimates the tilt of the input signal and checks for signals with this tilt in the PowerMask.
	If they exist, use them for interpolation; otherwise, it looks for tilt values near the estimated.
'''
def estimateOutputWithInterpolation(Gset, Pins, Frequencies, PowerMasks):
	# Estimating tilt value of input signal
	tilt = int(round(Pins[0] - Pins[number_of_channels-1]))

	p_outs_1 = None
	p_outs_2 = None

	# If estimated tilt exists in the Power Mask, use it
	if tilt in PowerMasks:
		p_outs_1 = getOutputSpectrum(Gset, Pins, Frequencies, PowerMasks[tilt])
		return p_outs_1
	# Otherwise, search for closest higher and closest lower tilt values
	else:
		for closest_lower in range(tilt-1, min_tilt-1, -1):
			if closest_lower in PowerMasks:
				p_outs_1 = getOutputSpectrum(Gset, Pins, Frequencies, PowerMasks[closest_lower])
				break
		for closest_higher in range(tilt+1, max_tilt+1):
			if closest_higher in PowerMasks:
				p_outs_2 = getOutputSpectrum(Gset, Pins, Frequencies, PowerMasks[closest_higher])
				break
	
	# Check which of the masks are used and return predicted P_out
	if p_outs_1 is not None:
		if p_outs_2 is not None:
			# If both tilts (higher and lower) exists, calculate factorX and return result
			factorX = (tilt - closest_lower) / (closest_higher - closest_lower)
			p_outs_1 = [p_out_ch * (1-factorX) for p_out_ch in p_outs_1]
			p_outs_2 = [p_out_ch * factorX for p_out_ch in p_outs_2]
			return p_outs_1 + p_outs_2
		else:
			# If only closest lower exists, return its prediction
			return p_outs_1
	else:
		# If only closest higher exists, return its prediction
		return p_outs_2

'''
	Main
'''
def interpolationMethod(training_data, test_data):
	# Defining wavelength for range of operation
	wavelengths = [1560.713, 1559.794, 1559.04, 1558.187, 1557.433, 1556.613, 1555.858, 1555.038, 1554.153, 1553.398,	
					1552.578, 1551.758, 1550.971, 1550.02, 1549.397, 1548.61, 1547.822, 1547.002, 1546.182, 1545.395, 
					1544.608, 1543.788, 1543.001, 1542.214, 1541.426, 1540.639, 1539.852, 1538.966, 1538.278, 1537.425, 
					1536.638, 1535.883, 1535.096, 1534.342, 1533.587, 1532.8, 1532.013, 1531.226, 1530.438, 1529.651]

	# Creating tilt dictionary for better search
	tilt_dict = defaultdict(list)

	for signal in training_data:
		tilt = signal[41]
		tilt_dict[tilt].append(signal)
	
	# Estimating Output Power (p_out) for each input signal from 'test_data'
	p_out = []

	for signal in test_data:
		# Getting info from signal
		g_set = signal[0]
		p_in = signal[1:1+number_of_channels]

		# Applying method
		p_out.append(estimateOutputWithInterpolation(g_set, p_in, wavelengths, tilt_dict))
	
	# Returning P_out prediction
	return p_out