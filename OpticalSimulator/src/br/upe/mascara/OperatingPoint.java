package br.upe.mascara;

import java.util.HashMap;

/***
 * This class models an amplifier operating point.
 * 
 * @author Erick
 *
 */
public class OperatingPoint implements Comparable<OperatingPoint> {
    /**
     * Amplifier total input power (dBm)
     */
    private float inputPower;

    /**
     * Amplifier gain set (dB)
     */
    private int gainSet;

    /**
     * Channels input powers (dBm)
     */
    private HashMap<Double, Float> inputPowerPerChannel;

    /**
     * Channels noise figure (dB)
     */
    private HashMap<Double, Float> noiseFigurePerChannel;

    /**
     * Channels gains (dB)
     */
    private HashMap<Double, Float> gainPerChannel;

    /**
     * Channels gnli (W/Hz)
     */
    private HashMap<Double, Float> gnliPerChannel;

    /**
     * Ripple calculated in the lab characterization (dB)
     */
    private float labRipple;

    public float getLabRipple() {
	return labRipple;
    }

    public void setLabRipple(float labRipple) {
	this.labRipple = labRipple;
    }

    @Override
    protected Object clone() throws CloneNotSupportedException {
	OperatingPoint newOp = new OperatingPoint();
	newOp.setTotalInputPower(inputPower);
	newOp.setGainSet(gainSet);
	newOp.setLabRipple(labRipple);

	newOp.setInputPowerPerChannel((HashMap<Double, Float>) inputPowerPerChannel.clone());
	newOp.setNoiseFigurePerChannel((HashMap<Double, Float>) noiseFigurePerChannel.clone());
	newOp.setGainPerChannel((HashMap<Double, Float>) gainPerChannel.clone());
	if (gnliPerChannel != null)
	    newOp.setGnliPerChannel((HashMap<Double, Float>) gnliPerChannel.clone());

	return newOp;
    }

    public float getTotalInputPower() {
	return inputPower;
    }

    public void setTotalInputPower(float inputPower) {
	this.inputPower = inputPower;
    }

    public int getGainSet() {
	return gainSet;
    }

    public void setGainSet(int gainSet) {
	this.gainSet = gainSet;
    }

    public HashMap<Double, Float> getGainPerChannel() {
	return gainPerChannel;
    }

    public void setGainPerChannel(HashMap<Double, Float> gainPerChannel) {
	this.gainPerChannel = gainPerChannel;
    }

    /**
     * Return a string "inputPower, gainSet, "
     */
    @Override
    public String toString() {
	return inputPower + ", " + gainSet + ", ";
    }

    /**
     * Compares the total input power (Pin) of two operating points Return -1 if
     * the current Pin is less than Pin of arg0 Return 1 if the current Pin is
     * greater than Pin of arg0 Return 0 if equals
     */
    @Override
    public int compareTo(OperatingPoint arg0) {
	if (this.inputPower < arg0.getTotalInputPower())
	    return -1;
	if (this.inputPower > arg0.getTotalInputPower())
	    return 1;
	return 0;
    }

    public HashMap<Double, Float> getNoiseFigurePerChannel() {
	return noiseFigurePerChannel;
    }

    public void setNoiseFigurePerChannel(HashMap<Double, Float> noiseFigurePerChannel) {
	this.noiseFigurePerChannel = noiseFigurePerChannel;
    }

    public HashMap<Double, Float> getInputPowerPerChannel() {
	return inputPowerPerChannel;
    }

    public void setInputPowerPerChannel(HashMap<Double, Float> inputPowerPerChannel) {
	this.inputPowerPerChannel = inputPowerPerChannel;
    }

    public HashMap<Double, Float> getGnliPerChannel() {
	return gnliPerChannel;
    }

    public void setGnliPerChannel(HashMap<Double, Float> gnliPerChannel) {
	this.gnliPerChannel = gnliPerChannel;
    }
}
