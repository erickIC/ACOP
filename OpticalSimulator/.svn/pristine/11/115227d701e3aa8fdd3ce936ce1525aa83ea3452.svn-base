package br.upe.simulations.compareHeuristics;

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
import br.upe.objfunctions.maskOSNR.MaskOSNRFunction;
import br.upe.objfunctions.rn.util.NormalizationUtility;
import br.upe.objfunctions.rn.util.NormalizationUtilityFactory;
import br.upe.selection.MaxGainSelection;
import br.upe.selection.UiaraWeightSelection;
import br.upe.signal.factory.PowerMaskSignal;
import br.upe.simulations.simsetups.SimSetAMPVOA;
import br.upe.simulations.simsetups.SimulationSetup;

public class Default_VarPin {

    public static void main(String[] args) {
	ACOPHeuristic heuristic;
	AmplifierType type = AmplifierType.EDFA_2_2_STG;

	NormalizationUtility nu = NormalizationUtilityFactory.getInstance().fabricate(type);
	ObjectiveFunction functionAux = new LinearInterpolationFunction(); // NNFunction(nu);

	System.out.println("-- LI --");

	int numberCh = 40;
	float pinSystem = -12.0f;

	while (pinSystem >= -27.0f) {

	    System.out.println("PIN = " + pinSystem);

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


	    heuristic = new MaxGain(numberAmplifiers, linLosses, inputSignal, function);
	    heuristic.setInitialization(new UniformInitialization(type));
	    heuristic.setSelectionOp(new MaxGainSelection());
	    heuristic.setVoaMaxAttenuation(simSet.getVOA_MAX_ATT());
	    heuristic.setRoadmAttenuation(simSet.getROADM_ATT());
	    heuristic.setMaxOutputPower(maxPout);
	    Amplifier[] amplifiers = heuristic.execute();
	    OpticalSignal endSignal = heuristic.getMonitors()[numberAmplifiers - 1].getOutputSignal();

	    System.out.println("****** MaxGain ******");
	    printResults(amplifiers, endSignal, nfMetric, gnliMetric, heuristic.calculateTilt(endSignal),
		    heuristic.calculateOSNR(endSignal));

	    double nfWeight = 1;
	    double gfWeight = 0.5;

	    heuristic = new AdGC(numberAmplifiers, linLosses, inputSignal, function);
	    heuristic.setInitialization(new UniformInitialization(type));
	    heuristic.setSelectionOp(new UiaraWeightSelection());
	    heuristic.setVoaMaxAttenuation(simSet.getVOA_MAX_ATT());
	    heuristic.setRoadmAttenuation(simSet.getROADM_ATT());
	    heuristic.setMaxOutputPower(maxPout);

	    // When the selection uses weight
	    if (heuristic.getSelectionOp() instanceof UiaraWeightSelection) {
		((UiaraWeightSelection) heuristic.getSelectionOp()).setNFWeight(nfWeight);
		((UiaraWeightSelection) heuristic.getSelectionOp()).setGFWeight(gfWeight);
	    }

	    amplifiers = heuristic.execute();
	    endSignal = heuristic.getMonitors()[numberAmplifiers - 1].getOutputSignal();

	    System.out.println("****** WAdGC ******");
	    printResults(amplifiers, endSignal, nfMetric, gnliMetric, heuristic.calculateTilt(endSignal),
		    heuristic.calculateOSNR(endSignal));

	    heuristic = new AsHBFlex(numberAmplifiers, linLosses, inputSignal, function);
	    heuristic.setSelectionOp(new UiaraWeightSelection());
	    heuristic.setInitialization(new UniformInitialization(type));
	    heuristic.setVoaMaxAttenuation(simSet.getVOA_MAX_ATT());
	    heuristic.setRoadmAttenuation(simSet.getROADM_ATT());
	    heuristic.setMaxOutputPower(maxPout);
	    ((AsHBFlex) heuristic).setMaxIteration(5);
	    // When the selection uses weight
	    if (heuristic.getSelectionOp() instanceof UiaraWeightSelection) {
		((UiaraWeightSelection) heuristic.getSelectionOp()).setNFWeight(1.0);
		((UiaraWeightSelection) heuristic.getSelectionOp()).setGFWeight(0.5);
	    }

	    amplifiers = heuristic.execute();
	    endSignal = heuristic.getMonitors()[numberAmplifiers - 1].getOutputSignal();

	    System.out.println("****** AsHB Flex ******");
	    printResults(amplifiers, endSignal, nfMetric, gnliMetric, heuristic.calculateTilt(endSignal),
		    heuristic.calculateOSNR(endSignal));

	    heuristic = new LossComp(numberAmplifiers, linLosses, inputSignal, function);
	    heuristic.setInitialization(new UniformInitialization(type));
	    heuristic.setVoaMaxAttenuation(simSet.getVOA_MAX_ATT());
	    heuristic.setRoadmAttenuation(simSet.getROADM_ATT());
	    heuristic.setMaxOutputPower(maxPout);
	    amplifiers = heuristic.execute();
	    endSignal = heuristic.getMonitors()[numberAmplifiers - 1].getOutputSignal();

	    amplifiers[0].getGainPerChannel();

	    System.out.println("****** LossComp ******");
	    printResults(amplifiers, endSignal, nfMetric, gnliMetric, heuristic.calculateTilt(endSignal),
		    heuristic.calculateOSNR(endSignal));

	    pinSystem -= 3.0f;
	}

    }

    private static void printResults(Amplifier[] amplifiers, OpticalSignal endSignal, BeckerNoiseFigureMetric nfMetric,
	    GNLIMetric gnliMetric, double tilt, double OSNR) {
	gnliMetric.evaluate(amplifiers);
	System.out.println("NF\tGF\tO_NLI\tO_ASE");
	System.out.printf("%2.3f\t%2.3f\t%2.3f\t%2.3f", nfMetric.evaluate(amplifiers), tilt, gnliMetric.worstOSNR_NLI(),
		gnliMetric.worstOSNR_ASE());
	System.out.println();

	for (int i = 0; i < amplifiers.length; i++) {
	    System.out.println(amplifiers[i]);
	}
	System.out.println();
    }

}
