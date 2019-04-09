
package br.upe.optimizationUtil;

import java.util.ArrayList;

import br.upe.base.ACOPHeuristic;
import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.AmplifierVOA;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalChannel;
import br.upe.base.OpticalSignal;
import br.upe.base.SimulationParameters;
import br.upe.heuristics.maxGain.MaxGain;
import br.upe.heuristics.uiara.AdGC;
import br.upe.initializations.BruteForceInitialization;
import br.upe.initializations.UniformInitializationVOA;
import br.upe.metrics.GNLIMetric;
import br.upe.objfunctions.linerInterpolation.LinearInterpolationFunction;
import br.upe.selection.MaxGainSelection;
import br.upe.selection.UiaraWeightSelection;
import br.upe.signal.factory.PowerMaskSignal;
import br.upe.util.DecibelConverter;
import br.upe.util.LinearRegression;

public class ACOP_MOOProblem {

    private Amplifier[] amplifiers;
    private AmplifierType type;
    private int numAmps;
    private ACOP_LOCAL_PROBLEM localProblem;
    private SimulationParameters simParams;

    public ACOP_MOOProblem(AmplifierType type, int numberOfAmplifiers, SimulationParameters parameters) {
	this.type = type;
	this.numAmps = numberOfAmplifiers;
	this.localProblem = ACOP_LOCAL_PROBLEM.AdGC;
	this.simParams = parameters;
    }

    public ACOP_MOOProblem(AmplifierType type, int numberOfAmplifiers, SimulationParameters parameters,
	    ACOP_LOCAL_PROBLEM localProblem) {
	this.type = type;
	this.numAmps = numberOfAmplifiers;
	this.localProblem = localProblem;
	this.simParams = parameters;
    }

    public double[] evaluateJustAttenuations(float[] attenuations) {
	return evaluate(null, attenuations);
    }

    public double[] evaluateJustGains(float[] gains) {
	return evaluate(gains, null);
    }

    public double[] evaluate(float[] gains, float[] attenuations) {

	// NormalizationUtility nu =
	// NormalizationUtilityFactory.getInstance().fabricate(type);
	ObjectiveFunction function = new LinearInterpolationFunction();

	double linkLength = simParams.getLinkLosses() * 1000 / 0.2;

	PowerMaskSignal signal = new PowerMaskSignal(simParams.getNumberCh(), type,
		simParams.getSimSet().getCHANNEL_POWER(), 40);
	OpticalSignal inputSignal = signal.createSignal();

	float totalInputPower = inputSignal.getTotalPower();

	Amplifier[] amplifiers;
	float voaAttenuation;
	if(gains == null) {
	    ACOPHeuristic heuristic = null;

	    switch (localProblem) {
	    case MaxGain:
		heuristic = new MaxGain(numAmps, simParams.getSimSet().getLINK_LOSSES(), inputSignal, function);
		heuristic.setSelectionOp(new MaxGainSelection());
		break;
	    case AdGC:
		heuristic = new AdGC(numAmps, simParams.getSimSet().getLINK_LOSSES(), inputSignal, function);
		heuristic.setSelectionOp(new UiaraWeightSelection());
		break;
	    default:
		heuristic = new AdGC(numAmps, simParams.getSimSet().getLINK_LOSSES(), inputSignal, function);
	    }

	    heuristic.setInitialization(new UniformInitializationVOA(type, attenuations));
	    heuristic.setVoaMaxAttenuation(simParams.getSimSet().getVOA_MAX_ATT());
	    heuristic.setRoadmAttenuation(simParams.getSimSet().getROADM_ATT());
	    heuristic.setMaxOutputPower(simParams.getSimSet().getMaxOutputPower());
	    amplifiers = heuristic.execute();

	    if (amplifiers == null)
		return null;

	    voaAttenuation = ((AmplifierVOA) amplifiers[amplifiers.length - 1]).getVoaOutAttenuation();
	} else {

	    boolean hasVOA = true;
	    if (attenuations == null)
		hasVOA = false;

	    BruteForceInitialization initialization = new BruteForceInitialization(type, hasVOA,
		    simParams.getSimSet().getMaxOutputPower());
	    initialization.setGains(gains);
	    initialization.setAttenuations(attenuations);

	    amplifiers = initialization.initialize(simParams.getSimSet().getNumberOfAmplifiers(), totalInputPower, 0,
		    simParams.getSimSet().getLINK_LOSSES(), function, inputSignal);

	    if (amplifiers == null)
		return null;

	    float ampVoaAtt = ((AmplifierVOA) amplifiers[amplifiers.length - 1]).getVoaOutAttenuation();
	    voaAttenuation = (float) (amplifiers[amplifiers.length - 1].getOutputPower() - ampVoaAtt
		    - totalInputPower - simParams.getSimSet().getROADM_ATT());
	    ((AmplifierVOA) amplifiers[amplifiers.length - 1]).increaseVoaOutAttenuation(voaAttenuation);

	}

	// If the output power of the link is less than the
	// input power, then the solution isn't desirable.
	// And, if the output power is greater than the
	// input
	// power + voa max attenuation + roadm attenuation,
	// then
	// the solution is not desirable
	if (amplifiers[amplifiers.length - 1].getOutputPower() >= totalInputPower
		&& ((AmplifierVOA) amplifiers[amplifiers.length - 1])
			.getOutputPowerAfterVOA() <= (totalInputPower + simParams.getSimSet().getVOA_MAX_ATT()
				+ simParams.getSimSet().getROADM_ATT())
		&& voaAttenuation >= 0) {

	    double[] result = new double[3];

	    GNLIMetric gnliMetric = new GNLIMetric(28e9, 100e9, simParams.getNumberCh(), simParams.getInputPowerCh(),
		    linkLength);
	    gnliMetric.evaluate(amplifiers);

	    // result[0] = calculateTilt(inputSignal); // minimizar

	    // result[1] = (1 / gnliMetric.worstOSNR_NLI()); // maximizar

	    if (gnliMetric.worstOSNR_ASE() < 0)
		// TODO: verificar casos com OSNR menor do que zero
		System.out.println();

	    result[1] = (1 / gnliMetric.worstOSNR_ASE()); // maximizar

	    // result[0] = gnliMetric.getTiltOSNR_NLI(); // minimizar

	    result[0] = Math.abs(calculateTiltLinearReg(inputSignal)); // minimizar

	    this.amplifiers = amplifiers;

	    return result;
	} else {
	    return null;
	}
    }

    private static double calculateTiltLinearReg(OpticalSignal signal) {
	ArrayList<OpticalChannel> channels = signal.getChannels();
	double[] frequencies = new double[channels.size()];
	double[] power = new double[channels.size()];

	int indexMaxFreq = 0, indexMinFreq = 0;

	for (int i = 0; i < power.length; i++) {
	    frequencies[i] = channels.get(i).getFrequency();
	    power[i] = channels.get(i).getSignalPower();

	    if (frequencies[i] < frequencies[indexMinFreq])
		indexMinFreq = i;
	    else if (frequencies[i] > frequencies[indexMaxFreq])
		indexMaxFreq = i;
	}

	// normalizing frequencies
	double maxFreq = frequencies[indexMaxFreq];
	double minFreq = frequencies[indexMinFreq];
	for (int i = 0; i < frequencies.length; i++) {
	    frequencies[i] = (frequencies[i] - minFreq) / (maxFreq - minFreq);
	}

	LinearRegression lr = new LinearRegression(frequencies, power);

	return lr.Tilt();
    }

    private double calculateTilt(OpticalSignal signal) {
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

    public Amplifier[] getAmplifiers() {
	return amplifiers;
    }

}
