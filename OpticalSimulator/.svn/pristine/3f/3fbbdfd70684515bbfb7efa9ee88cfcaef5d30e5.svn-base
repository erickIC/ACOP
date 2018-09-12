package br.teste.upe;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.AmplifierVOA;
import br.upe.base.OpticalSignal;
import br.upe.metrics.Metric;
import br.upe.metrics.OSNRMetric;
import br.upe.signal.factory.ITUGridUniformSignal;

public class OSNRCalculationTest {
	public static void main(String[] args) {
		int numberOfAmplifiers = 3;
		Amplifier[] amplifiers = new Amplifier[numberOfAmplifiers];
		AmplifierVOA[] amplifiersVOA = new AmplifierVOA[numberOfAmplifiers];
		float[] linkLosses = new float[numberOfAmplifiers-1];

		for(int i=0; i<numberOfAmplifiers; i++){
			amplifiers[i] = new Amplifier(0, 18, AmplifierType.B21_L24);
			amplifiers[i].setNoiseFigure(6);

			amplifiersVOA[i] = new AmplifierVOA(0, 18, AmplifierType.B21_L24);
			amplifiersVOA[i].setNoiseFigure(6);
			amplifiersVOA[i].setVoaInAttenuation(1);
			amplifiersVOA[i].setVoaOutAttenuation(1);
			amplifiersVOA[i].setGain(18);
			
			if(i < numberOfAmplifiers-1)
				linkLosses[i] = 18f;
		}

		ITUGridUniformSignal signal = new ITUGridUniformSignal(1, 1.921e14, 50e9, -17.53, 33.84);
		OpticalSignal inputSignal1 = signal.createSignal();
		OpticalSignal inputSignal2 = signal.createSignal();

		Metric metric = new OSNRMetric(inputSignal1, linkLosses);
		System.out.println("Sem VOA = " + metric.evaluate(amplifiers));
		metric = new OSNRMetric(inputSignal2, linkLosses);
		System.out.println("Com VOA = " + metric.evaluate(amplifiersVOA));
	}
}
