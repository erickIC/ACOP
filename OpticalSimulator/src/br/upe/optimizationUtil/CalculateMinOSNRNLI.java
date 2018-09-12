
package br.upe.optimizationUtil;

import br.upe.base.Amplifier;
import br.upe.metrics.GNLIMetric;
import br.upe.simulations.simsetups.SimulationSetup;

public class CalculateMinOSNRNLI extends CalculateFitness {

    @Override
    public double getFitness(OptimizationParameters parameters) {
	SimulationSetup simSet = parameters.getSimulationSetup();
	Amplifier[] amplifiers = heuristic.execute();
	double linkLength = simSet.getLINK_LOSSES()[0] * 1000 / 0.2;
	GNLIMetric gnliMetric = new GNLIMetric(28e9, 100e9, simSet.getCHANNELS(), simSet.getCHANNEL_POWER(),
		linkLength);
	gnliMetric.evaluate(amplifiers);
	
	return gnliMetric.worstOSNR_NLI();
    }
}
