package br.upe.simulations.simPadTec19;

import org.moeaframework.Executor;
import org.moeaframework.core.NondominatedPopulation;
import org.moeaframework.core.Solution;
import org.moeaframework.core.variable.EncodingUtils;

import com.sun.jmx.snmp.Timestamp;

import br.upe.MOO.modeling.ACOPProblem_GainsTilt_BitRate;
import br.upe.base.AmplifierType;
import br.upe.base.SimulationParameters;
import br.upe.simulations.simsetups.SimulationSetup;

public class MOOToMinTilt_PreTilt {
    public static void main(String[] args) {

	int populationSize = 150; // 60
	int numberOfGenerations = 500; // 500

	float chPower = -20.0f; // -20 dBm/ch = -4 dBm ;; -19 dBm/ch = -3 dBm
	int numberCh = 40;
	int numberAmps = 20;
	float loss = 20.0f;

	System.out.println("-4dBm_loss20_bitrate");

	SimulationSetup simSet = new SimSetPadTec(numberCh, chPower, numberAmps, loss);

	SimulationParameters simParams = new SimulationParameters(numberCh, chPower, loss, simSet);

	while (true) {
	    System.out.println(new Timestamp());
	    NondominatedPopulation result = new Executor()
		    .withProblemClass(ACOPProblem_GainsTilt_BitRate.class, numberAmps,
			    AmplifierType.EDFA_1_PadTec, simParams)
		    .withAlgorithm("NSGAII")
		    .withProperty("populationSize", populationSize)
		    .withMaxEvaluations(populationSize * numberOfGenerations).run();

	    if (result.size() <= 1)
		continue;

	    for (Solution solution : result) {
		System.out.format("%.4f\t%.4f\t|\t", (solution.getObjective(0)),
			(-1.0 * solution.getObjective(1)));
		int[] x = EncodingUtils.getInt(solution);

		System.out.print(x[0] + "\t"); // InputTilt

		float[] gains = new float[x.length];
		for (int i = 1; i < solution.getNumberOfVariables(); i++) {
		    System.out.print(x[i] + "\t");
		    gains[i] = (float) x[i];
		}

		/*// Verify Pout > 21 dBm
		BruteForceInitialization bfIni = new BruteForceInitialization(AmplifierType.EDFA_1_PadTec, false,
			Float.MAX_VALUE);
		bfIni.setGains(gains);
		
		ObjectiveFunction function = new LinearInterpolationFunction();
		PowerMaskSignal signal = new PowerMaskSignal(simSet.getCHANNELS(), AmplifierType.EDFA_1_PadTec,
			simSet.getCHANNEL_POWER(),
			40);
		OpticalSignal inputSignal = signal.createSignal();
		
		Amplifier[] amplifiers = bfIni.initialize(numberAmps, inputSignal.getTotalPower(), 0,
			simSet.getLINK_LOSSES(),
			function, inputSignal);
		
		for (int i = 0; i < amplifiers.length; i++) {
		    if (amplifiers[i].getOutputPower() > 21.0f) {
			System.out.print("\tTrue");
			break;
		    }
		}*/
		
		System.out.println();
	    }

	    break;
	}
    }
}
