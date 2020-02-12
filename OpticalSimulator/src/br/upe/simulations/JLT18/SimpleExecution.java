package br.upe.simulations.JLT18;

import org.moeaframework.Executor;
import org.moeaframework.core.NondominatedPopulation;
import org.moeaframework.core.Solution;
import org.moeaframework.core.variable.EncodingUtils;

import com.sun.jmx.snmp.Timestamp;

import br.upe.MOO.modeling.ACOPProblem;
import br.upe.base.AmplifierType;

public class SimpleExecution {
    public static void main(String[] args) {

	int populationSize = 200;
	int numberOfGenerations = 1500;

	while (true) {
	    System.out.println(new Timestamp());
	    NondominatedPopulation result = new Executor()
		    .withProblemClass(ACOPProblem.class, 8,
			    AmplifierType.EDFA_1_PadTec)
		    .withAlgorithm("NSGAII")
		    .withMaxEvaluations(populationSize * numberOfGenerations).run();

	    System.out.println(new Timestamp());

	    if (result.size() <= 1)
		continue;

	    for (Solution solution : result) {
		System.out.format("%.4f\t%.4f\t|\t", solution.getObjective(0), (1.0 / solution.getObjective(1)));
		int[] x = EncodingUtils.getInt(solution);
		for (int i = 0; i < solution.getNumberOfVariables(); i++) {
		    System.out.print(x[i] + "\t");
		}
		System.out.println();
	    }

	    break;
	}
    }
}
