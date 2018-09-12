package br.upe.metrics;

import br.upe.base.Amplifier;

public class SimpleFlatnessMetric implements Metric {

	@Override
	public double evaluate(Amplifier[] link) {
		float sum = 0;
		
		for (int i = 0; i < link.length; i++) {
			sum += link[i].getFlatness();
		}
		
		return sum;
	}

}
