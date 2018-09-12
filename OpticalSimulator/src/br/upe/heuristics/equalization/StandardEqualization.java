package br.upe.heuristics.equalization;

import br.upe.base.EqualizationHeuristic;
import br.upe.base.OpticalChannel;
import br.upe.base.OpticalSignal;
import br.upe.base.ROADM;
import br.upe.util.DecibelConverter;

public class StandardEqualization implements EqualizationHeuristic {

    @Override
    public OpticalSignal equalizeSignal(ROADM roadm, OpticalSignal signal) {
	OpticalSignal result = signal.clone();
	double minPower = Double.MAX_VALUE;
	for (OpticalChannel c : result.getChannels()) {
	    // Signal Gain
	    double signalLin = DecibelConverter.toLinearScale(c.getSignalPower());

	    if (signalLin < minPower)
		minPower = signalLin;
	}

	for (OpticalChannel c : result.getChannels()) {
	    // Signal Gain
	    double signalLin = DecibelConverter.toLinearScale(c.getSignalPower());

	    double factor = minPower / signalLin;

	    roadm.getVoaAttenuation().put(c.getFrequency(), DecibelConverter.toDecibelScale(factor));
	}

	return roadm.transferFunction(signal);

    }

}
