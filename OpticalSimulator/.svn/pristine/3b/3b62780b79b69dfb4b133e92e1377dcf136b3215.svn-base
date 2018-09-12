package br.upe.metrics;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierVOA;
import br.upe.util.DecibelConverter;

public class BeckerNoiseFigureMetric implements Metric {

	private float linkLosses[];
	private float voaAttenuation;

	public BeckerNoiseFigureMetric(float[] linkLosses){
		this.linkLosses = linkLosses;
		this.voaAttenuation = 0;
	}

	@Override
	public double evaluate(Amplifier[] link) {
		return evaluate(link, this.linkLosses);
	}
	
	public double evaluate(Amplifier[] link, float linkLosses[]) {
		//Following that equation: F(total) = F(0) + F(1)*L0/G0 + F(2)*L0*L1/G0*G1 + ... + F(n)/G0*..*Gn-1
		double sum = 0;
		double ganhoAcum = 1;
		
		for (int i = 0; i < link.length; i++) {
			
			if(i>0){
				ganhoAcum *= DecibelConverter.toLinearScale(link[i-1].getGain());
				
				if(link[i-1] instanceof AmplifierVOA){
					ganhoAcum *= DecibelConverter.toLinearScale(-1*((AmplifierVOA) link[i-1]).getVoaOutAttenuation());
				}
				
				ganhoAcum *= (1.0/DecibelConverter.toLinearScale(linkLosses[i-1]));
			}
			
			if(link[i] instanceof AmplifierVOA)
				ganhoAcum *= DecibelConverter.toLinearScale(-1*((AmplifierVOA)link[i]).getVoaInAttenuation());

			double noiseFactor = DecibelConverter.toLinearScale(link[i].getNoiseFigure());
			
			sum += (noiseFactor/ganhoAcum);
		}
		
		//Adding the shot noise due to the VOA in the end of the link.
		// L0*L1/G0*G1 ... *GN
		ganhoAcum *= DecibelConverter.toLinearScale(link[link.length-1].getGain());
		ganhoAcum *= DecibelConverter.toLinearScale(-1*((AmplifierVOA) link[link.length-1]).getVoaOutAttenuation());
		sum += 1/ganhoAcum;
				
		return DecibelConverter.toDecibelScale(sum);
	}

	/**
	 * @return the voaAttenuation
	 */
	private float getVoaAttenuation() {
		return voaAttenuation;
	}

	/**
	 * @param voaAttenuation the voaAttenuation to set
	 */
	public void setVoaAttenuation(float voaAttenuation) {
		this.voaAttenuation = voaAttenuation;
	}

}
