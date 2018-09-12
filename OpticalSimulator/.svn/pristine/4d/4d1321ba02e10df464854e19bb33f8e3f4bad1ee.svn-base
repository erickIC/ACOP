package br.upe.signal.factory;

import br.upe.util.DecibelConverter;

public class ITUGridLinearTiltedSignal extends ITUSignalFactory {
	private double OSNR;
	private double signalPower;
	private double[] noisePower;
	private double factor;
	private int channelNumber;
	
	public ITUGridLinearTiltedSignal(int channelNumber, double initialFrequency, double channelSpacing,
			double signalPower, double OSNR, double tilt) {
		super(channelNumber, initialFrequency, channelSpacing);
		this.OSNR = OSNR;
		this.signalPower = signalPower;
		this.factor = (tilt / (double) channelNumber);
		this.channelNumber = channelNumber;
		noisePower = new double[channelNumber];
	}

	@Override
	protected double calculateSignalPower(int channelIndex) {
		
		double realSignalPower = signalPower + (((channelNumber + 1) / 2.0) - channelIndex + 1) * factor;

		double signalLin = DecibelConverter.toLinearScale(realSignalPower);

		if (Double.isNaN(signalLin))
			System.out.println();

		noisePower[channelIndex] = signalLin / DecibelConverter.toLinearScale(OSNR);
		
		return DecibelConverter.toDecibelScale(signalLin);
	}

	@Override
	protected double calculateNoisePower(int channelIndex) {
		return DecibelConverter.toDecibelScale(noisePower[channelIndex]);
	}

}
