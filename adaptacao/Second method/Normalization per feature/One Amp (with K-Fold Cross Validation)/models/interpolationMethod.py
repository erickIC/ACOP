import math

# This is the function 'm' from the article
def getPoutInMask (frequency, Pin, Gset, tilt, PowerMask):
    # TODO: Find in PowerMask the channel that has the same 'frequency' in the line that has the same 'Pin', 'Gset' and 'tilt'
    # Return the 'pout_ch' of this channel
    return pout

# This is the function 's' from the article
def getPoutAnyFrequency (frequency, Pin, Gset, tilt, PowerMask):
    # TODO: Find the two closest values to 'frequency' in the PowerMask line that has the same 'Pin' and 'Gset'  (f_1 and f_2)
    factorX = (frequency - f_1) / (f_2 - f_1)

    return (1-factorX)*getPoutInMask(f_1,Pin,Gset,tilt,PowerMask) + factorX*getPoutInMask(f_2,Pin,tilt,PowerMask)


# This is the function 'g' from the article
def getPoutAnyPin (frequency, Pin, Gset, tilt, PowerMask):
    # TODO: Find the two closest values to 'Pin' in the PowerMask (Pin_1 and Pin_2)
    factorX = (Pin - Pin_1) / (Pin_2 - Pin_1)

    return (1-factorX)*getPoutAnyFrequency(frequency,Pin_1,Gset, tilt, PowerMask) + factorX*getPoutAnyFrequency(frequency,Pin_2, tilt, PowerMask)

# This function is the adaptation of this method to consider the tilt
# Proposed by us
def getPoutAnyTilt (frequency, Pin, Gset, PowerMask, tilt):
    # TODO: Find the two closest values to 'tilt' in the PowerMask (tilt_1 and tilt_2)
    factorX = (tilt - tilt_1) / (tilt_2 - tilt_1)

    return (1-factorX)*getPoutAnyPin(frequency,Pin,Gset,tilt_1,PowerMask) + factorX*getPoutAnyFrequency(frequency,Pin,tilt_2,PowerMask)

#TODO: Maybe we could implement a function that finds the closest values for any parameter (tilt,Pin,frequency). 
# The code would be more reusable

def getOutputSpectrum (frequencys, pins, Gset, tilt, PowerMask):
    dB_to_mW = lambda x : pow(10, x/10)
    mW_to_dB = lambda x : 10*math.log10(x)
    
    #Calculates Pin (total input power) using 'TIP algorithm'
    pins_mW = list(map(dB_to_mW,pins))
    Pin_mW = sum(pins_mW)
    Pin = 10*math.log10(Pin_mW) #mW to dB

    pouts = []
    for frequency in frequencys:
        pouts.append(getPoutAnyPin(frequency,Pin,Gset,tilt,PowerMask))
    
    #Apply gain matching algorithm
    pouts_mW = list(map(dB_to_mW,pouts))
    Pout_mW = sum(pouts_mW)
    adj_factor = (Pout_mW / Pin_mW) / Gset # Total Gain / Gain desired
    gain_matching = lambda x : x*adj_factor
    pouts_mW = list(map(gain_matching,pouts_mW))
    pouts = list(map(mW_to_dB,pouts_mW))

    return pouts
