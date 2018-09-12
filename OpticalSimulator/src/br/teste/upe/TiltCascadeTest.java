package br.teste.upe;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.AmplifierVOA;
import br.upe.base.OpticalSignal;
import br.upe.metrics.MetricCalculator;
import br.upe.objfunctions.linerInterpolation.LinearInterpolationFunction;
import br.upe.signal.factory.ITUGridUniformSignal;
import br.upe.util.DecibelConverter;

public class TiltCascadeTest {
	public static void main(String[] args) {
		int numberOfAmplifiers = 3;
		Amplifier[] amplifiers = new Amplifier[numberOfAmplifiers];
		float[] linkLosses = new float[numberOfAmplifiers-1];
		LinearInterpolationFunction function = new LinearInterpolationFunction();

		float linkInputPower = DecibelConverter.calculateInputPower(40, -26.3f);

		// ITUGridLinearTiltedSignal signal = new ITUGridLinearTiltedSignal(40,
		// 1.92103e14, 100e9, -26.3f, 30, -10.0);
		ITUGridUniformSignal signal = new ITUGridUniformSignal(40, 1.92103e14, 100e9, -26.3f, 30);
		OpticalSignal inputSignal = signal.createSignal();
		
		int ganho = 30;

		for(int i=0; i<numberOfAmplifiers; i++){
			float inputPower;
			
			if(i==0)
				inputPower = linkInputPower;
			else
				inputPower = amplifiers[i-1].getOutputPower()-linkLosses[i-1];
			
			amplifiers[i] = new AmplifierVOA(inputPower, ganho, (inputPower + ganho), 0.0f, 0.0f, 0.0f,
					AmplifierType.EDFA_1_STG);
			function.defineNewOperationPoint(amplifiers[i], inputSignal);

			if(i < numberOfAmplifiers-1)
				linkLosses[i] = 30f;
		}

	
		MetricCalculator metric = new MetricCalculator(inputSignal, linkLosses);
		metric.evaluate(amplifiers);
		
		System.out.println("OSNR = " + metric.getOSNR());
		System.out.println("Tilt = " + metric.getTilt());
		
	}

}
