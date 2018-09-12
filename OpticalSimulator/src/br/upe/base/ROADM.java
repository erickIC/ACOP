package br.upe.base;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import br.upe.util.DecibelConverter;

public class ROADM implements IOpticalDevice {

    private float insertionLoss;
    private HashMap<Double, Double> voaAttenuation; // in dBm
    private float voaMaxAttenuation; // in dBm
    private List<Double> dropFrequencys;
    private List<Double> addFrequencys;

    public ROADM(float insertionLoss, float voaMaxAttenuation) {
	this.insertionLoss = insertionLoss;
	this.voaMaxAttenuation = voaMaxAttenuation;

	this.voaAttenuation = new HashMap<Double, Double>();
	this.dropFrequencys = new ArrayList<Double>();
	this.addFrequencys = new ArrayList<Double>();
    }

    public float getInsertionLoss() {
	return insertionLoss;
    }

    public void setInsertionLoss(float insertionLoss) {
	this.insertionLoss = insertionLoss;
    }

    public HashMap<Double, Double> getVoaAttenuation() {
	return voaAttenuation;
    }

    public void setVoaAttenuation(HashMap<Double, Double> voaAttenuation) {
	this.voaAttenuation = voaAttenuation;
    }

    public float getVoaMaxAttenuation() {
	return voaMaxAttenuation;
    }

    public void setVoaMaxAttenuation(float voaMaxAttenuation) {
	this.voaMaxAttenuation = voaMaxAttenuation;
    }

    public List<Double> getDropFrequencys() {
	return dropFrequencys;
    }

    public void setDropFrequencys(List<Double> dropFrequencys) {
	this.dropFrequencys = dropFrequencys;
    }

    public List<Double> getAddFrequencys() {
	return addFrequencys;
    }

    public void setAddFrequencys(List<Double> addFrequencys) {
	this.addFrequencys = addFrequencys;
    }

    @Override
    public OpticalSignal transferFunction(OpticalSignal signal) {
	OpticalSignal result = signal.clone();
	double deviceLoss = DecibelConverter.toLinearScale(-1 * insertionLoss);
	for (OpticalChannel c : result.getChannels()) {
	    // Signal Gain
	    double voaAttenuation = DecibelConverter.toLinearScale(-1 * this.voaAttenuation.get(c.getFrequency()));
	    double signalLin = DecibelConverter.toLinearScale(c.getSignalPower());
	    signalLin *= voaAttenuation * deviceLoss;
	    // Noise Gain
	    double noiseLin = DecibelConverter.toLinearScale(c.getNoisePower());
	    noiseLin *= voaAttenuation * deviceLoss;

	    c.setSignalPower(DecibelConverter.toDecibelScale(signalLin));
	    c.setNoisePower(DecibelConverter.toDecibelScale(noiseLin));
	}
	return result;
    }

}
