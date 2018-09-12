package br.upe.base;

import java.text.NumberFormat;

public class OpticalChannel {
	private double frequency;
	private double SignalPower;
	private double NoisePower;
		
	/**
	 * 
	 * @param frequency in Hz
	 * @param signalPower in dBm
	 * @param noisePower in dBm
	 */
	public OpticalChannel(double frequency, double signalPower, double noisePower) {
		super();
		this.frequency = frequency;
		SignalPower = signalPower;
		NoisePower = noisePower;
	}
	
	/**
	 * 
	 * @return frequency in Hz
	 */
	public double getFrequency() {
		return frequency;
	}
	
	/**
	 * 
	 * @param frequency in Hz
	 */
	public void setFrequency(double frequency) {
		this.frequency = frequency;
	}
	
	/**
	 * 
	 * @return dBm
	 */
	public double getSignalPower() {
		return SignalPower;
	}
	
	/**
	 * 
	 * @param signalPower in dBm
	 */
	public void setSignalPower(double signalPower) {
		SignalPower = signalPower;
	}
	
	/**
	 * 
	 * @return in dB
	 */
	public double getNoisePower() {
		return NoisePower;
	}
	
	/**
	 * 
	 * @param noisePower in dB
	 */
	public void setNoisePower(double noisePower) {
		NoisePower = noisePower;
	}
	
	@Override
	public String toString() {
		NumberFormat nf = NumberFormat.getInstance();
		nf.setMaximumFractionDigits(2);
		nf.setMinimumFractionDigits(2);
			
		StringBuffer strBuff = new StringBuffer();
		double freqTemp = this.frequency / 1e12;
		strBuff.append(nf.format(freqTemp) + "\t");
		strBuff.append(nf.format(this.SignalPower) + "\t");
		strBuff.append(nf.format(this.NoisePower));
			
		return strBuff.toString();
	}
	
	protected OpticalChannel clone() {
		return new OpticalChannel(frequency, SignalPower, NoisePower);
	}
}
