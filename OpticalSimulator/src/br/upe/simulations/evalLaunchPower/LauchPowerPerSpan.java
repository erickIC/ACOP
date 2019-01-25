package br.upe.simulations.evalLaunchPower;

import java.util.ArrayList;

import org.moeaframework.Executor;
import org.moeaframework.core.NondominatedPopulation;
import org.moeaframework.core.Solution;
import org.moeaframework.core.variable.EncodingUtils;

import br.upe.MOO.modeling.ACOPProblem;
import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.AmplifierVOA;
import br.upe.optimizationUtil.ACOP_MOOProblem;

/***
 * Gerar 30 soluções com melhor OSNR Extrair potência de lançamento de cada span
 * Plotar gráfico: potência de lançamento vs. Posição span Fazer para 3 e
 * repetir para 5 e 7 amps
 * 
 * @author Erick
 *
 */
public class LauchPowerPerSpan {
    public static void main(String[] args) {

	int populationSize = 200;
	int numberOfGenerations = 1500;
	AmplifierType ampType = AmplifierType.EDFA_1_PadTec;
	int[] vNumberOfAmplifiers = { 8, 10 };
	int numberSolutions = 5;

	for (int a = 0; a < vNumberOfAmplifiers.length; a++) {

	    int numberOfAmplifiers = vNumberOfAmplifiers[a];
	    ArrayList<Solution> solutionsMaxOSNR = new ArrayList<>();
	    while (solutionsMaxOSNR.size() < numberSolutions) {
		NondominatedPopulation result = new Executor()
			.withProblemClass(ACOPProblem.class, numberOfAmplifiers, ampType).withAlgorithm("NSGAII")
			.withMaxEvaluations(populationSize * numberOfGenerations).run();

		if (result.size() <= 1)
		    continue;

		double maxOSNR = Double.MIN_VALUE;
		Solution solMaxOSNR = null;
		for (Solution solution : result) {
		    if (maxOSNR < (1.0 / solution.getObjective(1))) {
			maxOSNR = (1.0 / solution.getObjective(1));
			solMaxOSNR = solution;
		    }
		}

		solutionsMaxOSNR.add(solMaxOSNR);
	    }

	    double[][] launchPower = new double[numberOfAmplifiers][numberSolutions];

	    int j = 0;
	    for (Solution solution : solutionsMaxOSNR) {

		ACOP_MOOProblem problem = new ACOP_MOOProblem(ampType, numberOfAmplifiers);

		float[] gains = new float[numberOfAmplifiers];
		float[] attenuations = new float[numberOfAmplifiers];

		int[] x = EncodingUtils.getInt(solution);
		for (int i = 0; i < attenuations.length; i++) {
		    gains[i] = x[i];
		    attenuations[i] = x[i + numberOfAmplifiers];
		}

		problem.evaluate(gains, attenuations);

		Amplifier[] amplifiers = problem.getAmplifiers();

		for (int i = 0; i < amplifiers.length; i++) {
		    launchPower[i][j] = ((AmplifierVOA) amplifiers[i]).getOutputPowerAfterVOA();
		}
		j++;

		/*System.out.format("%.4f\t%.4f\t|\t", solution.getObjective(0), (1.0 / solution.getObjective(1)));
		for (int i = 0; i < solution.getNumberOfVariables(); i++) {
		    System.out.print(x[i] + "\t");
		}
		System.out.println();*/

	    }

	    for (int i = 0; i < launchPower.length; i++) {
		for (j = 0; j < launchPower[i].length; j++) {
		    System.out.format("%.4f\t", launchPower[i][j]);
		}
		System.out.println();
	    }
	    System.out.println("***\t" + vNumberOfAmplifiers[a] + " Amplifiers ***");
	}
    }
}
