package br.upe.simulations.simPadTec;

import java.util.HashMap;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.AmplifierVOA;
import br.upe.base.OpticalChannel;
import br.upe.base.OpticalSignal;
import br.upe.metrics.BeckerNoiseFigureMetric;
import br.upe.metrics.OSNRMetric;
import br.upe.signal.factory.ITUGridUniformSignal;
import br.upe.util.DecibelConverter;

public class SimPadTec {

    private static double calculateTilt(OpticalSignal signal) {
	double maxPeak = Double.MIN_VALUE;
	double minPeak = Double.MAX_VALUE;

	for (OpticalChannel c : signal.getChannels()) {
	    double signalLin = DecibelConverter.toLinearScale(c.getSignalPower());

	    if (signalLin > maxPeak) {
		maxPeak = signalLin;
	    }
	    if (signalLin < minPeak) {
		minPeak = signalLin;
	    }
	}

	return DecibelConverter.toDecibelScale(maxPeak / minPeak);
    }

    public static void main(String[] args) {
	float inputPower = -6.0f;
	float inputPowerPerCh = -22.02f;
	float gain = 19f;
	float NF = 4.85f;
	float tilt = 0.4f;
	int numberOfAmplifiers = 1;


	HashMap<Double, Float> gainPerChannel = new HashMap<Double, Float>();
	HashMap<Double, Float> nfPerChannel = new HashMap<Double, Float>();

	ITUGridUniformSignal signal = new ITUGridUniformSignal(40, 1.921e14, 100e9, inputPowerPerCh, 40);
	OpticalSignal inputSignal = signal.createSignal();

	for (OpticalChannel c : inputSignal.getChannels()) {
	    gainPerChannel.put(c.getFrequency(), gain);
	    nfPerChannel.put(c.getFrequency(), NF);
	}

	double nfM = Double.MAX_VALUE;
	double gfM = Double.MAX_VALUE;
	double osnrM = Double.MAX_VALUE;

	System.out.println("#Amps\tNF\tTilt\tOSNR");

	while (numberOfAmplifiers <= 20 && osnrM > 10.0) {
	    Amplifier[] amplifiers = new Amplifier[numberOfAmplifiers];
	    float[] linkLosses = new float[numberOfAmplifiers - 1];

	    for (int i = 0; i < amplifiers.length; i++) {
		if (i == amplifiers.length - 1) {
		    amplifiers[i] = new AmplifierVOA(inputPower, gain, gain + inputPower, NF, tilt, 0.0f,
			    AmplifierType.EDFA_1_STG);
		} else {
		    amplifiers[i] = new Amplifier(inputPower, gain, gain + inputPower, NF, tilt, 0.0f,
			    AmplifierType.EDFA_1_STG);
		    linkLosses[i] = gain;
		}

		amplifiers[i].setGainPerChannel(gainPerChannel);
		amplifiers[i].setNoiseFigurePerChannel(nfPerChannel);
	    }

	    BeckerNoiseFigureMetric nfMetric = new BeckerNoiseFigureMetric(linkLosses);
	    nfM = nfMetric.evaluate(amplifiers);

	    OSNRMetric osnrMetric = new OSNRMetric(inputSignal, linkLosses);
	    osnrM = osnrMetric.evaluate(amplifiers);

	    System.out.printf("%d\t%2.3f\t%2.3f\t%2.3f\n", numberOfAmplifiers, nfM, gfM, osnrM);
	    numberOfAmplifiers++;

	}

    }
}
