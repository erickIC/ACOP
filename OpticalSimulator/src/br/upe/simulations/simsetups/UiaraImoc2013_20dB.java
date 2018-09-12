package br.upe.simulations.simsetups;

public class UiaraImoc2013_20dB extends SimulationSetup {

	public UiaraImoc2013_20dB() {
		super.setNumberOfAmplifiers(4);
		
		float[] losses = { 20f, 20f, 20f };
		super.setLINK_LOSSES(losses);

		super.setCHANNELS(40);
		super.setCHANNEL_POWER(-15f); // dBm
		super.setVOA_MAX_ATT(20f); // dB
	}

}
