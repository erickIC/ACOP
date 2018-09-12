package br.upe.simulations.simsetups;

import br.upe.util.DecibelConverter;

public abstract class SimulationSetup {
    private int numberOfAmplifiers = 4;
    private float[] LINK_LOSSES = { 20f, 20f, 20f };

    private int CHANNELS = 10;
    private float CHANNEL_POWER = -15f; // dBm

    private float MAX_POWER = 0; // dBm

    private float VOA_MAX_ATT = 20.0f; // dB

    private float ROADM_ATT = 10.0f; // dB

    public int getNumberOfAmplifiers() {
	return numberOfAmplifiers;
    }

    public void setNumberOfAmplifiers(int numberOfAmplifiers) {
	this.numberOfAmplifiers = numberOfAmplifiers;
    }

    public void setLINK_LOSSES(float[] lINK_LOSSES) {
	LINK_LOSSES = lINK_LOSSES;
    }

    public void setCHANNELS(int cHANNELS) {
	CHANNELS = cHANNELS;
    }

    protected void setCHANNEL_POWER(float cHANNEL_POWER) {
	CHANNEL_POWER = cHANNEL_POWER;
    }

    protected void setVOA_MAX_ATT(float vOA_MAX_ATT) {
	VOA_MAX_ATT = vOA_MAX_ATT;
    }

    public float[] getLINK_LOSSES() {
	return LINK_LOSSES;
    }

    public int getCHANNELS() {
	return CHANNELS;
    }

    public float getCHANNEL_POWER() {
	return CHANNEL_POWER;
    }

    public float getVOA_MAX_ATT() {
	return VOA_MAX_ATT;
    }

    protected void setMaxChannelPower(float powerdBm) {
	this.MAX_POWER = (float) DecibelConverter.toDecibelScale((CHANNELS * DecibelConverter.toLinearScale(powerdBm)));
    }

    public float getMaxOutputPower() {
	return MAX_POWER;
    }

    /**
     * @param rOADM_ATT
     *            the rOADM_ATT to set
     */
    protected void setROADM_ATT(float rOADM_ATT) {
	ROADM_ATT = rOADM_ATT;
    }

    /**
     * @return the rOADM_ATT
     */
    public float getROADM_ATT() {
	return ROADM_ATT;
    }
}
