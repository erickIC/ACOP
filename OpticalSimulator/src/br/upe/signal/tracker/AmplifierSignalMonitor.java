package br.upe.signal.tracker;

import br.upe.base.OpticalSignal;

public class AmplifierSignalMonitor {
	private OpticalSignal inputSignal;
	private OpticalSignal outputSignal;

	public OpticalSignal getInputSignal() {
		return inputSignal;
	}

	public void setInputSignal(OpticalSignal inputSignal) {
		this.inputSignal = inputSignal.clone();
	}

	public OpticalSignal getOutputSignal() {
		return outputSignal;
	}

	public void setOutputSignal(OpticalSignal outputSignal) {
		this.outputSignal = outputSignal.clone();
	}
}
