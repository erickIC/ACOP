package br.upe.simulations.simsetups;

public class SimSetAMPVOA_4Amps extends SimulationSetup {

    public SimSetAMPVOA_4Amps(int numberCh, float chPower, float chMaxPower) {
	super.setNumberOfAmplifiers(4);

	float loss = 20f;

	float[] losses = new float[getNumberOfAmplifiers() - 1];
	for (int i = 0; i < losses.length; i++) {
	    losses[i] = loss;
	}
									 // 20f
								    // };// ,
							       // 20f,
							  // 20f
						     // };// ,
						// 20f,
					   // 20f
				      // };// ,
	// 18f,
	// 18f, 18f, 18f};
	super.setLINK_LOSSES(losses);

	super.setCHANNELS(numberCh);
	super.setCHANNEL_POWER(chPower); // dBm
	super.setMaxChannelPower(chMaxPower);
	super.setVOA_MAX_ATT(20.0f); // dB
	super.setROADM_ATT(20); // dBm
    }

}
