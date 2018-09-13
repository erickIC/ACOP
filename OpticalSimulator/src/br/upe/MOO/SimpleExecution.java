package br.upe.MOO;

import org.moeaframework.Executor;
import org.moeaframework.core.NondominatedPopulation;
import org.moeaframework.core.Solution;
import org.moeaframework.core.variable.EncodingUtils;

import br.upe.MOO.modeling.ACOPProblem;
import br.upe.base.AmplifierType;

public class SimpleExecution {
    public static void main(String[] args) {

	for (int run = 0; run < 1; run++) {

	    NondominatedPopulation result = new Executor()
		    .withProblemClass(ACOPProblem.class, 4,
			    AmplifierType.EDFA_2_PadTec)
		    .withAlgorithm("NSGAII")
		    .withMaxEvaluations(10000).run();

	    for (Solution solution : result) {
		System.out.format("%.4f\t%.4f\t|\t", solution.getObjective(0), (1.0 / solution.getObjective(1)));
		int[] x = EncodingUtils.getInt(solution);
		for (int i = 0; i < solution.getNumberOfVariables(); i++) {
		    System.out.print(x[i] + "\t");
		}
		System.out.println();
	    }

	}
    }
}
