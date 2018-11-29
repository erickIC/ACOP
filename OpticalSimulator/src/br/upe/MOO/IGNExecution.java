package br.upe.MOO;

import java.io.File;

import org.apache.commons.math3.stat.descriptive.moment.Mean;
import org.apache.commons.math3.stat.descriptive.moment.StandardDeviation;
import org.moeaframework.Analyzer;
import org.moeaframework.Executor;

import br.upe.MOO.modeling.ACOPProblem;
import br.upe.base.AmplifierType;

public class IGNExecution {

    public static void main(String[] args) {

	String[] files = { "e1_2a", "e1_3a", "e1_4a", "e2_2a", "e2_3a", "e2_4a" };

	int populationSize = 100;
	int numberOfGenerations = 300;

	for (int i = 0; i < files.length; i++) {
	    AmplifierType type = AmplifierType.EDFA_1_PadTec;
	    int numberOfAmplifiers = 2;

	    String[] infos = files[i].split("_");
	    if (infos[0].equals("e2"))
		type = AmplifierType.EDFA_2_PadTec;

	    if (infos[1].equals("3a"))
		numberOfAmplifiers = 3;
	    else if (infos[1].equals("4a"))
		numberOfAmplifiers = 4;

	    // setup the experiment
	    Executor executor = new Executor().withProblemClass(ACOPProblem.class, numberOfAmplifiers, type)
		    .withMaxEvaluations(populationSize * numberOfGenerations);

	    File referenceSetFile = new File("fb_" + files[i] + "_pareto.txt");
	    Analyzer analyzer = new Analyzer().withProblemClass(ACOPProblem.class, numberOfAmplifiers, type)
		    .includeInvertedGenerationalDistance().withReferenceSet(referenceSetFile);

	    // run each algorithm for 50 seeds
	    String algorithm = "NSGAII";
	    analyzer.addAll(algorithm, executor.withAlgorithm(algorithm).runSeeds(50));
	    analyzer.showStatistic(new Mean());
	    analyzer.showStatistic(new StandardDeviation());

	    System.out.println(files[i]);
	    // print the results
	    analyzer.printAnalysis();

	}
    }

}
