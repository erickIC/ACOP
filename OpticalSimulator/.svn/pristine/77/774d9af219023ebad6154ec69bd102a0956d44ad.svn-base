package br.upe.simulations.simsetups;

public class UiaraImoc2013 extends SimulationSetup {

	public UiaraImoc2013(int numberCh, float chPower, float chMaxPower) {
		super.setNumberOfAmplifiers(4);

		float[] losses = { 18f, 18f, 18f};//, 18f, 18f, 18f, 18f};//, 18f, 18f};
		super.setLINK_LOSSES(losses);

		super.setCHANNELS(numberCh);
		super.setCHANNEL_POWER(chPower); // dBm
		super.setMaxChannelPower(chMaxPower);
		super.setVOA_MAX_ATT(30f); // dB
		super.setROADM_ATT(18); //dBm
	}

}
