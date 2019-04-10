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
public class ACOPProblem_GainsTilt extends AbstractProblem {
    private int numberOfAmplifiers;
    private AmplifierType ampType;
    private static double MAX_VOA_ATT = 0.0f;
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

	solution.setVariable(0, new BinaryIntegerVariable(-20, 20)); // Tilt
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

	for (int i = 0; i < getNumberOfObjectives(); i++) {
	    if (r != null)
		f[i] = r[i];
	    else
		f[i] = Double.MAX_VALUE;
	}

	solution.setObjectives(f);
    }

    public static void main(String[] args) {
	SimulationSetup simSet = new SimSetPadTec(40, -21, 20, 20);
	
	SimulationParameters simParams = new SimulationParameters(40, -21, 20, simSet);

	ACOPProblem_GainsTilt problem = new ACOPProblem_GainsTilt(20, AmplifierType.EDFA_2_PadTec, simParams);

	int[] values = { 23, 27, 27, 27, 15, 7, 9, 0 };

	Solution solution = new Solution(8, 2);
	for (int i = 0; i < values.length; i++) {
	    if (i < 4) {
		solution.setVariable(i, new BinaryIntegerVariable(values[i], 17, 27));
	    } else {
		solution.setVariable(i, new BinaryIntegerVariable(values[i], 0, (int) MAX_VOA_ATT));
	    }
	}
	
	problem.evaluate(solution);
    }

}