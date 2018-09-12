package br.upe.objfunctions.linerInterpolation;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Set;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.AmplifierVOA;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalChannel;
import br.upe.base.OpticalSignal;
import br.upe.mascara.OperatingPoint;
import br.upe.mascara.PowerMask;
import br.upe.mascara.PowerMaskFactory;
import br.upe.signal.factory.ITUGridUniformSignal;
import br.upe.util.DecibelConverter;

public class LinearInterpolationFunction extends ObjectiveFunction {

    @Override
    public Amplifier[] getAmplifiersCandidate(Amplifier amplifier, OpticalSignal signal, boolean useInput) {
	// Get the power mask for this amplifier
	PowerMask pm = PowerMaskFactory.getInstance().fabricatePowerMask(amplifier.getType());
	float reference;
	if (useInput)
	    reference = amplifier.getInputPower();
	else
	    reference = amplifier.getGain();

	ArrayList<OperatingPoint> neighbors = new ArrayList<OperatingPoint>();
	ArrayList<OperatingPoint> ops = pm.getOperatingPoints();

	for (OperatingPoint op : ops) {
	    float maskValue;
	    if (useInput)
		maskValue = op.getTotalInputPower();
	    else
		maskValue = op.getGainSet();

	    if (Math.abs(reference - maskValue) < 0.5f) {
		neighbors.add(op);
	    }
	}

	Amplifier[] amplifiers = new Amplifier[neighbors.size()];
	for (int i = 0; i < amplifiers.length; i++) {
	    amplifiers[i] = new Amplifier(neighbors.get(i), amplifier.getType());
	    if (useInput)
		this.defineNewOperationPoint(amplifiers[i], signal);
	    else {
		double factor = amplifiers[i].getInputPower() - signal.getTotalPower();
		OpticalSignal temp = signal.adjustByFactor(factor);
		this.defineNewOperationPoint(amplifiers[i], temp);
	    }
	}

	return amplifiers;
    }

    @Override
    public void defineNewOperationPointWorstCase(Amplifier amplifier, OpticalSignal signal) {
	// Get the power mask for this amplifier
	PowerMask pm = PowerMaskFactory.getInstance().fabricateWorstCasePMwNLI(amplifier.getType());

	this.defineOpInternal(amplifier, signal, pm);
    }

    @Override
    public void defineNewOperationPoint(Amplifier amplifier, OpticalSignal signal) {
	// Get the power mask for this amplifier
	PowerMask pm = PowerMaskFactory.getInstance().fabricatePowerMask(amplifier.getType());

	this.defineOpInternal(amplifier, signal, pm);
    }

    private void defineOpInternal(Amplifier amplifier, OpticalSignal signal, PowerMask pm) {
	// Get the two operating points with the same gain set that surround the
	// total input power of the amplifier
	OperatingPoint[] neighbors = getNearestOperatingPoints(pm, amplifier.getInputPower(),
		(int) amplifier.getGain());

	// The total input power is out of mask.
	if (neighbors == null) {
	    amplifier = null;
	    return;
	}

	double[] outputPower = new double[signal.getChannels().size()];
	double[] noiseFigure = new double[signal.getChannels().size()];
	double totalOutputPower = 0, totalInputPower = 0;
	HashMap<Double, Float> gainPerChannel = new HashMap<Double, Float>();
	HashMap<Double, Float> nfPerChannel = new HashMap<Double, Float>();

	// For each channel
	for (int i = 0; i < outputPower.length; i++) {
	    OpticalChannel channel = signal.getChannels().get(i);
	    double signalLin = DecibelConverter.toLinearScale(channel.getSignalPower());

	    // Calculate gain
	    double gain = calculateGain(amplifier.getInputPower(), channel.getFrequency(), neighbors);
	    outputPower[i] = signalLin * gain;
	    gainPerChannel.put(channel.getFrequency(), (float) DecibelConverter.toDecibelScale(gain));

	    // Calculate noise figure
	    noiseFigure[i] = calculateNoiseFigure(amplifier.getInputPower(), channel.getFrequency(), neighbors);
	    nfPerChannel.put(channel.getFrequency(), (float) noiseFigure[i]);

	    totalInputPower += signalLin;
	    totalOutputPower += outputPower[i];
	}

	double totalGain = totalOutputPower / totalInputPower;

	// Gain Matching
	totalOutputPower = 0;
	double gainLin = DecibelConverter.toLinearScale(amplifier.getGain());
	double gainAdjust = (gainLin / totalGain);

	Set<Double> freqs = gainPerChannel.keySet();

	for(Double freq : freqs){
	    Float newG = (float) (DecibelConverter.toLinearScale(gainPerChannel.get(freq)) * gainAdjust);
	    gainPerChannel.put(freq, (float) DecibelConverter.toDecibelScale(newG));
	}
	
	for (int i = 0; i < outputPower.length; i++) {
	    outputPower[i] *= gainAdjust;
	    totalOutputPower += outputPower[i];
	}


	// Setting the features of the amplifier
	amplifier.setFlatness(calculateRipple(outputPower));

	if (amplifier.getFlatness() == 0) {
	    amplifier.setFlatness(calculateRipple(amplifier.getInputPower(), neighbors));
	}

	amplifier.setNoiseFigure(calculateNFMax(noiseFigure));
	amplifier.setOutputPower((float) DecibelConverter.toDecibelScale(totalOutputPower));
	amplifier.setGainPerChannel(gainPerChannel);
	amplifier.setNoiseFigurePerChannel(nfPerChannel);
    }

    private float calculateRipple(float inputPower, OperatingPoint[] neighbors) {
	double inputPowerLin = DecibelConverter.toLinearScale(inputPower);
	double inputPowerLinN0 = DecibelConverter.toLinearScale(neighbors[0].getTotalInputPower());
	double inputPowerLinN1 = DecibelConverter.toLinearScale(neighbors[1].getTotalInputPower());

	double factorX = 0;
	if (inputPowerLinN0 != inputPowerLinN1)
	    factorX = (inputPowerLin - inputPowerLinN0) / (inputPowerLinN1 - inputPowerLinN0);

	float ripple1 = neighbors[0].getLabRipple();
	float ripple2 = neighbors[1].getLabRipple();

	float ripple = (float) ((1 - factorX) * ripple1 + (factorX) * ripple2);

	return ripple;
    }

    /**
     * Function that find the two operating points of the power mask that
     * surround the input power
     * 
     * @param pm
     *            The power mask
     * @param inputPower
     *            The total input power used as reference
     * @param gain
     *            The gain set of the amplifier
     * @return The two operating points
     */
    private OperatingPoint[] getNearestOperatingPoints(PowerMask pm, float inputPower, int gain) {
	OperatingPoint[] neighbors = new OperatingPoint[2];
	ArrayList<OperatingPoint> ops = pm.getOperatingPoints();
	ArrayList<OperatingPoint> opsSameGain = new ArrayList<OperatingPoint>();

	if (gain < pm.getMinGain())
	    throw new RuntimeException(
		    "The gain " + gain + " is less than the minimum gain of the mask(" + pm.getMinGain() + " dB)");
	else if (gain > pm.getMaxGain())
	    throw new RuntimeException(
		    "The gain " + gain + " is greater than the maximum gain of the mask(" + pm.getMaxGain() + " dB)");

	for (OperatingPoint op : ops) {
	    if (op.getGainSet() == gain)
		opsSameGain.add(op);
	}

	Collections.sort(opsSameGain);
	float relax = 0.5f;

	for (int i = 0; i < opsSameGain.size(); i++) {
	    if (inputPower == opsSameGain.get(i).getTotalInputPower()) {
		neighbors[0] = neighbors[1] = opsSameGain.get(i);
		break;
	    } else if (inputPower < opsSameGain.get(i).getTotalInputPower()) {
		if (i == 0) {
		    if (Math.abs(inputPower - opsSameGain.get(i).getTotalInputPower()) > relax)
			return null; // throw new RuntimeException("Input power"
		    // + inputPower + " dB is out of the
		    // mask!");
		    else
			neighbors[0] = neighbors[1] = opsSameGain.get(i);

		    break;
		}

		neighbors[0] = opsSameGain.get(i - 1);
		neighbors[1] = opsSameGain.get(i);
		break;
	    } else if (i == opsSameGain.size() - 1) {
		if (Math.abs(inputPower - opsSameGain.get(i).getTotalInputPower()) > relax)
		    return null; // throw new RuntimeException("Input power " +
		// inputPower + " dB is out of the mask!");
		else
		    neighbors[0] = neighbors[1] = opsSameGain.get(i);
	    }
	}

	return neighbors;
    }

    /**
     * Estimate the gain of the channel using a linear interpolation
     * 
     * @param inputPower
     *            Amplifier total input power in dB
     * @param frequency
     *            The channel frequency in Hz
     * @param neighbors
     *            The two operating points near with total input power
     * @return Gain in mW
     */
    private double calculateGain(float inputPower, double frequency, OperatingPoint[] neighbors) {
	double inputPowerLin = DecibelConverter.toLinearScale(inputPower);
	double inputPowerLinN0 = DecibelConverter.toLinearScale(neighbors[0].getTotalInputPower());
	double inputPowerLinN1 = DecibelConverter.toLinearScale(neighbors[1].getTotalInputPower());

	double factorX = 0;
	if (inputPowerLinN0 != inputPowerLinN1)
	    factorX = (inputPowerLin - inputPowerLinN0) / (inputPowerLinN1 - inputPowerLinN0);

	double gainLinN0 = calculateChannelFeature(frequency, neighbors[0].getGainPerChannel());
	double gainLinN1 = calculateChannelFeature(frequency, neighbors[1].getGainPerChannel());

	double gain = (1 - factorX) * gainLinN0 + (factorX) * gainLinN1;
	return gain;
    }

    /**
     * Calculate the amplifiers noise figure using the nearest operating points
     * 
     * @param inputPower
     * @param neighbors
     * @return The noise figure in dB
     */
    private float calculateNoiseFigure(float inputPower, double frequency, OperatingPoint[] neighbors) {
	double inputPowerLin = DecibelConverter.toLinearScale(inputPower);
	double inputPowerLinN0 = DecibelConverter.toLinearScale(neighbors[0].getTotalInputPower());
	double inputPowerLinN1 = DecibelConverter.toLinearScale(neighbors[1].getTotalInputPower());

	double factorX = 0;
	if (inputPowerLinN0 != inputPowerLinN1)
	    factorX = (inputPowerLin - inputPowerLinN0) / (inputPowerLinN1 - inputPowerLinN0);

	double noiseFigureN0Lin = calculateChannelFeature(frequency, neighbors[0].getNoiseFigurePerChannel());
	double noiseFigureN1Lin = calculateChannelFeature(frequency, neighbors[1].getNoiseFigurePerChannel());

	double noiseFigure = (1 - factorX) * noiseFigureN0Lin + factorX * noiseFigureN1Lin;
	return (float) DecibelConverter.toDecibelScale(noiseFigure);
    }

    private int transformFrequency(double frequency) {
	return (int) (Math.round((frequency / 1e10)));
    }

    /**
     * Estimate the feature (gain or nf) for one channel
     * 
     * @param frequency
     *            Frequency of the channel in Hz
     * @param featurePerChannel
     *            Set of feature (Gain or NF) in dB of this operating point
     * @return Feature of the channel in mW
     */
    private double calculateChannelFeature(double frequency, HashMap<Double, Float> featurePerChannel) {
	if (featurePerChannel.containsKey(frequency)) {
	    return DecibelConverter.toLinearScale(featurePerChannel.get(frequency));
	}
	else {
	    Collection<Double> frequencys = featurePerChannel.keySet();
	    List<Double> freqList = new ArrayList<Double>(frequencys);
	    Collections.sort(freqList);

	    double freqMin = Double.MAX_VALUE, freqMax = Double.MAX_VALUE;

	    int frequencyTmp = transformFrequency(frequency);

	    for (int i = 0; i < freqList.size(); i++) {
		if (frequencyTmp == transformFrequency(freqList.get(i))) {
		    freqMin = freqMax = freqList.get(i);
		    break;
		} else if (frequency < freqList.get(i)) {
		    if (i == 0) {
			if (Math.abs(frequency - freqList.get(i)) > 50e9) // greater
			    // than
			    // 50GHz
			    throw new RuntimeException("Frequency " + frequency + " is out of the mask!");
			else
			    freqMin = freqMax = freqList.get(i);
			break;
		    }

		    freqMin = freqList.get(i - 1);
		    freqMax = freqList.get(i);
		    break;
		} else if (i == freqList.size() - 1) {
		    if (Math.abs(frequency - freqList.get(i)) > 50e9) // greater
			// than
			// 50GHz
			throw new RuntimeException("Frequency " + frequency + " is out of the mask!");
		    else
			freqMin = freqMax = freqList.get(i);
		}
	    }

	    double factorX = 0;
	    if (freqMin != freqMax)
		factorX = (frequency - freqMin) / (freqMax - freqMin);

	    double featureLinMin = DecibelConverter.toLinearScale(featurePerChannel.get(freqMin));
	    double featureLinMax = DecibelConverter.toLinearScale(featurePerChannel.get(freqMax));

	    return ((1 - factorX) * featureLinMin + factorX * featureLinMax);
	}
    }

    public static void main(String[] args) {
	float linkInputPower = DecibelConverter.calculateInputPower(39, -46.3f);

	ITUGridUniformSignal signal = new ITUGridUniformSignal(39, 1.9210e14, 100e9, -46.3f, 30);
	OpticalSignal inputSignal = signal.createSignal();

	int ganho = 30;
	Amplifier amplifier = new AmplifierVOA(linkInputPower, ganho, (linkInputPower + ganho), 0.0f, 0.0f, 0.0f,
		AmplifierType.EDFA_1_STG);

	// Amplifier[] amps = function.getAmplifiersCandidate(amplifier,
	// inputSignal);
	long t = System.currentTimeMillis();
	LinearInterpolationFunction function = new LinearInterpolationFunction();
	function.defineNewOperationPoint(amplifier, inputSignal);
	System.out.println(System.currentTimeMillis() - t);
    }

}
