package br.upe.simulations.JLT18;

import br.upe.base.ACOPHeuristic;
import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalSignal;
import br.upe.heuristics.AsHB.AsHBFlex;
import br.upe.heuristics.lossComp.LossComp;
import br.upe.heuristics.maxGain.MaxGain;
import br.upe.heuristics.uiara.AdGC;
import br.upe.initializations.UniformInitialization;
import br.upe.metrics.BeckerNoiseFigureMetric;
import br.upe.metrics.GNLIMetric;
import br.upe.objfunctions.linerInterpolation.LinearInterpolationFunction;
import br.upe.selection.MaxGainSelection;
import br.upe.selection.UiaraWeightSelection;
import br.upe.signal.factory.PowerMaskSignal;
import br.upe.simulations.simsetups.SimSetAMPVOA;
import br.upe.simulations.simsetups.SimulationSetup;

public class Default {

    public static void main(String[] args) {
	ACOPHeuristic heuristic;
	AmplifierType type = AmplifierType.EDFA_2_PadTec;

	ObjectiveFunction function = new LinearInterpolationFunction();

	int numberCh = 40;
	float pinSystem = -18.0f;
	SimulationSetup simSet = new SimSetAMPVOA(numberCh, pinSystem, 9.0f, 8, 18.0f);
	float[] linLosses = simSet.getLINK_LOSSES();
	int numberAmplifiers = simSet.getNumberOfAmplifiers();

	BeckerNoiseFigureMetric nfMetric = new BeckerNoiseFigureMetric(linLosses);

	double linkLength = linLosses[0] * 1000 / 0.2;
	GNLIMetric gnliMetric = new GNLIMetric(28e9, 100e9, numberCh, pinSystem, linkLength);

	// Definindo ganho m�ximo
	float maxPout = simSet.getMaxOutputPower();

	PowerMaskSignal signal = new PowerMaskSignal(numberCh, type, simSet.getCHANNEL_POWER(), 40);
	OpticalSignal inputSignal = signal.createSignal();
	Amplifier[] amplifiers;
	OpticalSignal endSignal;

	heuristic = new MaxGain(numberAmplifiers, linLosses, inputSignal, function);
	heuristic.setInitialization(new UniformInitialization(type));
	heuristic.setSelectionOp(new MaxGainSelection());
	heuristic.setVoaMaxAttenuation(simSet.getVOA_MAX_ATT());
	heuristic.setRoadmAttenuation(simSet.getROADM_ATT());
	heuristic.setMaxOutputPower(maxPout);
	amplifiers = heuristic.execute();
	endSignal = heuristic.getMonitors()[numberAmplifiers - 1].getOutputSignal();

	System.out.print("maxGain");
	printResults(amplifiers, endSignal, nfMetric, gnliMetric, heuristic.calculateTilt(endSignal),
		heuristic.calculateOSNR(endSignal));

	heuristic = new AdGC(numberAmplifiers, linLosses, inputSignal, function);
	heuristic.setInitialization(new UniformInitialization(type));
	heuristic.setSelectionOp(new UiaraWeightSelection());
	heuristic.setVoaMaxAttenuation(simSet.getVOA_MAX_ATT());
	heuristic.setRoadmAttenuation(simSet.getROADM_ATT());
	heuristic.setMaxOutputPower(maxPout);

	// When the selection uses weight
	if (heuristic.getSelectionOp() instanceof UiaraWeightSelection) {
	    ((UiaraWeightSelection) heuristic.getSelectionOp()).setNFWeight(1);
	    ((UiaraWeightSelection) heuristic.getSelectionOp()).setGFWeight(1);
	}

	amplifiers = heuristic.execute();
	endSignal = heuristic.getMonitors()[numberAmplifiers - 1].getOutputSignal();

	System.out.print("adgc");
	printResults(amplifiers, endSignal, nfMetric, gnliMetric, heuristic.calculateTilt(endSignal),
		heuristic.calculateOSNR(endSignal));

	heuristic = new AsHBFlex(numberAmplifiers, linLosses, inputSignal, function);
	heuristic.setSelectionOp(new UiaraWeightSelection());
	heuristic.setInitialization(new UniformInitialization(type));
	heuristic.setVoaMaxAttenuation(simSet.getVOA_MAX_ATT());
	heuristic.setRoadmAttenuation(simSet.getROADM_ATT());
	heuristic.setMaxOutputPower(maxPout);
	((AsHBFlex) heuristic).setMaxIteration(50);
	// When the selection uses weight
	if (heuristic.getSelectionOp() instanceof UiaraWeightSelection) {
	    ((UiaraWeightSelection) heuristic.getSelectionOp()).setNFWeight(1);
	    ((UiaraWeightSelection) heuristic.getSelectionOp()).setGFWeight(0.5);
	}

	amplifiers = heuristic.execute();
	endSignal = heuristic.getMonitors()[numberAmplifiers - 1].getOutputSignal();

	System.out.print("ashbflex");
	printResults(amplifiers, endSignal, nfMetric, gnliMetric, heuristic.calculateTilt(endSignal),
		heuristic.calculateOSNR(endSignal));

	heuristic = new LossComp(numberAmplifiers, linLosses, inputSignal, function);
	((LossComp) heuristic).setFirstAmplifierTargetGain(18); //Workout to edfa2
	heuristic.setInitialization(new UniformInitialization(type));
	heuristic.setVoaMaxAttenuation(simSet.getVOA_MAX_ATT());
	heuristic.setRoadmAttenuation(simSet.getROADM_ATT());
	heuristic.setMaxOutputPower(maxPout);
	amplifiers = heuristic.execute();
	endSignal = heuristic.getMonitors()[numberAmplifiers - 1].getOutputSignal();

	amplifiers[0].getGainPerChannel();

	System.out.print("lossComp");
	printResults(amplifiers, endSignal, nfMetric, gnliMetric, heuristic.calculateTilt(endSignal),
		heuristic.calculateOSNR(endSignal));

    }

    private static void printResults(Amplifier[] amplifiers, OpticalSignal endSignal, BeckerNoiseFigureMetric nfMetric,
	    GNLIMetric gnliMetric, double tilt, double OSNR) {
	gnliMetric.evaluate(amplifiers);
	// System.out.println("rp_O_NLI,O_NLI");
	// System.out.printf("%2.3f, %2.3f", gnliMetric.getTiltOSNR_NLI(),
	// gnliMetric.worstOSNR_NLI());
	System.out.println(" = [" + gnliMetric.getTiltOSNR_NLI() + ", " + gnliMetric.worstOSNR_NLI() + "]");

	// System.out.println(tilt + ", " + gnliMetric.worstOSNR_ASE() + ", " +
	// gnliMetric.worstOSNR_NLI());

	/*
	 * System.out.println("OSNR_edfa:"); double[] tempOSNR =
	 * gnliMetric.getOSNR_EDFA(); for (int i = 0; i < tempOSNR.length; i++)
	 * { System.out.print(tempOSNR[i] + "  "); }
	 */

	/*
	 * System.out.println(); System.out.println("OSNR_nli:"); tempOSNR =
	 * gnliMetric.getOSNR_NLI(); for (int i = 0; i < tempOSNR.length; i++) {
	 * System.out.print(tempOSNR[i] + "  "); }
	 */

	System.out.println();
	for (int i = 0; i < amplifiers.length; i++) {
		System.out.println(amplifiers[i]);
	}
    }

}
