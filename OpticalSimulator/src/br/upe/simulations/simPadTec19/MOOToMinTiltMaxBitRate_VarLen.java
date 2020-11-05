package br.upe.simulations.simPadTec19;

import org.moeaframework.Executor;
import org.moeaframework.core.NondominatedPopulation;
import org.moeaframework.core.Solution;
import org.moeaframework.core.variable.EncodingUtils;

import br.upe.MOO.modeling.ACOPProblem_JustGains;
import br.upe.base.AmplifierType;
import br.upe.base.SimulationParameters;
import br.upe.simulations.simsetups.SimulationSetup;

public class MOOToMinTiltMaxBitRate_VarLen {
	public static void main(String[] args) {

		int populationSize = 50; // 60
		int numberOfGenerations = 10; // 500

		float chPower = -20.0f; // -20 dBm/ch = -4 dBm ;; -19 dBm/ch = -3 dBm
		int numberCh = 40;
		int numberAmps = 20;
		float loss = 19.0f;

		// Gerando as perdas de forma aleatória
		float[] losses = { 19.00f, 23.00f, 20.00f, 14.00f, 15.00f, 15.00f, 23.00f, 16.00f, 16.00f, 20.00f, 15.00f,
				15.00f, 20.00f, 18.00f, 16.00f, 18.00f, 15.00f, 19.00f, 23.00f };

		// float[] losses = { 17f, 21f, 18f, 23f, 20f, 20f, 19f, 24f, 24f, 17f,
		// 16f, 19f, 16f, 21f, 17f, 15f, 23f, 19f,
		// 23f };

		System.out.println("BitRate_SemPE_C2_NSGA");

		SimulationSetup simSet = new SimSetPadTec(numberCh, chPower, numberAmps, losses);

		SimulationParameters simParams = new SimulationParameters(numberCh, chPower, loss, simSet);

		int runs = 1;
		// System.out.println(new Timestamp());
		while (runs > 0) {
			NondominatedPopulation result = new Executor()
					.withProblemClass(ACOPProblem_JustGains.class, numberAmps,
							AmplifierType.EDFA_1_PadTec, simParams)
					.withAlgorithm("NSGAII")
					.withProperty("populationSize", populationSize)
					.withMaxEvaluations(populationSize * numberOfGenerations).distributeOnAllCores().run();

			if (result.size() < 1)
				continue;

			for (Solution solution : result) {
				System.out.format("%.4f\t%.4f\t%.4f\t|\t", solution.getAttribute("tilt"),
						solution.getAttribute("bitrate"), solution.getAttribute("ripple"));
				int[] x = EncodingUtils.getInt(solution);

				for (int i = 0; i < solution.getNumberOfVariables(); i++) {
					System.out.print(x[i] + "\t");
				}

				System.out.println();
			}

			runs--;
		}
		// System.out.println(new Timestamp());
	}
}
