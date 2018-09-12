package br.upe.initializations;

import br.upe.base.Amplifier;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalSignal;

public interface InitializationStrategy {

	public Amplifier[] initialize(int numberOfAmplifiers, float linkInputPower, 
 float linkOutputPower,
			float[] linkLosses, ObjectiveFunction function, OpticalSignal signal);
}
