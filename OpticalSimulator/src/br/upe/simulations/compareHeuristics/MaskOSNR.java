package br.upe.simulations.compareHeuristics;

import br.upe.base.ACOPHeuristic;
import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalSignal;
import br.upe.heuristics.AsHB.AsHBFlex;
import br.upe.heuristics.uiara.AdGC;
import br.upe.initializations.UniformInitialization;
import br.upe.metrics.BeckerNoiseFigureMetric;
import br.upe.metrics.GNLIMetric;
import br.upe.objfunctions.linerInterpolation.LinearInterpolationFunction;
import br.upe.objfunctions.maskOSNR.MaskOSNRFunction;
import br.upe.objfunctions.rn.util.NormalizationUtility;
import br.upe.objfunctions.rn.util.NormalizationUtilityFactory;
import br.upe.selection.OSNRWeightSelection;
import br.upe.signal.factory.PowerMaskSignal;
import br.upe.simulations.simsetups.SimSetAMPVOA;
import br.upe.simulations.simsetups.SimulationSetup;

public class MaskOSNR {

    public static void main(String[] args) {
	ACOPHeuristic heuristic;
	AmplifierType type = AmplifierType.EDFA_1_PadTec;

	NormalizationUtility nu = NormalizationUtilityFactory.getInstance().fabricate(type);
	ObjectiveFunction functionAux = new LinearInterpolationFunction(); // NNFunction(nu);

	System.out.println("e1_3a");

	int numberCh = 40;
	float pinSystem = -18.0f;
	SimulationSetup simSet = new SimSetAMPVOA(numberCh, pinSystem, 9.0f, 3, 18.0f);
	float[] linLosses = simSet.getLINK_LOSSES();
	int numberAmplifiers = simSet.getNumberOfAmplifiers();

	ObjectiveFunction function = new MaskOSNRFunction(functionAux, linLosses[0], false);
	BeckerNoiseFigureMetric nfMetric = new BeckerNoiseFigureMetric(linLosses);

	double linkLength = linLosses[0] * 1000 / 0.2;
	GNLIMetric gnliMetric = new GNLIMetric(28e9, 100e9, numberCh, pinSystem, linkLength);

	// Definindo ganho m�ximo
	float maxPout = simSet.getMaxOutputPower();

	PowerMaskSignal signal = new PowerMaskSignal(numberCh, type, simSet.getCHANNEL_POWER(), 30);
	OpticalSignal inputSignal = signal.createSignal();

	double nfWeight = 1;
	double gfWeight = 0.5;

	heuristic = new AdGC(numberAmplifiers, linLosses, inputSignal, function);
	heuristic.setInitialization(new UniformInitialization(type));
	heuristic.setSelectionOp(new OSNRWeightSelection());
	heuristic.setVoaMaxAttenuation(simSet.getVOA_MAX_ATT());
	heuristic.setRoadmAttenuation(simSet.getROADM_ATT());
	heuristic.setMaxOutputPower(maxPout);

	// When the selection uses weight
	if (heuristic.getSelectionOp() instanceof OSNRWeightSelection) {
	    ((OSNRWeightSelection) heuristic.getSelectionOp()).setNFWeight(nfWeight);
	    ((OSNRWeightSelection) heuristic.getSelectionOp()).setGFWeight(gfWeight);
	}

	Amplifier[] amplifiers = heuristic.execute();
	OpticalSignal endSignal = heuristic.getMonitors()[numberAmplifiers - 1].getOutputSignal();

	System.out.print("adgc_nli");
	printResults(amplifiers, endSignal, nfMetric, gnliMetric, heuristic.calculateTilt(endSignal),
		heuristic.calculateOSNR(endSignal));

	heuristic = new AsHBFlex(numberAmplifiers, linLosses, inputSignal, function);
	heuristic.setSelectionOp(new OSNRWeightSelection());
	heuristic.setInitialization(new UniformInitialization(type));
	heuristic.setVoaMaxAttenuation(simSet.getVOA_MAX_ATT());
	heuristic.setRoadmAttenuation(simSet.getROADM_ATT());
	heuristic.setMaxOutputPower(maxPout);
	((AsHBFlex) heuristic).setMaxIteration(50);
	// When the selection uses weight
	if (heuristic.getSelectionOp() instanceof OSNRWeightSelection) {
	    ((OSNRWeightSelection) heuristic.getSelectionOp()).setNFWeight(1.0);
	    ((OSNRWeightSelection) heuristic.getSelectionOp()).setGFWeight(1.0);
	}

	amplifiers = heuristic.execute();
	endSignal = heuristic.getMonitors()[numberAmplifiers - 1].getOutputSignal();

	System.out.print("ashbflex_nli");
	printResults(amplifiers, endSignal, nfMetric, gnliMetric, heuristic.calculateTilt(endSignal),
		heuristic.calculateOSNR(endSignal));
    }

    private static void printResults(Amplifier[] amplifiers, OpticalSignal endSignal, BeckerNoiseFigureMetric nfMetric,
	    GNLIMetric gnliMetric, double tilt, double OSNR) {
	gnliMetric.evaluate(amplifiers);

	System.out.println(" = [" + gnliMetric.getTiltOSNR_NLI() + ", " + gnliMetric.worstOSNR_NLI() + "]");

	// System.out.println("rp_O_NLI,O_NLI");
	// System.out.printf("%2.3f, %2.3f", gnliMetric.getTiltOSNR_NLI(),
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

	// System.out.println();
	// for (int i = 0; i < amplifiers.length; i++) {
	// System.out.println(amplifiers[i]);
	// }
	// System.out.println();
    }

}
