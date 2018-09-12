package br.upe.objfunctions.maskOSNR;

import java.util.HashMap;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.AmplifierVOA;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalChannel;
import br.upe.base.OpticalSignal;
import br.upe.metrics.GNLIMetric;
import br.upe.objfunctions.linerInterpolation.LinearInterpolationFunction;
import br.upe.signal.factory.PowerMaskSignal;

public class MaskOSNRFunction extends ObjectiveFunction {

    private float linkLoss;
    private ObjectiveFunction function;
    private boolean worstCaseMask;

    public MaskOSNRFunction(ObjectiveFunction function, float linkLoss, boolean worstCaseMask) {
	this.linkLoss = 20.0f;// linkLoss;
	this.function = function;
	this.worstCaseMask = worstCaseMask;
    }

    @Override
    public void defineNewOperationPoint(Amplifier amplifier, OpticalSignal signal) {
	this.internalDefine(amplifier, signal);
    }

    private void internalDefine(Amplifier amplifier, OpticalSignal signal) {
	int numberCh = signal.getChannels().size();
	float pinSystem = (float) signal.getChannels().get(0).getSignalPower();
	float[] linLosses = { linkLoss };

	double linkLength = linLosses[0] * 1000 / 0.2;
	GNLIMetric gnliMetric = new GNLIMetric(28e9, 100e9, numberCh, pinSystem, linkLength);

	// Creating optical link with two amplifiers
	Amplifier[] amplifiers = new Amplifier[2];

	// The first amplifier is the one that will have its OSNR calculated
	amplifiers[0] = amplifier;
	if (worstCaseMask)
	    function.defineNewOperationPointWorstCase(amplifiers[0], signal);
	else
	    function.defineNewOperationPoint(amplifiers[0], signal);

	// The second amplifier is a dummy amplifier, just to use the IGN
	// without errors
	HashMap<Double, Float> gainPerChannel = new HashMap<Double, Float>();
	HashMap<Double, Float> nfPerChannel = new HashMap<Double, Float>();
	for (int i = 0; i < signal.getChannels().size(); i++) {
	    OpticalChannel channel = signal.getChannels().get(i);

	    gainPerChannel.put(channel.getFrequency(), 0f); // Dummy gain: 0 dB
	    nfPerChannel.put(channel.getFrequency(), 1f); // Dummy nf: 1 dB
	}
	amplifiers[1] = new Amplifier(pinSystem, 0, pinSystem, 1, 0, 0, amplifier.getType());
	amplifiers[1].setGainPerChannel(gainPerChannel);
	amplifiers[1].setNoiseFigurePerChannel(nfPerChannel);

	// Calling the IGN
	gnliMetric.evaluate(amplifiers);
	amplifier.setMaskOSNR((float) gnliMetric.worstOSNR_NLI());
    }

    @Override
    public Amplifier[] getAmplifiersCandidate(Amplifier amplifier, OpticalSignal signal, boolean useInput) {
	Amplifier[] candidates = function.getAmplifiersCandidate(amplifier, signal, useInput);
	
	for (int i = 0; i < candidates.length; i++) {
	    defineNewOperationPoint(candidates[i], signal);
	}
	
	return candidates;
    }

    @Override
    public void defineNewOperationPointWorstCase(Amplifier amplifier, OpticalSignal signal) {
	this.worstCaseMask = true;
	this.internalDefine(amplifier, signal);

    }

    public static void main(String[] args) {
	boolean worstCaseMask = true;
	float linkLoss = 20;
	LinearInterpolationFunction functionAux = new LinearInterpolationFunction();
	MaskOSNRFunction function = new MaskOSNRFunction(functionAux, linkLoss, worstCaseMask);

	Amplifier amplifier = new AmplifierVOA(-5, 15, AmplifierType.EDFA_1_PadTec);

	PowerMaskSignal signal = new PowerMaskSignal(40, AmplifierType.EDFA_1_PadTec, -21.0f, 30);
	OpticalSignal inputSignal = signal.createSignal();

	function.defineNewOperationPoint(amplifier, inputSignal);

	System.out.println();
    }

}
