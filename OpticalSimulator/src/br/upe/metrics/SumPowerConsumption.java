package br.upe.metrics;

import br.upe.base.Amplifier;

public class SumPowerConsumption implements Metric {

	private double factor;
	
	/**
	 * 
	 * @param numberCh Number of channels considered.
	 * @param rateCh The channel rate in Gbps.
	 */
	public SumPowerConsumption(int numberCh, int rateCh){
		this.factor = 1;//numberCh*rateCh;
	}
	
	@Override
	public double evaluate(Amplifier[] link) {
		double powerSum = 0;
		
		for(int p=0; p<link.length; p++){
			powerSum += link[p].getPowerConsumption();
		}

		return (powerSum/factor);
	}
}
