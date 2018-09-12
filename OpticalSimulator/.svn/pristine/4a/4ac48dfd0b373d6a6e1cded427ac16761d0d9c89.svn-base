package br.upe.heuristics.AsHB;

import br.upe.base.ACOPHeuristic;
import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.AmplifierVOA;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalSignal;
import br.upe.initializations.UniformInitialization;
import br.upe.mascara.PowerMask;
import br.upe.mascara.PowerMaskFactory;
import br.upe.metrics.BeckerNoiseFigureMetric;
import br.upe.objfunctions.linerInterpolation.LinearInterpolationFunction;
import br.upe.objfunctions.rn.util.NormalizationUtility;
import br.upe.objfunctions.rn.util.NormalizationUtilityFactory;
import br.upe.selection.UiaraWeightSelection;
import br.upe.signal.factory.PowerMaskSignal;
import br.upe.signal.tracker.AmplifierSignalMonitor;
import br.upe.simulations.simsetups.SimSetAMPVOA;
import br.upe.simulations.simsetups.SimulationSetup;

public class AsHBFlex extends ACOPHeuristic {	

    private double errorOutput = 0;
    private double errorInput = 0;

    private int maxIteration;
    private int currentIteration;


    /**
     * Complete constructor of this class
     * 
     * @param numberOfAmplifiers
     * @param linkInputPower
     *            Input power of the link
     * @param linkLosses
     *            The losses in each sub-link of the link
     * @param maxAmplifierOutPower
     *            The max output power allowed to the amplifiers
     * @param minAmplifierOutPower
     *            The min input power allowed to the amplifiers
     * @param localSearchFactor
     *            The size of the local search pass
     * @param learningRate
     *            The rate used in the backpropagation fase
     */
    public AsHBFlex(int numberOfAmplifiers, float[] linkLosses, OpticalSignal inputSignal, ObjectiveFunction function) {
	super(numberOfAmplifiers, linkLosses, inputSignal, function);
	monitors[0] = new AmplifierSignalMonitor();
	monitors[0].setInputSignal(inputSignal);
    }

    @Override
    public Amplifier[] execute() {
	this.amplifiers = initialization.initialize(numberOfAmplifiers, linkInputPower, linkOutputPower, linkLosses,
		function, monitors[0].getInputSignal());

	boolean outOfMask = false;

	currentIteration = 0;
	while (!isStabilized()) {

	    // Forward process.
	    // It isn't necessary to adjust the output power of the last
	    // amplifier.
	    for (int i = 0; i < numberOfAmplifiers; i++) {

		float currentOutputPower = 0;

		// Input power restriction
		if (i == 0) {
		    float outputPower = (float) (amplifiers[i].getOutputPower() - errorInput);
		    setGain(amplifiers[i], (outputPower - linkInputPower));
		    amplifiers[i].setInputPower(linkInputPower);
		}

		Amplifier[] candidates;
		if (amplifiers[i] instanceof AmplifierVOA) {
		    if (i + 1 == numberOfAmplifiers && !(amplifiers[0] instanceof AmplifierVOA)) {
			// The last amplifier has VOA but the others hasn't.
			// Then it is a VOA to the link, not to the AMP.
			candidates = function.getAmplifiersCandidate(amplifiers[i], monitors[i].getInputSignal(),
				maxOutputPower);
		    } else {
			candidates = function.getAmplifiersCandidate(amplifiers[i], monitors[i].getInputSignal());
		    }
		} else {
		    candidates = function.getAmplifiersCandidate(amplifiers[i], monitors[i].getInputSignal(),
			    maxOutputPower);
		}

		if (candidates.length == 0) {
		    PowerMask pm = PowerMaskFactory.getInstance().fabricatePowerMask(amplifiers[i].getType());

		    float maxInputPower = pm.getMaxTotalInputPower();

		    float difference = Math.abs(amplifiers[i].getInputPower() - maxInputPower);
		    if (difference == 0 || outOfMask) {
			difference = 0.1f;
			amplifiers[i].setInputPower(amplifiers[i].getInputPower() - difference);
			outOfMask = true;
		    } else {
			amplifiers[i].setInputPower(maxInputPower);
			outOfMask = false;
		    }

		    // if (difference < 0.5)
		    // continue;

		    amplifiers[i].setInputPower(maxInputPower);

		    if (amplifiers[i - 1] instanceof AmplifierVOA) {
			// Increase the voa attenuation of the previous
			// amplifier
			((AmplifierVOA) amplifiers[i - 1]).increaseVoaOutAttenuation(difference);

			// Use the amplifier to transform the signal
			// Save the output power of this amplifier
			monitors[i].setOutputSignal(amplifiers[i].transferFunction(monitors[i].getInputSignal()));

			updateNextAmplifier(i - 1);
			i--;
		    } else {
			for (int j = i - 1; j >= 0; j--) {
			    // Decrease the gain of the previous amplifier
			    // (decrease the gain)
			    float newGain = amplifiers[j].getGain() - difference;
			    PowerMask pm2 = PowerMaskFactory.getInstance().fabricatePowerMask(amplifiers[j].getType());

			    // If the decrease cannot be done in the previous
			    // amplifier, then try the previous amplifiers
			    if (newGain >= pm2.getMinGain()) {
				setGain(amplifiers[j], newGain);
				function.defineNewOperationPoint(amplifiers[j], monitors[j].getInputSignal());

				// Use the amplifier to transform the signal
				// Save the output power of this amplifier
				monitors[j]
					.setOutputSignal(amplifiers[j].transferFunction(monitors[j].getInputSignal()));

				updateNextAmplifier(j);
				i--;
				break;
			    }

			    i--;
			}
		    }

		    continue;
		}

		Amplifier referenceOption = selectionOp.select(candidates);

		if (amplifiers[i].getGain() == 0) {
		    currentOutputPower = amplifiers[i].getInputPower();
		    currentOutputPower += PowerMaskFactory.getInstance().fabricatePowerMask(amplifiers[i].getType())
			    .getMinGain();
		} else {
		    currentOutputPower = amplifiers[i].getOutputPower();
		}

		float step = getStepMagnitude(currentOutputPower, referenceOption.getOutputPower());

		float newOutputPower = currentOutputPower + step;

		// Setting the attenuation of the VOA according to the max
		// output power restriction
		if (amplifiers[i] instanceof AmplifierVOA && newOutputPower > maxOutputPower) {
		    ((AmplifierVOA) amplifiers[i]).setVoaOutAttenuation(newOutputPower - maxOutputPower);
		}

		// updating the gain of the current amplifier
		setGain(amplifiers[i], (newOutputPower - amplifiers[i].getInputPower()));
		function.defineNewOperationPoint(amplifiers[i], monitors[i].getInputSignal());
		// Use the amplifier to transform the signal
		// Save the output power of this amplifier
		monitors[i].setOutputSignal(amplifiers[i].transferFunction(monitors[i].getInputSignal()));

		if (i + 1 < numberOfAmplifiers) {
		    // updating the input power of the next amplifier
		    updateNextAmplifier(i);
		}
	    }

	    errorOutput = amplifiers[amplifiers.length - 1].getOutputPower()
		    - (linkOutputPower + voaMaxAttenuation + roadmAttenuation);

	   /* BeckerNoiseFigureMetric nfMetric = new BeckerNoiseFigureMetric(linkLosses);
	    OpticalSignal endSignal = monitors[amplifiers.length - 1].getOutputSignal();
	    System.out.printf("%2.3f\t%2.3f\t%2.3f\n", nfMetric.evaluate(amplifiers), calculateTilt(endSignal),
		    calculateOSNR(endSignal));

	    for (int i = 0; i < amplifiers.length; i++) {
		System.out.print(amplifiers[i] + " ");
	    }
	    System.out.println();*/

	    // Backward process.
	    // It isn't necessary to adjust the input power of the first
	    // amplifier.

	    for (int i = numberOfAmplifiers - 1; i > 0; i--) {
		float currentInputPower = 0;

		// USING VOA
		if (i == numberOfAmplifiers - 1) {
		    if (amplifiers[i].getOutputPower() < (linkOutputPower - roadmAttenuation)) {
			setGain(amplifiers[i], (linkOutputPower - amplifiers[i].getInputPower()));
		    } else if (amplifiers[i].getOutputPower() > linkOutputPower + voaMaxAttenuation
			    + roadmAttenuation) {
			setGain(amplifiers[i], (float) (linkOutputPower + voaMaxAttenuation + roadmAttenuation)
				- amplifiers[i].getInputPower());
		    }

		    // ***** NOVO IF PARA RESTRIÇÃO DE POTÊNCIA ****
		    if (amplifiers[i].getOutputPower() > maxOutputPower) {
			if (amplifiers[i] instanceof AmplifierVOA) {
			    float voaAttenuation = (float) (amplifiers[i].getOutputPower() - maxOutputPower);
			    ((AmplifierVOA) amplifiers[i]).setVoaOutAttenuation(voaAttenuation);
			} else
			    setGain(amplifiers[i], (maxOutputPower - amplifiers[i].getInputPower()));
		    }

		    float ampVoaAtt = ((AmplifierVOA) amplifiers[i]).getVoaOutAttenuation();
		    float voaAttenuation = (float) (amplifiers[i].getOutputPower() - ampVoaAtt - linkInputPower
			    - roadmAttenuation);
		    ((AmplifierVOA) amplifiers[i]).increaseVoaOutAttenuation(voaAttenuation);
		}

		if (currentIteration == maxIteration)
		    break;

		Amplifier[] candidates = function.getAmplifiersCandidate(amplifiers[i], monitors[i].getInputSignal(),
			false);

		if (candidates.length == 0) {

		}

		Amplifier referenceOption = selectionOp.select(candidates);

		currentInputPower = amplifiers[i].getInputPower();

		float step = getStepMagnitude(currentInputPower, referenceOption.getInputPower());

		setGain(amplifiers[i - 1], (amplifiers[i - 1].getGain() + step));

		if (i > 0) {
		    int j = i - 1;
		    function.defineNewOperationPoint(amplifiers[j], monitors[j].getInputSignal());
		    // Use the amplifier to transform the signal
		    // Save the output power of this amplifier
		    monitors[j].setOutputSignal(amplifiers[j].transferFunction(monitors[j].getInputSignal()));

		    updateNextAmplifier(j);
		}
	    }

	    errorInput = amplifiers[0].getInputPower() - linkInputPower;

/*	    if (currentIteration < maxIteration) {
		int j = amplifiers.length - 1;
		function.defineNewOperationPoint(amplifiers[j], monitors[j].getInputSignal());
		monitors[j].setOutputSignal(amplifiers[j].transferFunction(monitors[j].getInputSignal()));
		nfMetric = new BeckerNoiseFigureMetric(linkLosses);
		endSignal = monitors[j].getOutputSignal();
		System.out.printf("%2.3f\t%2.3f\t%2.3f\n", nfMetric.evaluate(amplifiers), calculateTilt(endSignal),
			calculateOSNR(endSignal));

		for (int i = 0; i < amplifiers.length; i++) {
		    System.out.print(amplifiers[i] + " ");
		}
		System.out.println("\n ------- ");
	    }*/
	}

	return amplifiers;
    }


    private float getStepMagnitude(float currentPower, float candidatePower) {
	float direction = candidatePower - currentPower;
	double temperature = currentIteration * 1.0 / maxIteration;
	double tempStep = Math.exp(-temperature) - Math.exp(-1);
	tempStep *= direction;

	return (float) tempStep;
    }

    private boolean isStabilized() {
	if (currentIteration < maxIteration) {
	    currentIteration++;
	    return false;
	}
	return true;
    }


    public void setMaxIteration(int maxIteration) {
	this.maxIteration = maxIteration;
    }

    /**
     * @param args
     */
    public static void main(String[] args) {
	AmplifierType type = AmplifierType.EDFA_1_STG;

	NormalizationUtility nu = NormalizationUtilityFactory.getInstance().fabricate(type);
	ObjectiveFunction function = new LinearInterpolationFunction(); // NNFunction(nu);
	System.out.println("-- LinearInterpolationFunction --");

	int numberCh = 39;
	SimulationSetup simSet = new SimSetAMPVOA(numberCh, -21f, 4.5f);
	float[] linLosses = simSet.getLINK_LOSSES();
	int numberAmplifiers = simSet.getNumberOfAmplifiers();

	BeckerNoiseFigureMetric nfMetric = new BeckerNoiseFigureMetric(linLosses);

	// Definindo ganho máximo
	float maxPout = simSet.getMaxOutputPower();
	System.out.println(maxPout);

	PowerMaskSignal signal = new PowerMaskSignal(numberCh, type, simSet.getCHANNEL_POWER(), 30);
	OpticalSignal inputSignal = signal.createSignal();

	ACOPHeuristic heuristic = new AsHBFlex(numberAmplifiers, linLosses, inputSignal, function);
	heuristic.setSelectionOp(new UiaraWeightSelection());
	heuristic.setInitialization(new UniformInitialization(type));
	heuristic.setVoaMaxAttenuation(simSet.getVOA_MAX_ATT());
	heuristic.setRoadmAttenuation(simSet.getROADM_ATT());
	heuristic.setMaxOutputPower(maxPout);
	((AsHBFlex) heuristic).setMaxIteration(5);
	Amplifier[] amplifiers = heuristic.execute();
	System.out.println("****** AsHB Flex ******");
	System.out.println("NF\tGF\tOSNR");
	OpticalSignal endSignal = heuristic.getMonitors()[numberAmplifiers - 1].getOutputSignal();
	System.out.printf("%2.3f\t%2.3f\t%2.3f\n", nfMetric.evaluate(amplifiers), heuristic.calculateTilt(endSignal),
		heuristic.calculateOSNR(endSignal));

	for (int i = 0; i < amplifiers.length; i++) {
	    System.out.println(amplifiers[i]);
	}
	System.out.println();
    }


}
