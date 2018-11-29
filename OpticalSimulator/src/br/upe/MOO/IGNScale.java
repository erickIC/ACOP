package br.upe.MOO;

import java.io.File;
import java.io.Serializable;

import org.moeaframework.Executor;
import org.moeaframework.Instrumenter;
import org.moeaframework.algorithm.PeriodicAction.FrequencyType;
import org.moeaframework.analysis.collector.Accumulator;

import br.upe.MOO.modeling.ACOPProblem;
import br.upe.base.AmplifierType;

public class IGNScale {

    public static void main(String[] args) {
	AmplifierType type = AmplifierType.EDFA_2_PadTec;

	int numberOfAmplifiers = 8;

	int populationSize = 250;
	int numberOfGenerations = 2000;

	Instrumenter instrumenter = new Instrumenter()
		.withProblemClass(ACOPProblem.class, numberOfAmplifiers, type).withFrequency(numberOfGenerations / 20)
		.withFrequencyType(FrequencyType.STEPS)
		.attachInvertedGenerationalDistanceCollector().withReferenceSet(new File("fb_e2_4a_pareto.txt"));

	int runMax = 50;
	Serializable[][] results = null;

	for (int run = 0; run < runMax; run++) {
	    new Executor().withProblemClass(ACOPProblem.class, numberOfAmplifiers, type).withAlgorithm("NSGAII")
		    .withMaxEvaluations(populationSize * numberOfGenerations)
		    .withProperty("populationSize", populationSize)
		    .withInstrumenter(instrumenter)
		    .run();

	    Accumulator accumulator = instrumenter.getLastAccumulator();

	    if (run == 0) {
		for (int i = 0; i < accumulator.size("NFE"); i++) {
		    System.out.print(accumulator.get("NFE", i) + "\t");
		}
		System.out.println();
		results = new Serializable[accumulator.size("NFE")][runMax];
	    }

	    for (int i = 0; i < results.length; i++) {
		results[i][run] = accumulator.get("InvertedGenerationalDistance", i);
	    }
	}

	for (int i = 0; i < results.length; i++) {
	    for (int j = 0; j < results[i].length; j++) {
		if (Double.isFinite((double) results[i][j]))
		    System.out.print(results[i][j] + "\t");
		else
		    System.out.print(" \t");
	    }
	    System.out.println();
	}
	System.out.println("***\t" + numberOfAmplifiers + " Amplifiers	****");
    }

}
