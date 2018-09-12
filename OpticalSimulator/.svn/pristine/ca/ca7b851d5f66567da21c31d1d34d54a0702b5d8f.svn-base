package br.upe.simulations.compareHeuristics;

import br.upe.base.ACOPHeuristic;
import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalSignal;
import br.upe.heuristics.AsHB.AsHBFlex;
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

public class MaskOSNR_VarItAsHB {

    public static void main(String[] args) {
	ACOPHeuristic heuristic;
	AmplifierType type = AmplifierType.EDFA_2_2_STG;

	NormalizationUtility nu = NormalizationUtilityFactory.getInstance().fabricate(type);
	ObjectiveFunction functionAux = new LinearInterpolationFunction(); // NNFunction(nu);

	System.out.println("-- LI --");

	int numberCh = 40;
	int iterations = 1;
	float pinSystem = -21.0f;

	while (iterations <= 50) {

	    SimulationSetup simSet = new SimSetAMPVOA(numberCh, pinSystem, 9.0f);
	    float[] linLosses = simSet.getLINK_LOSSES();
	    int numberAmplifiers = simSet.getNumberOfAmplifiers();

	    ObjectiveFunction function = new MaskOSNRFunction(functionAux, linLosses[0]);
	    BeckerNoiseFigureMetric nfMetric = new BeckerNoiseFigureMetric(linLosses);

	    double linkLength = linLosses[0] * 1000 / 0.2;
	    GNLIMetric gnliMetric = new GNLIMetric(28e9, 100e9, numberCh, pinSystem, linkLength);

	    // Definindo ganho máximo
	    float maxPout = simSet.getMaxOutputPower();
	    // System.out.println(maxPout);

	    PowerMaskSignal signal = new PowerMaskSignal(numberCh, type, simSet.getCHANNEL_POWER(), 30);
	    OpticalSignal inputSignal = signal.createSignal();


	    heuristic = new AsHBFlex(numberAmplifiers, linLosses, inputSignal, function);
	    heuristic.setSelectionOp(new OSNRWeightSelection());
	    heuristic.setInitialization(new UniformInitialization(type));
	    heuristic.setVoaMaxAttenuation(simSet.getVOA_MAX_ATT());
	    heuristic.setRoadmAttenuation(simSet.getROADM_ATT());
	    heuristic.setMaxOutputPower(maxPout);
	    ((AsHBFlex) heuristic).setMaxIteration(iterations); // When the
								// selection
							// uses weight
	    if (heuristic.getSelectionOp() instanceof OSNRWeightSelection) {
		((OSNRWeightSelection) heuristic.getSelectionOp()).setNFWeight(1.0);
		((OSNRWeightSelection) heuristic.getSelectionOp()).setGFWeight(1.0);
	    }

	    Amplifier[] amplifiers = heuristic.execute();
	    OpticalSignal endSignal = heuristic.getMonitors()[numberAmplifiers - 1].getOutputSignal();

	    // System.out.println("****** AsHB Flex ******");
	    printResults(amplifiers, endSignal, nfMetric, gnliMetric, heuristic.calculateTilt(endSignal),
		    heuristic.calculateOSNR(endSignal));

	    iterations += 1;
	}

    }

    private static void printResults(Amplifier[] amplifiers, OpticalSignal endSignal, BeckerNoiseFigureMetric nfMetric,
	    GNLIMetric gnliMetric, double tilt, double OSNR) {
	gnliMetric.evaluate(amplifiers);
	// System.out.println("NF\tGF\tO_NLI\tO_ASE");
	System.out.printf("%2.3f\t%2.3f\t%2.3f\t%2.3f", nfMetric.evaluate(amplifiers), tilt, gnliMetric.worstOSNR_NLI(),
		gnliMetric.worstOSNR_ASE());
	System.out.println();

	/*for (int i = 0; i < amplifiers.length; i++) {
	    System.out.println(amplifiers[i]);
	}
	System.out.println();*/

	/*System.out.print(tilt + ", " + gnliMetric.worstOSNR_NLI() + "]");
	System.out.println();*/
    }

}
