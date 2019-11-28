package br.upe.simulations.simPadTec19;

import org.moeaframework.Analyzer;
import org.moeaframework.Executor;

import br.upe.MOO.modeling.ACOPProblem_JustGains;
import br.upe.base.AmplifierType;
import br.upe.base.SimulationParameters;
import br.upe.simulations.simsetups.SimulationSetup;

public class MOOScaleAnalysis {

    public static void main(String[] args) {
	int populationSize = 150; // 60
	// int numberOfGenerations = 500; // 500

	float chPower = -20.0f; // -20 dBm/ch = -4 dBm ;; -19 dBm/ch = -3 dBm
	int numberCh = 40;
	int numberAmps = 20;
	float loss = 20.0f;

	// Gerando as perdas de forma aleatória
	// float[] losses = { 19.00f, 23.00f, 20.00f, 14.00f, 15.00f, 15.00f,
	// 23.00f, 16.00f, 16.00f, 20.00f, 15.00f,
	// 15.00f, 20.00f, 18.00f, 16.00f, 18.00f, 15.00f, 19.00f, 23.00f };
	
	float[] losses = { 17f, 21f, 18f, 23f, 20f, 20f, 19f, 24f, 24f, 17f, 16f, 19f, 16f, 21f, 17f, 15f, 23f, 19f,
		23f };

	String label = "BitRate_SemPE_C1_MOO.txt";
	System.out.println(label);

	SimulationSetup simSet = new SimSetPadTec(numberCh, chPower, numberAmps, losses);

	SimulationParameters simParams = new SimulationParameters(numberCh, chPower, loss, simSet);

	// setup the experiment
	Executor executor = new Executor().withProblemClass(ACOPProblem_JustGains.class, numberAmps,
		AmplifierType.EDFA_1_PadTec, simParams);

	double[] refPoint = new double[2];
	String[] simCase = label.split("_");

	if (simCase[1].compareToIgnoreCase("ComPE") == 0 && simCase[2].compareToIgnoreCase("C1") == 0) {
	    refPoint[0] = 0.0999;
	    refPoint[1] = 0.0025;
	}
	else if (simCase[1].compareToIgnoreCase("ComPE") == 0 && simCase[2].compareToIgnoreCase("C2") == 0) {
	    refPoint[0] = 0.0996;
	    refPoint[1] = 0.005;
	} else if (simCase[1].compareToIgnoreCase("SemPE") == 0 && simCase[2].compareToIgnoreCase("C1") == 0) {
	    refPoint[0] = 0.0998;
	    refPoint[1] = 0.01;
	} else if (simCase[1].compareToIgnoreCase("SemPE") == 0 && simCase[2].compareToIgnoreCase("C2") == 0) {
	    refPoint[0] = 7.8936;
	    refPoint[1] = 0.00125;
	}

	// System.out.println(refPoint[0] + "\t" + refPoint[1]);

	Analyzer analyzer = new Analyzer()
		.withProblemClass(ACOPProblem_JustGains.class, numberAmps,
			AmplifierType.EDFA_1_PadTec, simParams)
		.includeHypervolume().showStatisticalSignificance().withReferencePoint(refPoint);

	// run each algorithm for 50 seeds
	for (int i = 500; i <= 1000; i += 100) {
	    String runName = "Run_" + i;
	    executor.withAlgorithm("NSGAII").withMaxEvaluations(populationSize * i);
	    analyzer.addAll(runName, executor.distributeOn(3).runSeeds(10));
	}

	// print the results
	analyzer.printAnalysis();
    }


}
