package br.upe.simulations.JLT18;

import java.io.File;

import org.moeaframework.Executor;
import org.moeaframework.Instrumenter;
import org.moeaframework.algorithm.PeriodicAction.FrequencyType;
import org.moeaframework.analysis.collector.Accumulator;

import br.upe.MOO.modeling.ACOPProblem;
import br.upe.base.AmplifierType;

public class IGNTime {

    public static void main(String[] args) {
	AmplifierType type = AmplifierType.EDFA_1_PadTec;

	int numberOfAmplifiers = 2;

	int populationSize = 100;
	int numberOfGenerations = 300;

	Instrumenter instrumenter = new Instrumenter()
		.withProblemClass(ACOPProblem.class, numberOfAmplifiers, type).withFrequency(numberOfGenerations / 20)
		.withFrequencyType(FrequencyType.STEPS)
		.attachElapsedTimeCollector()
		.attachInvertedGenerationalDistanceCollector().withReferenceSet(new File("fb_e1_4a_pareto.txt"));


	new Executor().withProblemClass(ACOPProblem.class, numberOfAmplifiers, type).withAlgorithm("NSGAII")
		.withMaxEvaluations(populationSize * numberOfGenerations).withProperty("populationSize", populationSize)
		.withInstrumenter(instrumenter).run();

	Accumulator accumulator = instrumenter.getLastAccumulator();

	for (int i = 0; i < accumulator.size("NFE"); i++) {
	    System.out.println(accumulator.get("NFE", i) + "\t" + accumulator.get("Elapsed Time", i) + "\t"
		    + accumulator.get("InvertedGenerationalDistance", i));
	}
    }

}
