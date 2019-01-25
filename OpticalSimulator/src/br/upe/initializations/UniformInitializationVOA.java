package br.upe.initializations;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.AmplifierVOA;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalSignal;
import br.upe.mascara.PowerMask;
import br.upe.mascara.PowerMaskFactory;

public class UniformInitializationVOA implements InitializationStrategy {
    private AmplifierType type;
    private float[] voaLosses;

    public UniformInitializationVOA(AmplifierType type) {
	this.type = type;
    }

    public UniformInitializationVOA(AmplifierType type, float[] voaLosses) {
	this.type = type;
	this.voaLosses = voaLosses;
    }

    @Override
    public Amplifier[] initialize(int numberOfAmplifiers, float linkInputPower, float linkOutputPower,
	    float[] linkLosses, ObjectiveFunction function, OpticalSignal signal) {
	AmplifierVOA[] amplifiers = new AmplifierVOA[numberOfAmplifiers];

	PowerMask pm = PowerMaskFactory.getInstance().fabricatePowerMask(type);
	for (int i = 0; i < numberOfAmplifiers; i++) {
	    // The first amplifier
	    if (i == 0) {
		amplifiers[0] = new AmplifierVOA(linkInputPower, type);
		amplifiers[0].setOutputPower(linkOutputPower + pm.getMinGain());
		amplifiers[0].calculateGain();
	    }
	    // The last amplifier
	    else if (i + 1 == numberOfAmplifiers) {
		float inputPower = amplifiers[i - 1].getOutputPower() - linkLosses[i - 1];
		amplifiers[i] = new AmplifierVOA(inputPower, type);
	    }
	    // The others amplifiers
	    else {
		float inputPower = amplifiers[i - 1].getOutputPower() - linkLosses[i - 1];
		amplifiers[i] = new AmplifierVOA(inputPower, type);
	    }
	    
	    if(voaLosses != null)
		amplifiers[i].setVoaOutAttenuation(voaLosses[i]);
	}

	return amplifiers;
    }
}
