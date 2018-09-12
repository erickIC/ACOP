package br.upe.mascara;

import java.util.ArrayList;
import java.util.HashMap;

public class PowerMask {
    /**
     * Set of Operating Points
     */
    private ArrayList<OperatingPoint> operatingPoints;

    /**
     * The minimum total input power (dB) among all operating points
     */
    private float minTotalInputPower;
    /**
     * The maximum total input power (dB) among all operating points
     */
    private float maxTotalInputPower;
    /**
     * The minimum gain (dB) among all operating points
     */
    private int minGain;
    /**
     * The maximum gain (dB) among all operating points
     */
    private int maxGain;
    /**
     * The minimum total input power (dB) for each possible gain among all
     * operating points
     */
    private HashMap<Integer, Float> minTotalPinPerGain;
    /**
     * The maximum total input power (dB) for each possible gain among all
     * operating points
     */
    private HashMap<Integer, Float> maxTotalPinPerGain;
    /**
     * The maximum channel frequency (Hz) among all operating points
     */
    private float maxFrequency;
    /**
     * The minimum channel frequency (Hz) among all operating points
     */
    private float minFrequency;
    /**
     * The maximum channel gain (dB) among all operating points
     */
    private float maxGainPerChannel;
    /**
     * The minimum channel gain (dB) among all operating points
     */
    private float minGainPerChannel;
    /**
     * The maximum noise figure (dB) among all operating points
     */
    private float maxNoiseFigure;
    /**
     * The minimum noise figure (dB) among all operating points
     */
    private float minNoiseFigure;

    @Override
    protected Object clone() throws CloneNotSupportedException {
	PowerMask newPM = new PowerMask();
	newPM.setMaxFrequency(maxFrequency);
	newPM.setMinFrequency(minFrequency);
	newPM.setMaxGain(maxGain);
	newPM.setMinGain(minGain);
	newPM.setMinTotalInputPower(minTotalInputPower);
	newPM.setMaxTotalInputPower(maxTotalInputPower);
	newPM.setMaxGainPerChannel(maxGainPerChannel);
	newPM.setMinGainPerChannel(minGainPerChannel);
	newPM.setMaxNoiseFigure(maxNoiseFigure);
	newPM.setMinNoiseFigure(minNoiseFigure);

	ArrayList<OperatingPoint> tempList = new ArrayList<OperatingPoint>();
	for (OperatingPoint op : operatingPoints) {
	    tempList.add((OperatingPoint) op.clone());
	}
	newPM.setOperatingPoints(tempList);

	newPM.setMinTotalPinPerGain((HashMap<Integer, Float>) minTotalPinPerGain.clone());
	newPM.setMaxTotalPinPerGain((HashMap<Integer, Float>) maxTotalPinPerGain.clone());

	return newPM;
    }

    public ArrayList<OperatingPoint> getOperatingPoints() {
	return operatingPoints;
    }

    public void setOperatingPoints(ArrayList<OperatingPoint> operatingPoints) {
	this.operatingPoints = operatingPoints;
    }

    public void setMaxTotalPinPerGain(HashMap<Integer, Float> maxTotalPinPerGain) {
	this.maxTotalPinPerGain = maxTotalPinPerGain;
    }

    public void setMinTotalPinPerGain(HashMap<Integer, Float> minTotalPinPerGain) {
	this.minTotalPinPerGain = minTotalPinPerGain;
    }

    public float getMinTotalInputPower() {
	return minTotalInputPower;
    }

    public void setMinTotalInputPower(float minTotalInputPower) {
	this.minTotalInputPower = minTotalInputPower;
    }

    public float getMaxTotalOutputPower() {
	return (this.maxGain + this.maxTotalInputPower);
    }

    public int getMinGain() {
	return minGain;
    }

    public void setMinGain(int minGain) {
	this.minGain = minGain;
    }

    public int getMaxGain() {
	return maxGain;
    }

    public void setMaxGain(int maxGain) {
	this.maxGain = maxGain;
    }

    public float getMaxTotalInputPower() {
	return maxTotalInputPower;
    }

    public void setMaxTotalInputPower(float maxTotalInputPower) {
	this.maxTotalInputPower = maxTotalInputPower;
    }

    public float getMinTotalOutputPower() {
	return (this.minGain + this.minTotalInputPower);
    }

    public float getMaxTotalInputPower(int gain) {
	return maxTotalPinPerGain.get(gain);
    }

    public float getMinTotalInputPower(int gain) {
	return minTotalPinPerGain.get(gain);
    }

    public float getMaxFrequency() {
	return maxFrequency;
    }

    public void setMaxFrequency(float maxFrequency) {
	this.maxFrequency = maxFrequency;
    }

    public float getMinFrequency() {
	return minFrequency;
    }

    public void setMinFrequency(float minFrequency) {
	this.minFrequency = minFrequency;
    }

    public float getMaxGainPerChannel() {
	return maxGainPerChannel;
    }

    public void setMaxGainPerChannel(float maxGainPerChannel) {
	this.maxGainPerChannel = maxGainPerChannel;
    }

    public float getMinGainPerChannel() {
	return minGainPerChannel;
    }

    public void setMinGainPerChannel(float minGainPerChannel) {
	this.minGainPerChannel = minGainPerChannel;
    }

    public float getMaxNoiseFigure() {
	return maxNoiseFigure;
    }

    public void setMaxNoiseFigure(float maxNoiseFigure) {
	this.maxNoiseFigure = maxNoiseFigure;
    }

    public float getMinNoiseFigure() {
	return minNoiseFigure;
    }

    public void setMinNoiseFigure(float minNoiseFigure) {
	this.minNoiseFigure = minNoiseFigure;
    }

    public HashMap<Integer, Float> getMinTotalPinPerGain() {
	return minTotalPinPerGain;
    }

    public HashMap<Integer, Float> getMaxTotalPinPerGain() {
	return maxTotalPinPerGain;
    }
}
