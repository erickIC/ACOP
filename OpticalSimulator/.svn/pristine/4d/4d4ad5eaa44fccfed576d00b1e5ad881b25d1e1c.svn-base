package br.upe.signal.factory;

import br.upe.base.OpticalChannel;

public abstract class ITUSignalFactory extends SignalFactory {

	private static final int C = 299792458; //m/s
	
	private double initialFrequency = 190.10e12f; //THz
	private double channelSpacing;
	
	/**
	 * 
	 * @param channelNumber
	 * @param initialFrequency in Hz
	 * @param channelSpacing in Hz
	 * @param signalPower in dBm
	 * @param OSNR in dB
	 */
	public ITUSignalFactory(int channelNumber, double initialFrequency, double channelSpacing) {
		super(channelNumber);
		this.initialFrequency = initialFrequency;
		this.channelSpacing = channelSpacing;
	}

	@Override
	protected OpticalChannel createChannel(int channelIndex) {
		double frequency = channelSpacing*channelIndex + initialFrequency;
		return new OpticalChannel(frequency, calculateSignalPower(channelIndex), calculateNoisePower(channelIndex));
	}
}
