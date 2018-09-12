package br.upe.metrics;

import br.upe.base.Amplifier;

public class CascadeNoiseFigureMetric implements Metric {

	@Override
	public double evaluate(Amplifier[] link) {
		//Following that equation: F(total) = F(0) + F(1)/G0 + F(2)/G0*G1 + ... + F(n)/G0*..*Gn-1
		float sum = 0;

		for (int i = 0; i < link.length; i++) {
			float factor = 1;
			for(int j=i-1; j>=0; j--){
				factor *= link[j].getGain();
			}

			double noiseFactor = Math.pow(10, (link[i].getNoiseFigure()/10));
			sum += (noiseFactor/factor);
		}

		return 10*Math.log10(sum);
	}

}
