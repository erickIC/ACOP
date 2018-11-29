
package br.upe.optimizationUtil;

import br.upe.base.ACOPHeuristic;
import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.AmplifierVOA;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalChannel;
import br.upe.base.OpticalSignal;
import br.upe.heuristics.maxGain.MaxGain;
import br.upe.heuristics.uiara.AdGC;
import br.upe.initializations.BruteForceInitialization;
import br.upe.initializations.UniformInitializationVOA;
import br.upe.metrics.GNLIMetric;
import br.upe.objfunctions.linerInterpolation.LinearInterpolationFunction;
import br.upe.selection.MaxGainSelection;
import br.upe.selection.UiaraWeightSelection;
import br.upe.signal.factory.PowerMaskSignal;
import br.upe.simulations.simsetups.SimSetAMPVOA;
import br.upe.simulations.simsetups.SimulationSetup;
import br.upe.util.DecibelConverter;

public class ACOP_MOOProblem {

    private Amplifier[] amplifiers;
    private AmplifierType type;
    private int numAmps;
    private ACOP_LOCAL_PROBLEM localProblem;

    public ACOP_MOOProblem(AmplifierType type, int numberOfAmplifiers) {
	this.type = type;
	this.numAmps = numberOfAmplifiers;
	this.localProblem = ACOP_LOCAL_PROBLEM.AdGC;
    }

    public ACOP_MOOProblem(AmplifierType type, int numberOfAmplifiers, ACOP_LOCAL_PROBLEM localProblem) {
	this.type = type;
	this.numAmps = numberOfAmplifiers;
	this.localProblem = localProblem;
    }

    public double[] evaluate(float[] attenuations) {
	return evaluate(null, attenuations);
    }

    public double[] evaluate(float[] gains, float[] attenuations) {

	// NormalizationUtility nu =
	// NormalizationUtilityFactory.getInstance().fabricate(type);
	ObjectiveFunction function = new LinearInterpolationFunction();

	int numberCh = 40;
	float inputPowerCh = -18f;
	float linkLosses = 18.0f;
	SimulationSetup simSet = new SimSetAMPVOA(numberCh, inputPowerCh, 9.0f, numAmps);
	double linkLength = linkLosses * 1000 / 0.2;

	PowerMaskSignal signal = new PowerMaskSignal(numberCh, type, simSet.getCHANNEL_POWER(), 40);
	OpticalSignal inputSignal = signal.createSignal();

	float totalInputPower = inputSignal.getTotalPower();

	Amplifier[] amplifiers;
	float voaAttenuation;
	if(gains == null) {
	    ACOPHeuristic heuristic = null;

	    switch (localProblem) {
	    case MaxGain:
		heuristic = new MaxGain(numAmps, simSet.getLINK_LOSSES(), inputSignal, function);
		heuristic.setSelectionOp(new MaxGainSelection());
		break;
	    case AdGC:
		heuristic = new AdGC(numAmps, simSet.getLINK_LOSSES(), inputSignal, function);
		heuristic.setSelectionOp(new UiaraWeightSelection());
		break;
	    default:
		heuristic = new AdGC(numAmps, simSet.getLINK_LOSSES(), inputSignal, function);
	    }

	    heuristic.setInitialization(new UniformInitializationVOA(type, attenuations));
	    heuristic.setVoaMaxAttenuation(simSet.getVOA_MAX_ATT());
	    heuristic.setRoadmAttenuation(simSet.getROADM_ATT());
	    heuristic.setMaxOutputPower(simSet.getMaxOutputPower());
	    amplifiers = heuristic.execute();

	    if (amplifiers == null)
		return null;

	    voaAttenuation = ((AmplifierVOA) amplifiers[amplifiers.length - 1]).getVoaOutAttenuation();
	} else {

	    BruteForceInitialization initialization = new BruteForceInitialization(type, true,
		    simSet.getMaxOutputPower());
	    initialization.setGains(gains);
	    initialization.setAttenuations(attenuations);

	    amplifiers = initialization.initialize(simSet.getNumberOfAmplifiers(), totalInputPower, 0,
		    simSet.getLINK_LOSSES(), function, inputSignal);

	    if (amplifiers == null)
		return null;

	    float ampVoaAtt = ((AmplifierVOA) amplifiers[amplifiers.length - 1]).getVoaOutAttenuation();
	    voaAttenuation = (float) (amplifiers[amplifiers.length - 1].getOutputPower() - ampVoaAtt
		    - totalInputPower - simSet.getROADM_ATT());
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
			.getOutputPowerAfterVOA() <= (totalInputPower + simSet.getVOA_MAX_ATT() + simSet.getROADM_ATT())
		&& voaAttenuation >= 0) {

	    double[] result = new double[3];

	    GNLIMetric gnliMetric = new GNLIMetric(28e9, 100e9, numberCh, inputPowerCh, linkLength);
	    gnliMetric.evaluate(amplifiers);

	    // result[0] = calculateTilt(inputSignal); // minimizar

	    result[1] = (1 / gnliMetric.worstOSNR_NLI()); // maximizar

	    result[0] = gnliMetric.getTiltOSNR_NLI(); // minimizar

	    this.amplifiers = amplifiers;

	    return result;
	} else {
	    return null;
	}
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
