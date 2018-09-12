package br.upe.simulations.simsetups;

public class SimSetAMPVOA extends SimulationSetup {

    public SimSetAMPVOA(int numberCh, float chMaxPower) {
	float loss = 18f;
	float chPower = -18.0f;

	super.setNumberOfAmplifiers(4);

	float[] losses = new float[getNumberOfAmplifiers() - 1];
	for (int i = 0; i < losses.length; i++) {
	    losses[i] = loss;
	}

	super.setLINK_LOSSES(losses);
	super.setCHANNELS(numberCh);
	super.setCHANNEL_POWER(chPower); // dBm
	super.setMaxChannelPower(chMaxPower);
	super.setVOA_MAX_ATT(20.0f); // dB
	super.setROADM_ATT(18); // dBm
    }

    public SimSetAMPVOA(int numberCh, float chPower, float chMaxPower, int nAmps) {
	float loss = 18f;

	super.setNumberOfAmplifiers(nAmps);

	float[] losses = new float[getNumberOfAmplifiers() - 1];
	for (int i = 0; i < losses.length; i++) {
	    losses[i] = loss;
	}

	super.setLINK_LOSSES(losses);
	super.setCHANNELS(numberCh);
	super.setCHANNEL_POWER(chPower); // dBm
	super.setMaxChannelPower(chMaxPower);
	super.setVOA_MAX_ATT(20.0f); // dB
	super.setROADM_ATT(18); // dBm
    }

    public SimSetAMPVOA(int numberCh, float chMaxPower, float loss) {
	super.setNumberOfAmplifiers(4);

	float[] losses = new float[getNumberOfAmplifiers() - 1];
	for (int i = 0; i < losses.length; i++) {
	    losses[i] = loss;
	}

	super.setLINK_LOSSES(losses);
	super.setCHANNELS(numberCh);
	super.setCHANNEL_POWER(-18.0f); // dBm
	super.setMaxChannelPower(chMaxPower);
	super.setVOA_MAX_ATT(20.0f); // dB
	super.setROADM_ATT(18); // dBm
    }

    public SimSetAMPVOA(int numberCh, float chPower, float chMaxPower, int nAmps, float loss) {
	super.setNumberOfAmplifiers(nAmps);

	float[] losses = new float[getNumberOfAmplifiers() - 1];
	for (int i = 0; i < losses.length; i++) {
	    losses[i] = loss;
	}

	super.setLINK_LOSSES(losses);
	super.setCHANNELS(numberCh);
	super.setCHANNEL_POWER(chPower); // dBm
	super.setMaxChannelPower(chMaxPower);
	super.setVOA_MAX_ATT(20.0f); // dB
	super.setROADM_ATT(18); // dBm
    }

}
