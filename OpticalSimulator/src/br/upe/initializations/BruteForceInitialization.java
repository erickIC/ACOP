package br.upe.initializations;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.AmplifierVOA;
import br.upe.base.Fiber;
import br.upe.base.FiberType;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalChannel;
import br.upe.base.OpticalSignal;
import br.upe.mascara.PowerMask;
import br.upe.mascara.PowerMaskFactory;
import br.upe.objfunctions.linerInterpolation.LinearInterpolationFunction;
import br.upe.signal.factory.PowerMaskSignal;
import br.upe.util.DecibelConverter;
import br.upe.util.SignalFeatureCalculation;

public class BruteForceInitialization implements InitializationStrategy {

    private float[] gains;
    private float[] attenuations;
    private AmplifierType type;
    private OpticalSignal signal;
    private boolean hasVOA;
    private float maxOutPower;
    private double[] tiltOut;
    private OpticalSignal[] signalOut;

    public BruteForceInitialization(AmplifierType type, boolean hasVOA, float maxOutPower) {
	this.type = type;
	this.hasVOA = hasVOA;
	this.maxOutPower = maxOutPower;
    }

    @Override
    public Amplifier[] initialize(int numberOfAmplifiers, float linkInputPower, float linkOutputPower,
	    float[] linkLosses, ObjectiveFunction function, OpticalSignal inputSignal) {
	Amplifier[] amplifiers = new Amplifier[numberOfAmplifiers];
	tiltOut = new double[numberOfAmplifiers];
	if (attenuations == null) {
	    attenuations = new float[numberOfAmplifiers];
	}

	this.signal = inputSignal;
	signalOut = new OpticalSignal[numberOfAmplifiers];

	for (int i = 0; i < numberOfAmplifiers; i++) {
	    // calculate the signal tilt
	    double tilt = SignalFeatureCalculation.calculateTiltNonLinearReg(signal);
	    // select the best mask considering the signal tilt
	    type = getAmplifierType(tilt);

	    // The first amplifier
	    if (i == 0) {
		if (!hasVOA)
		    amplifiers[0] = new Amplifier(linkInputPower, gains[i], type);
		else {
		    amplifiers[0] = new AmplifierVOA(linkInputPower, gains[i], type);
		    ((AmplifierVOA) amplifiers[0]).setVoaOutAttenuation(this.attenuations[0]);
		}
	    }
	    // The last amplifier
	    else if (i + 1 == numberOfAmplifiers) {
		float inputPower = signal.getTotalPower();
		amplifiers[i] = new AmplifierVOA(inputPower, gains[i], type);
		((AmplifierVOA) amplifiers[i]).setVoaOutAttenuation(this.attenuations[i]);
	    }
	    // The others amplifiers
	    else {
		float inputPower = signal.getTotalPower();
		if (!hasVOA)
		    amplifiers[i] = new Amplifier(inputPower, gains[i], type);
		else {
		    amplifiers[i] = new AmplifierVOA(inputPower, gains[i], type);
		    ((AmplifierVOA) amplifiers[i]).setVoaOutAttenuation(this.attenuations[i]);
		}
	    }

	    if (applyRestriction(amplifiers[i])) {
		function.defineNewOperationPoint(amplifiers[i], signal);

		if (amplifiers[i].getGainPerChannel() == null)
		    return null;

		if (amplifiers[i] instanceof AmplifierVOA)
		    outputPowerCorrection((AmplifierVOA) amplifiers[i]);

		// Use the amplifier to transform the signal
		signal = amplifiers[i].transferFunction(signal);

		signalOut[i] = signal.clone();
		tiltOut[i] = SignalFeatureCalculation.calculateTiltLinearReg(signal);

		if (i + 1 < numberOfAmplifiers) {
		    // updating the input power of the next amplifier
		    signal = new Fiber(FiberType.SMF_28, linkLosses[i]).linkTrasferFunction(signal);
		    // linkTrasferFunction(linkLosses[i], signal);
		}
	    } else {
		return null;
	    }
	}

	inputSignal.setChannels(signal.getChannels());
	return amplifiers;
    }

    private void outputPowerCorrection(AmplifierVOA amplifier) {
	if (amplifier.getOutputPowerAfterVOA() > this.maxOutPower) {
	    amplifier.setVoaOutAttenuation(amplifier.getOutputPower() - this.maxOutPower);
	}

    }

    /**
     * @return the gains
     */
    public float[] getGains() {
	return gains;
    }

    /**
     * @param gains
     *            the gains to set
     */
    public void setGains(float[] gains) {
	this.gains = gains;
    }

    public float[] getAttenuations() {
	return attenuations;
    }

    public double[] getTiltsOut() {
	return tiltOut;
    }

    public void setAttenuations(float[] attenuations) {
	this.attenuations = attenuations;
    }

    private void linkTrasferFunction(float linkLoss, OpticalSignal signal) {
	for (OpticalChannel c : signal.getChannels()) {
	    // Signal Total Gain
	    double signalLin = DecibelConverter.toLinearScale(c.getSignalPower());
	    signalLin *= DecibelConverter.toLinearScale(-1 * linkLoss);
	    // Noise Gain
	    double noiseLin = DecibelConverter.toLinearScale(c.getNoisePower());
	    noiseLin *= DecibelConverter.toLinearScale(-1 * linkLoss);

	    c.setSignalPower(DecibelConverter.toDecibelScale(signalLin));
	    c.setNoisePower(DecibelConverter.toDecibelScale(noiseLin));
	}
    }

    private boolean applyRestriction(Amplifier amplifier) {
	amplifier.calculateGain();
	PowerMask pm = PowerMaskFactory.getInstance().fabricatePowerMask(amplifier.getType());

	if (Math.round(amplifier.getGain()) < pm.getMinGain()) {
	    return false;
	} else if (Math.round(amplifier.getGain()) > pm.getMaxGain()) {
	    return false;
	} // Restricao para manter pontos dentro da mascara.
	else {
	    int gain = (int) amplifier.getGain();
	    float relax = 0.5f;

	    // Se o Pin é maior do que o maximo ou menor que o mínimo.
	    if (amplifier.getInputPower() > (pm.getMaxTotalInputPower(gain) + relax)
		    || amplifier.getInputPower() < (pm.getMinTotalInputPower(gain) - relax)) {
		return false;
	    }

	}

	return true;
    }

    public OpticalSignal getSignal() {
	return signal;
    }

    public void setSignal(OpticalSignal signal) {
	this.signal = signal;
    }

    public boolean isHasVOA() {
	return hasVOA;
    }

    public void setHasVOA(boolean hasVOA) {
	this.hasVOA = hasVOA;
    }

    private AmplifierType getAmplifierType(double tilt) {
	if (tilt < 0) {
	    tilt *= -1;
	    if (tilt < 1)
		return AmplifierType.EDFA_1_PadTec;
	    else if (tilt >= 1 && tilt < 3)
		return AmplifierType.EDFA_1_Tm2_PadTec;
	    else if (tilt >= 3 && tilt < 5)
		return AmplifierType.EDFA_1_Tm4_PadTec;
	    else if (tilt >= 5 && tilt < 7)
		return AmplifierType.EDFA_1_Tm6_PadTec;
	    else if (tilt >= 7 && tilt < 9)
		return AmplifierType.EDFA_1_Tm8_PadTec;
	    else if (tilt >= 9 && tilt < 11)
		return AmplifierType.EDFA_1_Tm10_PadTec;
	    else
		return AmplifierType.EDFA_1_Tm12_PadTec;
	} else {
	    if (tilt < 1)
		return AmplifierType.EDFA_1_PadTec;
	    else if (tilt >= 1 && tilt < 3)
		return AmplifierType.EDFA_1_T2_PadTec;
	    else if (tilt >= 3 && tilt < 5)
		return AmplifierType.EDFA_1_T4_PadTec;
	    else if (tilt >= 5 && tilt < 7)
		return AmplifierType.EDFA_1_T6_PadTec;
	    else if (tilt >= 7 && tilt < 9)
		return AmplifierType.EDFA_1_T8_PadTec;
	    else if (tilt >= 9 && tilt < 11)
		return AmplifierType.EDFA_1_T10_PadTec;
	    else
		return AmplifierType.EDFA_1_T12_PadTec;
	}
    }

    public OpticalSignal[] getSignalOut() {
	return signalOut;
    }

    public static void main(String[] args0) {
	BruteForceInitialization bfIni = new BruteForceInitialization(AmplifierType.EDFA_1_PadTec, false,
		Float.MAX_VALUE);
	float[] gains = { 23, 21, 18, 23, 18, 22, 19, 21, 20, 18, 22, 19, 19, 22, 21, 17, 23, 20, 19, 19 };
	bfIni.setGains(gains);
	
	ObjectiveFunction function = new LinearInterpolationFunction();
	PowerMaskSignal signal = new PowerMaskSignal(40, AmplifierType.EDFA_1_PadTec, -20, 40);
	OpticalSignal inputSignal = signal.createSignal();

	float totalInputPower = inputSignal.getTotalPower();
	float[] losses = new float[20];
	for (int i = 0; i < losses.length; i++) {
	    losses[i] = 20f;
	}
	
	Amplifier[] amplifiers = bfIni.initialize(20, totalInputPower, 0, losses, function, inputSignal);
	for (int i = 0; i < amplifiers.length; i++) {
	    System.out.println(amplifiers[i].getOutputPower());
	}
    }
}
