package br.upe.simulations.simPadTec19;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

import org.moeaframework.Executor;
import org.moeaframework.core.NondominatedPopulation;
import org.moeaframework.core.Solution;
import org.moeaframework.core.variable.EncodingUtils;

import br.upe.MOO.modeling.ACOPProblem_MaxBitRate_PE;
import br.upe.base.AmplifierType;
import br.upe.base.SimulationParameters;
import br.upe.simulations.simsetups.SimulationSetup;

public class MaxBitRate_PreTilt_VarLen {
    public static void main(String[] args) {

	int populationSize = 150; // 60
	int numberOfGenerations = 500; // 500

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

	String label = "BitRate_ComPE_C2_GA";
	System.out.println(label);

	SimulationSetup simSet = new SimSetPadTec(numberCh, chPower, numberAmps, losses);

	SimulationParameters simParams = new SimulationParameters(numberCh, chPower, loss, simSet);

	int runs = 30;
	// System.out.println(new Timestamp());
	while (runs > 0) {

	    NondominatedPopulation result = new Executor()
		    .withProblemClass(ACOPProblem_MaxBitRate_PE.class, numberAmps,
			    AmplifierType.EDFA_1_PadTec, simParams)
		    .withAlgorithm("GA")
		    .withProperty("populationSize", populationSize)
		    .withMaxEvaluations(populationSize * numberOfGenerations).run();

	    if (result.size() < 1)
		continue;

	    FileWriter arq = null;
	    try {
		arq = new FileWriter(label, true);
	    } catch (IOException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	    }
	    PrintWriter gravarArq = new PrintWriter(arq);

	    for (Solution solution : result) {
		System.out.format("%.4f\t|\t", (1 / solution.getObjective(0)));
		gravarArq.printf("%.4f\t|\t", (1 / solution.getObjective(0)));

		int[] x = EncodingUtils.getInt(solution);

		System.out.print(x[0] + "\t"); // InputTilt
		gravarArq.print(x[0] + "\t"); // InputTilt

		float[] gains = new float[x.length];
		for (int i = 1; i < solution.getNumberOfVariables(); i++) {
		    System.out.print(x[i] + "\t");
		    gravarArq.printf(x[i] + "\t");
		    gains[i] = (float) x[i];
		}

		System.out.println();
		gravarArq.printf("\n");
	    }

	    try {
		arq.close();
	    } catch (IOException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	    }
	    runs--;
	}

	// System.out.println(new Timestamp());
    }
}
