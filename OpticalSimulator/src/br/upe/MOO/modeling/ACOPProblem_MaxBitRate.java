package br.upe.MOO.modeling;

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
public class ACOPProblem_MaxBitRate extends AbstractProblem {
    private int numberOfAmplifiers;
    private AmplifierType ampType;
    private static double MAX_VOA_ATT = 0.0f;
    private SimulationParameters simParams;

    /**
     * Constructs a new instance of the ACOPProblem function, defining it to
     * include number of amplifier decision variables and 2 objectives.
     */
    public ACOPProblem_MaxBitRate(int numberOfAmplifiers, AmplifierType type, SimulationParameters parameters) {
	super(numberOfAmplifiers, 1);
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

	for (int i = 0; i < getNumberOfVariables(); i++) {
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

	ACOP_MOOProblem problem = new ACOP_MOOProblem(ampType, numberOfAmplifiers, simParams);

	float[] gains = new float[numberOfAmplifiers];
	for (int i = 0; i < gains.length; i++) {
	    gains[i] = x[i];
	}

	double[] r = problem.evaluateJustGains(gains);

	if (r == null)
	    f[0] = Double.MAX_VALUE;
	else if (r[2] > 20) // Se ripple maior que 20 dB
	    f[0] = r[3] + r[2]; // Piora o BitRate (minimização)
	else
	    f[0] = r[3];

	if (r != null) {
	    solution.setAttribute("tilt", r[0]);
	    solution.setAttribute("minOSNR", -1 * r[1]);
	    solution.setAttribute("ripple", r[2]);
	    solution.setAttribute("bitrate", 1 / r[3]);
	}

	// System.out.format("%.4f\t%.4f\t%.4f\t%.4f\n", r[0], -1 * r[1], 1 /
	// r[3], r[2]);

	solution.setObjectives(f);
    }

    public static void main(String[] args) {
	float chPower = -20.0f; // -20 dBm/ch = -4 dBm ;; -19 dBm/ch = -3 dBm
	int numberCh = 40;
	int numberAmps = 20;
	float loss = 20.0f;

	// Gerando as perdas de forma aleatória
	float[] losses = { 17f, 21f, 18f, 23f, 20f, 20f, 19f, 24f, 24f, 17f, 16f, 19f, 16f, 21f, 17f, 15f, 23f, 19f,
		23f };

	// float[] losses = { 19f, 23f, 20f, 14f, 15f, 15f, 23f, 16f, 16f, 20f,
	// 15f, 15f, 20f, 18f, 16f, 18f, 15f, 19f,
	// 23f };

	SimulationSetup simSet = new SimSetPadTec(numberCh, chPower, numberAmps, losses);

	SimulationParameters simParams = new SimulationParameters(numberCh, chPower, loss, simSet);

	ACOPProblem_MaxBitRate problem = new ACOPProblem_MaxBitRate(simSet.getNumberOfAmplifiers(),
		AmplifierType.EDFA_1_PadTec, simParams);


	int[][] valuesMatrix = {
		{ 16, 21, 22, 20, 17, 23, 23, 21, 23, 24, 16, 18, 15, 20, 16, 18, 18, 23, 20, 20 },
		{ 23, 17, 17, 20, 24, 23, 20, 19, 22, 19, 21, 17, 17, 20, 21, 15, 16, 23, 18, 23 },
		{ 20, 18, 20, 22, 22, 19, 23, 19, 23, 23, 15, 16, 20, 17, 21, 14, 20, 21, 20, 23 },
		{ 21, 20, 21, 16, 23, 20, 18, 24, 23, 20, 19, 19, 15, 19, 21, 18, 14, 21, 23, 23 },
		{ 22, 17, 17, 24, 22, 19, 21, 21, 23, 18, 21, 18, 16, 18, 19, 18, 17, 21, 23, 23 },
		{ 20, 19, 22, 17, 24, 20, 17, 23, 24, 21, 20, 16, 19, 15, 17, 20, 16, 23, 21, 20 },
		{ 18, 23, 19, 18, 21, 22, 20, 22, 23, 18, 19, 21, 17, 17, 21, 18, 14, 22, 22, 14 },
		{ 23, 16, 20, 21, 21, 23, 18, 21, 22, 24, 16, 17, 17, 17, 17, 20, 18, 24, 20, 21 },
		{ 19, 21, 19, 21, 20, 23, 20, 20, 23, 19, 19, 17, 22, 15, 18, 21, 14, 22, 22, 22 },
		{ 19, 20, 20, 22, 22, 21, 18, 21, 23, 20, 21, 16, 19, 16, 18, 18, 16, 21, 23, 24 },
		{ 23, 16, 18, 18, 24, 21, 20, 23, 24, 22, 17, 14, 22, 17, 17, 19, 16, 23, 19, 22 },
		{ 21, 18, 20, 18, 22, 22, 19, 23, 24, 19, 20, 16, 19, 18, 18, 18, 15, 22, 23, 23 },
		{ 21, 17, 19, 21, 21, 22, 21, 21, 24, 19, 14, 23, 16, 20, 19, 16, 18, 23, 19, 21 },
		{ 23, 17, 16, 19, 23, 21, 24, 20, 24, 23, 15, 18, 15, 20, 15, 20, 19, 22, 20, 22 },
		{ 18, 20, 21, 21, 23, 18, 19, 22, 24, 22, 16, 20, 17, 15, 23, 15, 17, 20, 22, 23 } };


	for (int i = 0; i < valuesMatrix.length; i++) {

	    int[] values = valuesMatrix[i];

	    Solution solution = new Solution(20, 1);
	    for (int j = 0; j < values.length; j++) {
		solution.setVariable(j, new BinaryIntegerVariable(values[j], 14, 24));
	    }

	    problem.evaluate(solution);
	}
    }

}