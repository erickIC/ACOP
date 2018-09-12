package br.upe.mascara;

import java.util.HashMap;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalChannel;
import br.upe.base.OpticalSignal;
import br.upe.metrics.GNLIMetric;
import br.upe.objfunctions.linerInterpolation.LinearInterpolationFunction;
import br.upe.signal.factory.PowerMaskSignal;

public class BuildMaskOSNR {

    public static void main(String[] args) {
	AmplifierType type = AmplifierType.EDFA_2_2_STG;

	ObjectiveFunction function = new LinearInterpolationFunction();
							 // // //
	System.out.println("-- NN --");

	int numberCh = 40;
	float pinSystem = -21.0f;
	float[] linLosses = { 20.0f };

	double linkLength = linLosses[0] * 1000 / 0.2;
	GNLIMetric gnliMetric = new GNLIMetric(28e9, 100e9, numberCh, pinSystem, linkLength);

	PowerMaskSignal signal = new PowerMaskSignal(numberCh, type, pinSystem, 30);
	OpticalSignal inputSignal = signal.createSignal();

	Amplifier[] amplifiers = new Amplifier[2];

	PowerMask pm = PowerMaskFactory.getInstance().fabricatePowerMask(type);
	
	amplifiers[0] = new Amplifier(inputSignal.getTotalPower(), type);
	amplifiers[0].setOutputPower(inputSignal.getTotalPower() + 22f);
	amplifiers[0].calculateGain();
	function.defineNewOperationPoint(amplifiers[0], inputSignal);
	
	HashMap<Double, Float> gainPerChannel = new HashMap<Double, Float>();
	HashMap<Double, Float> nfPerChannel = new HashMap<Double, Float>();
	for (int i = 0; i < inputSignal.getChannels().size(); i++) {
	    OpticalChannel channel = inputSignal.getChannels().get(i);

	    gainPerChannel.put(channel.getFrequency(), 0f);
	    nfPerChannel.put(channel.getFrequency(), 1f);
	}
	amplifiers[1] = new Amplifier(pinSystem, 0, pinSystem, 1, 0, 0, type);
	amplifiers[1].setGainPerChannel(gainPerChannel);
	amplifiers[1].setNoiseFigurePerChannel(nfPerChannel);

	gnliMetric.evaluate(amplifiers);
	System.out.println("OSNR_ASE\tOSNR_NLI");
	System.out.printf("%2.3f\t%2.3f", gnliMetric.worstOSNR_ASE(), gnliMetric.worstOSNR_NLI());

    }
}
