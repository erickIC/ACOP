
package br.upe.optimizationUtil;

import br.upe.base.Amplifier;
import br.upe.base.OpticalSignal;

public class CalculateRipple extends CalculateFitness {

    @Override
    public double getFitness(OptimizationParameters parameters) {
	Amplifier[] amplifiers = heuristic.execute();
	OpticalSignal outputSignal = heuristic.getMonitors()[amplifiers.length - 1].getOutputSignal();
	
	return heuristic.calculateTilt(outputSignal);
    }
}
