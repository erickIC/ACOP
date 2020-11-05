package br.upe.MOO.modeling;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

import org.moeaframework.core.Solution;
import org.moeaframework.core.variable.BinaryIntegerVariable;
import org.moeaframework.core.variable.EncodingUtils;
import org.moeaframework.problem.AbstractProblem;

import br.upe.base.AmplifierType;
import br.upe.base.SimulationParameters;
import br.upe.mascara.PowerMask;
import br.upe.mascara.PowerMaskFactory;
import br.upe.optimizationUtil.ACOP_MOOProblem;
import br.upe.simulations.simPadTec19.SimSetPadTec;
import br.upe.simulations.simsetups.SimulationSetup;


/**
 * Implementation of the ACOP function.
 */
public class ACOPProblem_GainsTilt extends AbstractProblem {
	private int numberOfAmplifiers;
	private AmplifierType ampType;
	private static int MAX_VOA_ATT = 15;
	private SimulationParameters simParams;

	/**
	 * Constructs a new instance of the ACOPProblem function, defining it to
	 * include number of amplifier decision variables and 2 objectives.
	 */
	public ACOPProblem_GainsTilt(int numberOfAmplifiers, AmplifierType type, SimulationParameters parameters) {
		super(numberOfAmplifiers + 1, 2);
		this.numberOfAmplifiers = numberOfAmplifiers;
		this.ampType = type;
		this.simParams = parameters;
	}

	/**
	 * Constructs a new solution and defines the bounds of the decision
	 * variables.
	 */
	@Override
	public Solution newSolution() {
		Solution solution = new Solution(getNumberOfVariables(), getNumberOfObjectives());

		PowerMask pm = PowerMaskFactory.getInstance().fabricatePowerMask(ampType);

		solution.setVariable(0, new BinaryIntegerVariable(-MAX_VOA_ATT, MAX_VOA_ATT)); // Tilt
		for (int i = 1; i < getNumberOfVariables(); i++) {
			solution.setVariable(i, new BinaryIntegerVariable(pm.getMinGain(), pm.getMaxGain())); // Gains
		}

		return solution;
	}

	/**
	 * Extracts the decision variables from the solution, evaluates the
	 * function, and saves the resulting objective value back to the solution.
	 */
	@Override
	public void evaluate(Solution solution) {
		int[] x = EncodingUtils.getInt(solution);
		double[] f = new double[numberOfObjectives];

		ACOP_MOOProblem problem = new ACOP_MOOProblem(ampType, numberOfAmplifiers, simParams, x[0]);

		float[] gains = new float[numberOfAmplifiers];
		for (int i = 0; i < gains.length; i++) {
			gains[i] = x[i + 1];
		}

		double[] r = problem.evaluateJustGains(gains);

		// System.out.printf("%.4f\t%.4f\t%.1f\n", r[0], -1 * r[1], 1.0 / r[3]);

		if (r == null)
			f[0] = f[1] = Double.MAX_VALUE;
		else {
			f[0] = r[0];
			f[1] = r[3];
		}

		solution.setObjectives(f);
	}

	public static void main(String[] args) {
		float chPower = -20.0f; // -20 dBm/ch = -4 dBm ;; -19 dBm/ch = -3 dBm
		int numberCh = 40;
		int numberAmps = 20;
		float loss = 20.0f;

		// Gerando as perdas de forma aleatória
		// -4
		// float[] losses = { 17f, 21f, 18f, 23f, 20f, 20f, 19f, 24f, 24f, 17f,
		// 16f, 19f, 16f, 21f, 17f, 15f, 23f, 19f,
		// 23f };
		float[] losses = { 19f, 23f, 20f, 14f, 15f, 15f, 23f, 16f, 16f, 20f, 15f, 15f, 20f, 18f, 16f, 18f, 15f, 19f,
				23f };

		SimulationSetup simSet = new SimSetPadTec(numberCh, chPower, numberAmps, losses);

		SimulationParameters simParams = new SimulationParameters(numberCh, chPower, loss, simSet);

		ACOPProblem_GainsTilt problem = new ACOPProblem_GainsTilt(simSet.getNumberOfAmplifiers(),
				AmplifierType.EDFA_1_PadTec, simParams);

		ArrayList<Integer[]> valuesMatrix = new ArrayList<>();
		File file = new File("inputTemp.txt");
		Scanner reader;
		try {
			reader = new Scanner(file);
			while (reader.hasNextLine()) {
				String[] line = reader.nextLine().split("\t");
				Integer[] values = new Integer[line.length];

				for (int i = 0; i < values.length; i++) {
					values[i] = Integer.parseInt(line[i]);
				}

				valuesMatrix.add(values);
			}

			reader.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}


		for (int i = 0; i < valuesMatrix.size(); i++) {

			Integer[] values = valuesMatrix.get(i);

			Solution solution = new Solution(21, 2);
			solution.setVariable(0, new BinaryIntegerVariable(values[0], -20, 20));
			for (int j = 1; j < values.length; j++) {
				solution.setVariable(j, new BinaryIntegerVariable(values[j], 14, 24));
			}

			problem.evaluate(solution);
		}
	}

}