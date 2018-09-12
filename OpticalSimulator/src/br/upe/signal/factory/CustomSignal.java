package br.upe.signal.factory;

import br.upe.base.OpticalChannel;
import br.upe.util.DecibelConverter;

public class CustomSignal extends SignalFactory {
    private double OSNR;
    private double[] frequencys;
    private double[] signalPower;
    private double[] noisePower;

    public CustomSignal(double[] frequencys, double[] signalPower, double OSNR) {
	super(frequencys.length);
	this.signalPower = signalPower;
	this.OSNR = OSNR;
	noisePower = null;

	this.frequencys = frequencys;
    }

    public CustomSignal(double[] frequencys, double[] signalPower, double[] signalNoise) {
	super(frequencys.length);
	this.signalPower = signalPower;
	this.noisePower = signalNoise;

	this.frequencys = frequencys;
    }

    @Override
    protected OpticalChannel createChannel(int channelIndex) {
	return new OpticalChannel(frequencys[channelIndex], calculateSignalPower(channelIndex),
		calculateNoisePower(channelIndex));
    }

    @Override
    protected double calculateSignalPower(int channelIndex) {
	return this.signalPower[channelIndex];
    }

    @Override
    protected double calculateNoisePower(int channelIndex) {
	if (this.noisePower != null)
	    return noisePower[channelIndex];

	double signalLin = DecibelConverter.toLinearScale(signalPower[channelIndex]);
	double osnrLin = DecibelConverter.toLinearScale(OSNR);
	double noiseLin = signalLin / osnrLin;

	return DecibelConverter.toDecibelScale(noiseLin);
    }

}
