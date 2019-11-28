package br.upe.heuristics.lossComp;

import br.upe.base.ACOPHeuristic;
import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.AmplifierVOA;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalSignal;
import br.upe.initializations.UniformInitialization;
import br.upe.mascara.PowerMask;
import br.upe.mascara.PowerMaskFactory;
import br.upe.objfunctions.linerInterpolation.LinearInterpolationFunction;
import br.upe.signal.factory.PowerMaskSignal;
import br.upe.signal.tracker.AmplifierSignalMonitor;
import br.upe.simulations.simPadTec19.SimSetPadTec;
import br.upe.simulations.simsetups.SimulationSetup;
import br.upe.util.SignalFeatureCalculation;

public class LossComp extends ACOPHeuristic {	

    private float firstAmplifierTargerGain = 0.0f;

    public LossComp(int numberOfAmplifiers, float[] linkLosses, OpticalSignal inputSignal, ObjectiveFunction function) {
	super(numberOfAmplifiers, linkLosses, inputSignal, function);
	monitors[0] = new AmplifierSignalMonitor();
	monitors[0].setInputSignal(inputSignal);
    }

    public void setFirstAmplifierTargetGain(float gain) {
	firstAmplifierTargerGain = gain;
    }

    @Override
    public Amplifier[] execute() {
	this.amplifiers = initialization.initialize(numberOfAmplifiers, linkInputPower, linkOutputPower, linkLosses,
		function, monitors[0].getInputSignal());

	for (int i = 0; i < numberOfAmplifiers; i++) {
	    float targetGain = 0;
	    // First amplifier
	    // The gain is equal to the ROADM loss
	    if (i == 0 && firstAmplifierTargerGain == 0) {
		float channelPower = (float) monitors[0].getInputSignal().getChannels().get(0).getSignalPower();
		targetGain = -3.0f - channelPower; // getRoadmAttenuation();
		
		targetGain = applyRestriction(targetGain, amplifiers[0]);
	    }
	    // First amplifier, gain defined a priori
	    else if (i == 0) {
		targetGain = firstAmplifierTargerGain;
	    }
	    // Other amplifier
	    // The gain is equal to the previous loss
	    else {
		targetGain = linkLosses[i - 1];
	    }

	    float newOutputPower = amplifiers[i].getInputPower() + targetGain;

	    if (newOutputPower > maxOutputPower) {
		targetGain = newOutputPower - maxOutputPower;
	    }

	    // updating the output power of the current amplifier
	    amplifiers[i].setGain(Math.round(targetGain));
	    function.defineNewOperationPoint(amplifiers[i], monitors[i].getInputSignal());

	    // Last amplifier
	    if (i + 1 == numberOfAmplifiers) {
		if (amplifiers[i].getOutputPower() > linkOutputPower + voaMaxAttenuation + roadmAttenuation) {
		    int diff = Math.round(
			    amplifiers[i].getOutputPower() - (linkOutputPower + voaMaxAttenuation + roadmAttenuation));
		    amplifiers[i].setGain(amplifiers[i].getGain() - diff);
		    function.defineNewOperationPoint(amplifiers[i], monitors[i].getInputSignal());
		}

		float ampVoaAtt = ((AmplifierVOA) amplifiers[i]).getVoaOutAttenuation();
		float voaAttenuation = (float) (amplifiers[i].getOutputPower() - ampVoaAtt - linkInputPower
			- roadmAttenuation);
		((AmplifierVOA) amplifiers[i]).increaseVoaOutAttenuation(voaAttenuation);
	    }

	    // Updating signal
	    // Save the output power of this amplifier
	    monitors[i].setOutputSignal(amplifiers[i].transferFunction(monitors[i].getInputSignal()));

	    if (i + 1 < numberOfAmplifiers) {
		// updating the input power of the next amplifier
		OpticalSignal result = super.linkTrasferFunction(monitors[i].getOutputSignal(), linkLosses[i]);
		amplifiers[i + 1].setInputPower(result.getTotalPower());
		// Save the input power of this amplifier
		monitors[i + 1] = new AmplifierSignalMonitor();
		monitors[i + 1].setInputSignal(result);
	    }
	}

	return amplifiers;
    }

    private float applyRestriction(float targetGain, Amplifier amplifier) {
	PowerMask pm = PowerMaskFactory.getInstance().fabricatePowerMask(amplifier.getType());

	if (targetGain < pm.getMinGain()) {
	    return pm.getMinGain();
	} else if (targetGain > pm.getMaxGain()) {
	    return pm.getMaxGain();
	}

	return targetGain;
    }

    /**
     * @param args
     */
    public static void main(String[] args) {

	ACOPHeuristic heuristic;
	ObjectiveFunction function = new LinearInterpolationFunction();

	float chPower = -20.0f; // -20 dBm/ch = -4 dBm ;; -19 dBm/ch = -3 dBm
	int numberCh = 40;
	int numberAmps = 20;
	float loss = 19.0f;

	float[] linLosses = { 17f, 21f, 18f, 23f, 20f, 20f, 19f, 24f, 24f, 17f, 16f, 19f, 16f, 21f, 17f, 15f, 23f, 19f,
		23f };

	SimulationSetup simSet = new SimSetPadTec(numberCh, chPower, numberAmps, linLosses);

	int numberAmplifiers = simSet.getNumberOfAmplifiers();

	// Definindo ganho máximo
	float maxPout = simSet.getMaxOutputPower();
	System.out.println(maxPout);

	PowerMaskSignal signal = new PowerMaskSignal(numberCh, AmplifierType.EDFA_1_PadTec,
		simSet.getCHANNEL_POWER(), 40);
	OpticalSignal inputSignal = signal.createSignal();

	long t1 = System.currentTimeMillis();
	heuristic = new LossComp(numberAmplifiers, linLosses, inputSignal, function);
	heuristic.setInitialization(new UniformInitialization(AmplifierType.EDFA_1_PadTec));
	heuristic.setVoaMaxAttenuation(simSet.getVOA_MAX_ATT());
	heuristic.setRoadmAttenuation(simSet.getROADM_ATT());
	heuristic.setMaxOutputPower(maxPout);
	Amplifier[] amplifiers = heuristic.execute();

	OpticalSignal outputSignal = heuristic.getMonitors()[numberAmplifiers - 1].getOutputSignal();
	double tilt = Math.abs(SignalFeatureCalculation.calculateTiltLinearReg(outputSignal));
	double ripple = SignalFeatureCalculation.calculateRipple(outputSignal);
	double bitrate = SignalFeatureCalculation.calculateBitRate(outputSignal);

	System.out.format("%.4f\t%.4f\t%.4f\t|\t", tilt, bitrate, ripple);

	System.out.println();
	for (int i = 0; i < amplifiers.length; i++) {
	    System.out.println(amplifiers[i]);
	}

	System.out.println("Tempo V = " + (System.currentTimeMillis() - t1));
    }
}
