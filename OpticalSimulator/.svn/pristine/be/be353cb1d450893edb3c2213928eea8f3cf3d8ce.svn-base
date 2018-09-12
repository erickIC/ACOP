package br.upe.initializations;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.AmplifierVOA;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalSignal;
import br.upe.mascara.PowerMask;
import br.upe.mascara.PowerMaskFactory;

public class UniformInitialization implements InitializationStrategy {
	private AmplifierType type;

	public UniformInitialization(AmplifierType type){
		this.type = type;
	}

	@Override	
	public Amplifier[] initialize(int numberOfAmplifiers, float linkInputPower,
 float linkOutputPower,
			float[] linkLosses, ObjectiveFunction function, OpticalSignal signal) {
		Amplifier[] amplifiers = new Amplifier[numberOfAmplifiers];

		PowerMask pm = PowerMaskFactory.getInstance().fabricatePowerMask(type);
		for (int i = 0; i < numberOfAmplifiers; i++) {
			// The first amplifier
			if (i == 0) {
				amplifiers[0] = new Amplifier(linkInputPower, type);
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
				amplifiers[i] = new Amplifier(inputPower, type);
			}
		}

		return amplifiers;
	}
}
