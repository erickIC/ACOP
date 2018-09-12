package br.upe.metrics;

import br.upe.base.Amplifier;
import br.upe.base.OpticalChannel;
import br.upe.base.OpticalSignal;
import br.upe.util.DecibelConverter;

public class TiltMetric implements Metric {
	private OpticalSignal signal;
	private float[] linkLosses;
	
	public TiltMetric(OpticalSignal signal, float[] linkLosses) {
		super();
		this.signal = signal;
		this.linkLosses = linkLosses;
	}	
	
	@Override
	public double evaluate(Amplifier[] link) {
		for(int i=0; i<link.length; i++){
			link[i].transferFunction(signal);
			
			if(i < link.length-1)
				linkTrasferFunction(linkLosses[i]);
		}
				
		return calculateTilt();
	}

	private void linkTrasferFunction(float linkLoss) {
		for(OpticalChannel c : signal.getChannels()){
			//Signal Total Gain
			double signalLin = DecibelConverter.toLinearScale(c.getSignalPower());
			signalLin *= DecibelConverter.toLinearScale(-1*linkLoss);			
			//Noise Gain
			double noiseLin = DecibelConverter.toLinearScale(c.getNoisePower());
			noiseLin *= DecibelConverter.toLinearScale(-1*linkLoss);
						
			c.setSignalPower(DecibelConverter.toDecibelScale(signalLin));
			c.setNoisePower(DecibelConverter.toDecibelScale(noiseLin));
		}
	}

	private double calculateTilt() {
		double maxPeak = Double.MIN_VALUE;
		double minPeak = Double.MAX_VALUE;
		
		for(OpticalChannel c : signal.getChannels()){
			double signalLin = DecibelConverter.toLinearScale(c.getSignalPower());
			
			if(signalLin > maxPeak){
				maxPeak = signalLin;
			}
			if(signalLin < minPeak){
				minPeak = signalLin;
			}
		}
		
		return DecibelConverter.toDecibelScale(maxPeak-minPeak);
	}
	

}
