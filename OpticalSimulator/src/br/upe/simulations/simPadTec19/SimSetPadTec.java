package br.upe.simulations.simPadTec19;

import br.upe.simulations.simsetups.SimulationSetup;

public class SimSetPadTec extends SimulationSetup {



    public SimSetPadTec(int numberCh, float chPower, int nAmps, float loss) {
	super.setNumberOfAmplifiers(nAmps);

	float[] losses = new float[getNumberOfAmplifiers() - 1];
	for (int i = 0; i < losses.length; i++) {
	    losses[i] = loss;
	}

	super.setLINK_LOSSES(losses);
	super.setCHANNELS(numberCh);
	super.setCHANNEL_POWER(chPower); // dBm
	super.setMaxChannelPower(Float.MAX_VALUE);
	super.setVOA_MAX_ATT(20.0f); // dB
	super.setROADM_ATT(10); // dBm
    }

}
