package ACOP;

import org.moeaframework.core.Solution;
import org.moeaframework.core.variable.BinaryIntegerVariable;
import org.moeaframework.core.variable.EncodingUtils;
import org.moeaframework.problem.AbstractProblem;

import br.upe.base.AmplifierType;
import br.upe.mascara.PowerMask;
import br.upe.mascara.PowerMaskFactory;
import br.upe.optimizationUtil.ACOP_MOOProblem;

/**
 * Implementation of the ACOP function.
 */
public class ACOPProblem extends AbstractProblem {
    private int numberOfAmplifiers;
    private AmplifierType ampType;
    private static double MAX_VOA_ATT = 20.0f;

    /**
     * Constructs a new instance of the ACOPProblem function, defining it to
     * include 2*number of amplifier decision variables and 2 objectives.
     */
    public ACOPProblem(int numberOfAmplifiers, AmplifierType type) {
	super(numberOfAmplifiers, 2);
	this.numberOfAmplifiers = numberOfAmplifiers;
	this.ampType = type;
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
	    if (i < numberOfAmplifiers) {
		solution.setVariable(i, new BinaryIntegerVariable(pm.getMinGain(), pm.getMaxGain()));
	    } else {
		solution.setVariable(i, new BinaryIntegerVariable(0, (int) MAX_VOA_ATT));
	    }
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

	ACOP_MOOProblem problem = new ACOP_MOOProblem(ampType, numberOfAmplifiers);

	float[] gains = new float[numberOfAmplifiers];
	float[] attenuations = new float[numberOfAmplifiers];

	for (int i = 0; i < attenuations.length; i++) {
	    gains[i] = x[i];
	    attenuations[i] = x[i + numberOfAmplifiers];
	}

	double[] r = problem.evaluate(gains, attenuations);

	for (int i = 0; i < getNumberOfObjectives(); i++) {
	    if (r != null)
		f[i] = r[i];
	    else
		f[i] = Double.MAX_VALUE;
	}

	solution.setObjectives(f);
    }

}