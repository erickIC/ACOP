package br.upe.base;

import br.upe.initializations.InitializationStrategy;
import br.upe.mascara.PowerMask;
import br.upe.mascara.PowerMaskFactory;
import br.upe.metrics.Metric;
import br.upe.selection.SelectionOperator;
import br.upe.signal.tracker.AmplifierSignalMonitor;
import br.upe.util.DecibelConverter;

public abstract class ACOPHeuristic {
    // Attributes of the problem
    protected float linkInputPower;
    protected float linkOutputPower;
    protected int numberOfAmplifiers;
    protected Amplifier[] amplifiers;
    protected float[] linkLosses;
    protected float voaMaxAttenuation;
    protected float roadmAttenuation;
    protected float maxOutputPower;
    protected AmplifierSignalMonitor[] monitors;
    protected double[][] voaLosses;

    // Attributes of the solution
    protected ObjectiveFunction function;
    protected SelectionOperator selectionOp;
    protected Metric metricCalculator;
    protected InitializationStrategy initialization;


    public ACOPHeuristic(int numberOfAmplifiers, float[] linkLosses, OpticalSignal inputSignal,
	    ObjectiveFunction function) {
	this.numberOfAmplifiers = numberOfAmplifiers;
	this.linkInputPower = inputSignal.getTotalPower();
	this.linkOutputPower = linkInputPower;
	this.linkLosses = linkLosses;
	this.function = function;
	this.monitors = new AmplifierSignalMonitor[numberOfAmplifiers];
    }

    /**
     * Executes the heuristic
     * 
     * @return The set of amplifier generated
     */
    public abstract Amplifier[] execute();

    /**
     * Define the losses using a constant value for all links.
     * 
     * @param constantLoss
     *            The value of the link's loss in dB
     */
    public void defineLosses(float constantLoss) {
	for (int i = 0; i < linkLosses.length; i++) {
	    linkLosses[i] = constantLoss;
	}
    }

    /**
     * @return the selectionOp
     */
    public SelectionOperator getSelectionOp() {
	return selectionOp;
    }

    /**
     * @param selectionOp
     *            the selectionOp to set
     */
    public void setSelectionOp(SelectionOperator selectionOp) {
	this.selectionOp = selectionOp;
    }


    /**
     * @return the function
     */
    public ObjectiveFunction getFunction() {
	return function;
    }

    /**
     * @param function
     *            the function to set
     */
    public void setFunction(ObjectiveFunction function) {
	this.function = function;
    }

    /**
     * @return the initialization
     */
    public InitializationStrategy getInitialization() {
	return initialization;
    }

    /**
     * @param initialization
     *            the initialization to set
     */
    public void setInitialization(InitializationStrategy initialization) {
	this.initialization = initialization;
    }


    /**
     * @param voaMaxAttenuation
     *            the voaMaxAttenuation to set
     */
    public void setVoaMaxAttenuation(float voaMaxAttenuation) {
	this.voaMaxAttenuation = voaMaxAttenuation;
    }

    /**
     * @return the voaMaxAttenuation
     */
    public float getVoaMaxAttenuation() {
	return voaMaxAttenuation;
    }

    /**
     * @return the roadmAttenuation
     */
    public float getRoadmAttenuation() {
	return roadmAttenuation;
    }

    /**
     * @param roadmAttenuation
     *            the roadmAttenuation to set
     */
    public void setRoadmAttenuation(float roadmAttenuation) {
	this.roadmAttenuation = roadmAttenuation;
    }

    public Amplifier[] getAmplifiers() {
	return amplifiers;
    }

    public void setAmplifiers(Amplifier[] amplifiers) {
	this.amplifiers = amplifiers;
    }

    /**
     * @return the maximum total output power that each amplifier can reach.
     */
    public float getMaxOutputPower() {
	return maxOutputPower;
    }

    /**
     * Set the maximum total output power that each amplifier can reach.
     * 
     * @param maxOutputPower
     */
    public void setMaxOutputPower(float maxOutputPower) {
	this.maxOutputPower = maxOutputPower;
    }

    public Metric getMetricCalculator() {
	return metricCalculator;
    }

    public void setMetricCalculator(Metric metricCalculator) {
	this.metricCalculator = metricCalculator;
    }

    public AmplifierSignalMonitor[] getMonitors() {
	return monitors;
    }

    public double[][] getVoaLosses() {
	return voaLosses;
    }

    /**
     * Define the losses in each VOA of the cascade for each channel considered
     * 
     * @param voaLosses
     *            [#span][#channels]
     */
    public void setVoaLosses(double[][] voaLosses) {
	this.voaLosses = voaLosses;
    }

    /**
     * Define the losses in each VOA of the cascade. The same loss is applied
     * for all the channels
     * 
     * @param voaLosses[#spans]:
     *            The losses, for each span, that will be applied in all
     *            channels
     */
    public void setVoaLosses(double[] voaLosses) {
	this.voaLosses = new double[voaLosses.length][1];
	for (int i = 0; i < voaLosses.length; i++) {
	    this.voaLosses[i][0] = voaLosses[i];
	}
    }

    protected OpticalSignal linkTrasferFunction(OpticalSignal signal, float linkLoss) {
	OpticalSignal result = signal.clone();
	for (OpticalChannel c : result.getChannels()) {
	    // Signal Total Gain
	    double signalLin = DecibelConverter.toLinearScale(c.getSignalPower());
	    signalLin *= DecibelConverter.toLinearScale(-1 * linkLoss);
	    // Noise Gain
	    double noiseLin = DecibelConverter.toLinearScale(c.getNoisePower());
	    noiseLin *= DecibelConverter.toLinearScale(-1 * linkLoss);

	    c.setSignalPower(DecibelConverter.toDecibelScale(signalLin));
	    c.setNoisePower(DecibelConverter.toDecibelScale(noiseLin));
	}

	return result;
    }

    public double calculateOSNR(OpticalSignal signal) {
	double minOSNR = Double.MAX_VALUE;
	for (OpticalChannel c : signal.getChannels()) {
	    double signalLin = DecibelConverter.toLinearScale(c.getSignalPower());
	    double noiseLin = DecibelConverter.toLinearScale(c.getNoisePower());
	    double OSNR = signalLin / noiseLin;

	    if (OSNR < minOSNR) {
		minOSNR = OSNR;
	    }
	}

	return DecibelConverter.toDecibelScale(minOSNR);
    }

    public double calculateTilt(OpticalSignal signal) {
	double maxPeak = Double.MIN_VALUE;
	double minPeak = Double.MAX_VALUE;

	for (OpticalChannel c : signal.getChannels()) {
	    double signalLin = DecibelConverter.toLinearScale(c.getSignalPower());

	    if (signalLin > maxPeak) {
		maxPeak = signalLin;
	    }
	    if (signalLin < minPeak) {
		minPeak = signalLin;
	    }
	}

	return DecibelConverter.toDecibelScale(maxPeak / minPeak);
    }

    protected void updateNextAmplifier(int currentIndex) {
	// updating the input power of the next amplifier
	OpticalSignal result = linkTrasferFunction(monitors[currentIndex].getOutputSignal(),
		linkLosses[currentIndex]);
	// apply the voaLosses
	if (voaLosses != null && currentIndex <= voaLosses.length)
	    result = applyVoaLosses(voaLosses[currentIndex], result);

	amplifiers[currentIndex + 1].setInputPower(result.getTotalPower());
	// Save the input power of this amplifier
	monitors[currentIndex + 1] = new AmplifierSignalMonitor();
	monitors[currentIndex + 1].setInputSignal(result);
    }

    private OpticalSignal applyVoaLosses(double[] voaLossPerChannel, OpticalSignal inputSignal) {
	OpticalSignal result = inputSignal.clone();
	
	int index = 0;
	for (OpticalChannel c : result.getChannels()) {
	    double voaLoss = 0.0;
	    
	    // If all the channels suffer the same loss
	    if (voaLossPerChannel.length == 1)
		voaLoss = voaLossPerChannel[0];
	    else
		voaLoss = voaLossPerChannel[index++];

	    double newSignalPower = c.getSignalPower() - voaLoss;
	    double newNoisePower = c.getNoisePower() - voaLoss;

	    c.setNoisePower(newNoisePower);
	    c.setSignalPower(newSignalPower);
	}

	return result;
    }

    protected void setGain(Amplifier amplifier, float gain) {
	PowerMask pm = PowerMaskFactory.getInstance().fabricatePowerMask(amplifier.getType());
	int maxGain = pm.getMaxGain();
	int minGain = pm.getMinGain();

	int intGain = (int) gain;
	
	if (intGain < minGain)
	    intGain = minGain;
	else if (intGain > maxGain)
	    intGain = maxGain;
	
	float maxInputPower = pm.getMaxTotalInputPower(intGain);

	while (amplifier.getInputPower() > maxInputPower + 0.5) {
	    if (intGain <= minGain)
		break;
	    intGain -= 1f;
	    maxInputPower = pm.getMaxTotalInputPower(intGain);
	}

	
	float minInputPower = pm.getMinTotalInputPower(intGain);
	while (amplifier.getInputPower() < minInputPower - 0.5) {
	    if (intGain >= minGain)
		break;
	    intGain += 1f;
	    minInputPower = pm.getMinTotalInputPower(intGain);
	}

	amplifier.setGain(intGain);
	
    }

    public float getLinkInputPower() {
	return linkInputPower;
    }

    public void setLinkInputPower(float linkInputPower) {
	this.linkInputPower = linkInputPower;
    }

    public float[] getGains() {
	float[] gains = new float[amplifiers.length];
	for (int i = 0; i < amplifiers.length; i++) {
	    gains[i] = amplifiers[i].getGain();
	}

	return gains;
    }

    public float[] getVOAAttenuations() {
	float[] attenuations = new float[amplifiers.length];
	for (int i = 0; i < attenuations.length; i++) {
	    if (amplifiers[i] instanceof AmplifierVOA)
		attenuations[i] = ((AmplifierVOA) amplifiers[i]).getVoaOutAttenuation();
	    else
		attenuations[i] = 0;
	}

	return attenuations;
    }

}

