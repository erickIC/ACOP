package br.upe.initializations;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.AmplifierVOA;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalChannel;
import br.upe.base.OpticalSignal;
import br.upe.mascara.PowerMask;
import br.upe.mascara.PowerMaskFactory;
import br.upe.util.DecibelConverter;

public class BruteForceInitialization implements InitializationStrategy {

    private float[] gains;
    private float[] attenuations;
    private AmplifierType type;
    private OpticalSignal signal;
    private boolean hasVOA;
    private float maxOutPower;

    public BruteForceInitialization(AmplifierType type, boolean hasVOA, float maxOutPower) {
	this.type = type;
	this.hasVOA = hasVOA;
	this.maxOutPower = maxOutPower;
    }

    @Override
    public Amplifier[] initialize(int numberOfAmplifiers, float linkInputPower, float linkOutputPower,
	    float[] linkLosses, ObjectiveFunction function, OpticalSignal inputSignal) {
	Amplifier[] amplifiers = new Amplifier[numberOfAmplifiers];
	if (attenuations == null) {
	    attenuations = new float[numberOfAmplifiers];
	}

	this.signal = inputSignal;

	for (int i = 0; i < numberOfAmplifiers; i++) {
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

		if (i + 1 < numberOfAmplifiers) {
		    // updating the input power of the next amplifier
		    linkTrasferFunction(linkLosses[i], signal);
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

}
