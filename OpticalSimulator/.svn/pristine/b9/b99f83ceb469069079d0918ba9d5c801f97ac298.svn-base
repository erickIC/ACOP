package br.upe.signal.factory;

import br.upe.util.DecibelConverter;

public class ITUGridRandomSignal extends ITUSignalFactory {
	private double OSNR;
	private double signalPower;
	private double[] noisePower;
	
	public ITUGridRandomSignal(int channelNumber, double initialFrequency, double channelSpacing, double signalPower, double OSNR) {
		super(channelNumber, initialFrequency, channelSpacing);
		this.OSNR = OSNR;
		this.signalPower = signalPower;
		noisePower = new double[channelNumber];
	}

	@Override
	protected double calculateSignalPower(int channelIndex) {
		double signalLin = DecibelConverter.toLinearScale(signalPower);
		double lower = signalLin*0.7;
		double upper = signalLin*1.3;
		double realSignalPower = Math.random() * (upper - lower) + lower;
		
		noisePower[channelIndex] = realSignalPower/DecibelConverter.toLinearScale(OSNR);
		
		return DecibelConverter.toDecibelScale(realSignalPower);
	}

	@Override
	protected double calculateNoisePower(int channelIndex) {
		return DecibelConverter.toDecibelScale(noisePower[channelIndex]);
	}

}
