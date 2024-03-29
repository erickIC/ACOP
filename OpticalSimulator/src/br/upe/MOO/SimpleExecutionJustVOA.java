package br.upe.MOO;

import org.moeaframework.Executor;
import org.moeaframework.core.NondominatedPopulation;
import org.moeaframework.core.Solution;
import org.moeaframework.core.variable.EncodingUtils;

import br.upe.MOO.modeling.ACOPProblem_JustVOA;
import br.upe.base.AmplifierType;
import br.upe.optimizationUtil.ACOP_LOCAL_PROBLEM;

public class SimpleExecutionJustVOA {
    public static void main(String[] args) {

	for (int run = 0; run < 100; run++) {

	    NondominatedPopulation result = new Executor().withProblemClass(ACOPProblem_JustVOA.class, 4,
		    AmplifierType.EDFA_1_PadTec, ACOP_LOCAL_PROBLEM.AdGC).withAlgorithm("NSGAII")
		    .withMaxEvaluations(10000).run();

	    for (Solution solution : result) {
		System.out.format("%.4f\t%.4f |\t", solution.getObjective(0), (1.0 / solution.getObjective(1)));
		int[] x = EncodingUtils.getInt(solution);
		for (int i = 0; i < solution.getNumberOfVariables(); i++) {
		    System.out.print(x[i] + "\t");
		}
		System.out.println();
	    }

	}
    }
}
