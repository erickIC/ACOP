package br.upe.base;

import java.text.NumberFormat;

import br.upe.util.DecibelConverter;

public class AmplifierVOA extends Amplifier {

    private float voaOutAttenuation;
    private float voaInAttenuation;
    private boolean attenuationsSetted;

    public AmplifierVOA(float inputPower, AmplifierType type) {
	super(inputPower, type);
	voaOutAttenuation = 0.0f;
	voaInAttenuation = 0.0f;
    }

    public AmplifierVOA(float inputPower, float gain, AmplifierType type) {
	super(inputPower, gain, type);
	voaOutAttenuation = 0.0f;
	voaInAttenuation = 0.0f;
    }

    public AmplifierVOA(float inputPower, float gain, float outputPower, float noiseFigure, float flatness,
	    float powerConsumption, AmplifierType type) {
	super(inputPower, gain, outputPower, noiseFigure, flatness, powerConsumption, type);
	voaOutAttenuation = 0.0f;
	voaInAttenuation = 0.0f;
    }

    public float getVoaOutAttenuation() {
	return voaOutAttenuation;
    }

    public float getVoaInAttenuation() {
	return voaInAttenuation;
    }

    public void setVoaOutAttenuation(float voaAttenuation) {
	this.voaOutAttenuation = voaAttenuation;
	this.attenuationsSetted = true;
    }

    public void setVoaInAttenuation(float voaInAttenuation) {
	this.voaInAttenuation = voaInAttenuation;
	setInputPower(getInputPower() - voaInAttenuation);
	calculateGain();
    }

    public void increaseVoaOutAttenuation(float increaseValue) {
	this.voaOutAttenuation += increaseValue;
    }

    public float getOutputPowerAfterVOA() {
	return getOutputPower() - voaOutAttenuation;
    }

    @Override
    public String toString() {
	NumberFormat nf = NumberFormat.getInstance();
	nf.setMaximumFractionDigits(2);
	nf.setMinimumFractionDigits(2);

	StringBuffer strBuff = new StringBuffer();
	strBuff.append("[(" + nf.format(this.voaInAttenuation) + ") ");
	strBuff.append(nf.format(super.getInputPower()) + "\t");
	strBuff.append(nf.format(super.getGain()) + "\t");
	strBuff.append(nf.format(super.getOutputPower()) + " ");
	strBuff.append("(" + nf.format(this.voaOutAttenuation) + ")\t");
	strBuff.append(nf.format(super.getNoiseFigure()) + "\t");
	strBuff.append(nf.format(super.getFlatness()) + "\t");
	strBuff.append(nf.format(super.getMaskOSNR()) + "]");

	return strBuff.toString();
    }

    @Override
    public OpticalSignal transferFunction(OpticalSignal signal) {
	OpticalSignal result = signal.clone();
	for (OpticalChannel c : result.getChannels()) {
	    // Signal Total Gain (VOA + AMP)
	    double channelGain = calculateChannelFeature(c.getFrequency(), super.getGainPerChannel());
	    double signalLin = DecibelConverter.toLinearScale(c.getSignalPower());
	    signalLin *= DecibelConverter.toLinearScale(-1 * voaInAttenuation);
	    signalLin *= channelGain;
	    signalLin *= DecibelConverter.toLinearScale(-1 * voaOutAttenuation);
	    // Noise Gain
	    double noiseLin = DecibelConverter.toLinearScale(c.getNoisePower());
	    noiseLin *= DecibelConverter.toLinearScale(-1 * voaInAttenuation);
	    noiseLin *= channelGain;
	    // ASE Added
	    noiseLin += calculateAsePower(c.getFrequency(), channelGain);
	    noiseLin *= DecibelConverter.toLinearScale(-1 * voaOutAttenuation);

	    c.setSignalPower(DecibelConverter.toDecibelScale(signalLin));
	    c.setNoisePower(DecibelConverter.toDecibelScale(noiseLin));
	}

	return result;
    }

    public boolean isAttenuationsSetted() {
	return attenuationsSetted;
    }

    public void setAttenuationsSetted(boolean attenuationsSetted) {
	this.attenuationsSetted = attenuationsSetted;
    }

}
