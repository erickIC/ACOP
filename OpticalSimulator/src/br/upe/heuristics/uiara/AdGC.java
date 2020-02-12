package br.upe.heuristics.uiara;

import br.upe.base.ACOPHeuristic;
import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.AmplifierVOA;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalSignal;
import br.upe.initializations.UniformInitialization;
import br.upe.mascara.PowerMask;
import br.upe.mascara.PowerMaskFactory;
import br.upe.objfunctions.linerInterpolation.LinearInterpolationFunction;
import br.upe.selection.UiaraWeightSelection;
import br.upe.signal.factory.ITUGridUniformSignal;
import br.upe.signal.tracker.AmplifierSignalMonitor;
import br.upe.simulations.simsetups.SimSetAMPVOA;
import br.upe.simulations.simsetups.SimulationSetup;

public class AdGC extends ACOPHeuristic {

    public AdGC(int numberOfAmplifiers, float[] linkLosses, OpticalSignal inputSignal, ObjectiveFunction function) {
	super(numberOfAmplifiers, linkLosses, inputSignal, function);
	monitors[0] = new AmplifierSignalMonitor();
	monitors[0].setInputSignal(inputSignal);
    }

    @Override
    public Amplifier[] execute() {
	this.amplifiers = initialization.initialize(numberOfAmplifiers, linkInputPower, linkOutputPower, linkLosses,
		function, monitors[0].getInputSignal());

	boolean outOfMask = false;

	for (int i = 0; i < numberOfAmplifiers; i++) {
	    Amplifier[] candidates;

	    if (amplifiers[i] instanceof AmplifierVOA) {
		// Adaptação para considerar VOA na entrada
		/*
		 * if(amplifiers[0] instanceof AmplifierVOA){ MaxMinUtility
		 * maxmin = new MaxMinUtility(amplifiers[i].getType()); int
		 * minPin = maxmin.getMinPin(); for( int Pin =
		 * maxmin.getMinPin()+1; Pin <= amplifiers[i].getInputPower();
		 * Pin++){ if(maxmin.getMinNoiseFigure(Pin) <
		 * maxmin.getMinNoiseFigure(minPin)) minPin = Pin; } float
		 * voaInAtt = amplifiers[i].getInputPower() - minPin;
		 * ((AmplifierVOA) amplifiers[i]).setVoaInAttenuation(voaInAtt);
		 * }
		 */

		// The last amplifier has VOA but the others hasn't. Then it is
		// a VOA to the link, not to the AMP.
		if (i + 1 == numberOfAmplifiers && !(amplifiers[0] instanceof AmplifierVOA)) {
		    candidates = function.getAmplifiersCandidate(amplifiers[i], monitors[i].getInputSignal(),
			    maxOutputPower);
		} else {
		    candidates = function.getAmplifiersCandidate(amplifiers[i], monitors[i].getInputSignal());
		}
	    } else {
		candidates = function.getAmplifiersCandidate(amplifiers[i], monitors[i].getInputSignal(),
			maxOutputPower);
	    }

	    // for (int j = 0; j < candidates.length; j++) {
	    // System.out.println(1.0 / candidates[j].getMaskOSNR() + "\t" +
	    // candidates[j].getFlatness() + "\t"
	    // + candidates[j].getGain());
	    // }

	    // There is no operating point for the given input power
	    if (candidates.length == 0) {
		if (amplifiers[i] instanceof AmplifierVOA) {
		    if (((AmplifierVOA) amplifiers[i]).isAttenuationsSetted())
			return null;
		}

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

		amplifiers[i].setInputPower(maxInputPower);

		if (amplifiers[i - 1] instanceof AmplifierVOA) {
		    // Increase the voa attenuation of the previous amplifier
		    ((AmplifierVOA) amplifiers[i - 1]).increaseVoaOutAttenuation(difference);

		    if (((AmplifierVOA) amplifiers[i - 1]).getVoaOutAttenuation() > voaMaxAttenuation)
			return null;

		    // Use the amplifier to transform the signal
		    // Save the output power of this amplifier
		    monitors[i - 1]
			    .setOutputSignal(amplifiers[i - 1].transferFunction(monitors[i - 1].getInputSignal()));

		    updateNextAmplifier(i - 1);
		    i--;
		} else {
		    for (int j = i - 1; j >= 0; j--) {
			// Decrease the gain of the previous amplifier
			// (decrease the gain)
			float newGain = amplifiers[j].getGain() - 0.5f;// Math.round(amplifiers[j].getGain()
			// -
			// difference);
			PowerMask pm2 = PowerMaskFactory.getInstance().fabricatePowerMask(amplifiers[j].getType());

			// If the decrease cannot be done in the previous
			// amplifier, tr
			if (newGain >= pm2.getMinGain()) {
			    amplifiers[j].setGain(newGain);
			    function.defineNewOperationPoint(amplifiers[j], monitors[j].getInputSignal());

			    // Use the amplifier to transform the signal
			    // Save the output power of this amplifier
			    monitors[j].setOutputSignal(amplifiers[j].transferFunction(monitors[j].getInputSignal()));

			    updateNextAmplifier(j);
			    i--;
			    break;
			}

			i--;
		    }
		}

		continue;
	    }

	    Amplifier referenceOption = null;

	    // printObjectiveSpace(candidates);

	    referenceOption = selectionOp.select(candidates);

	    // updating the gain of the current amplifier
	    amplifiers[i].setGain(referenceOption.getGain());
	    function.defineNewOperationPoint(amplifiers[i], monitors[i].getInputSignal());

	    // Setting the attenuation of the VOA according to the max output
	    // power restriction
	    if (amplifiers[i] instanceof AmplifierVOA) {
		float newOutputPower = amplifiers[i].getOutputPower();
		if (newOutputPower > maxOutputPower)
		    ((AmplifierVOA) amplifiers[i]).setVoaOutAttenuation(newOutputPower - maxOutputPower);
	    }

	    // Last amplifier
	    if (i + 1 == numberOfAmplifiers) {
		if (amplifiers[i].getOutputPower() > linkOutputPower + voaMaxAttenuation + roadmAttenuation) {
		    int diff = Math.round(
			    amplifiers[i].getOutputPower() - (linkOutputPower + voaMaxAttenuation + roadmAttenuation));
		    amplifiers[i].setGain(amplifiers[i].getGain() - diff);
		    function.defineNewOperationPoint(amplifiers[i], monitors[i].getInputSignal());
		}

		float ampVoaAtt = ((AmplifierVOA) amplifiers[i]).getVoaOutAttenuation();
		float voaAttenuation = (float) (amplifiers[i].getOutputPower() - ampVoaAtt - linkInputPower
			- roadmAttenuation);
		((AmplifierVOA) amplifiers[i]).increaseVoaOutAttenuation(voaAttenuation);
	    }

	    // Use the amplifier to transform the signal
	    // Save the output power of this amplifier
	    monitors[i].setOutputSignal(amplifiers[i].transferFunction(monitors[i].getInputSignal()));

	    // If there is a next amplifier
	    if ((i + 1) < numberOfAmplifiers) {
		updateNextAmplifier(i);
	    }
	}

	return amplifiers;
    }

    private void printObjectiveSpace(Amplifier[] candidates) {
	StringBuffer OSNR = new StringBuffer();
	StringBuffer rp = new StringBuffer();
	StringBuffer gain = new StringBuffer();

	OSNR.append("osnr = [");
	rp.append("rp = [");
	gain.append("gain = [");

	for (int i = 0; i < candidates.length; i++) {
	    OSNR.append(candidates[i].getMaskOSNR());
	    rp.append(candidates[i].getFlatness());
	    gain.append(candidates[i].getGain());

	    if (i == candidates.length - 1) {
		OSNR.append("]");
		rp.append("]");
		gain.append("]");
	    } else {
		OSNR.append(", ");
		rp.append(", ");
		gain.append(", ");
	    }
	}

	System.out.println(OSNR);
	System.out.println(rp);
	System.out.println(gain);

    }

    public static void main(String[] args) {
	ACOPHeuristic heuristic;
	ObjectiveFunction function = new LinearInterpolationFunction();

	int numberCh = 40;
	SimulationSetup simSet = new SimSetAMPVOA(numberCh, -26.3f, 4.0f);
	float[] linLosses = simSet.getLINK_LOSSES();
	int numberAmplifiers = simSet.getNumberOfAmplifiers();

	// Definindo ganho máximo
	float maxPout = simSet.getMaxOutputPower();
	System.out.println(maxPout);

	ITUGridUniformSignal signal = new ITUGridUniformSignal(simSet.getCHANNELS(), 1.921e14, 100e9,
		simSet.getCHANNEL_POWER(), 30);
	OpticalSignal inputSignal = signal.createSignal();

	long t1 = System.currentTimeMillis();
	heuristic = new AdGC(numberAmplifiers, linLosses, inputSignal, function);
	heuristic.setInitialization(new UniformInitialization(AmplifierType.EDFA_1_STG));
	heuristic.setSelectionOp(new UiaraWeightSelection());
	heuristic.setVoaMaxAttenuation(simSet.getVOA_MAX_ATT());
	heuristic.setRoadmAttenuation(simSet.getROADM_ATT());
	heuristic.setMaxOutputPower(maxPout);

	// When the selection uses weight
	if (heuristic.getSelectionOp() instanceof UiaraWeightSelection) {
	    ((UiaraWeightSelection) heuristic.getSelectionOp()).setNFWeight(1);
	    ((UiaraWeightSelection) heuristic.getSelectionOp()).setGFWeight(0.5);
	}

	Amplifier[] amplifiers = heuristic.execute();
	System.out.printf("OSNR_h = %2.3f\t",
		heuristic.calculateOSNR(heuristic.getMonitors()[numberAmplifiers - 1].getOutputSignal()));
	System.out.printf("Tilt_h = %2.3f\n",
		heuristic.calculateTilt(heuristic.getMonitors()[numberAmplifiers - 1].getOutputSignal()));

	for (int i = 0; i < amplifiers.length; i++) {
	    System.out.println(amplifiers[i]);
	}

	System.out.println("Tempo V = " + (System.currentTimeMillis() - t1));
    }
}
