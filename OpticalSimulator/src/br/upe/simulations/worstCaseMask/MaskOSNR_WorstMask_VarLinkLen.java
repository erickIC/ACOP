package br.upe.simulations.worstCaseMask;

import java.text.NumberFormat;

import br.upe.base.ACOPHeuristic;
import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalSignal;
import br.upe.heuristics.uiara.AdGC;
import br.upe.initializations.BruteForceInitialization;
import br.upe.initializations.UniformInitialization;
import br.upe.metrics.BeckerNoiseFigureMetric;
import br.upe.metrics.GNLIMetric;
import br.upe.objfunctions.linerInterpolation.LinearInterpolationFunction;
import br.upe.objfunctions.maskOSNR.MaskOSNRFunction;
import br.upe.selection.OSNRWeightSelection;
import br.upe.signal.factory.PowerMaskSignal;
import br.upe.simulations.simsetups.SimSetAMPVOA;
import br.upe.simulations.simsetups.SimulationSetup;

public class MaskOSNR_WorstMask_VarLinkLen {

    public static void main(String[] args) {
	ACOPHeuristic heuristic;
	AmplifierType type = AmplifierType.EDFA_1_PadTec;
	ObjectiveFunction functionAux = new LinearInterpolationFunction();

	int numberCh = 40;
	float[] losses = { 16, 18, 20, 22, 24 };

	StringBuffer sb = new StringBuffer();

	for (int i = 0; i < losses.length; i++) {
	    SimulationSetup simSet = new SimSetAMPVOA(numberCh, 9.0f, losses[i]);
	    float[] linLosses = simSet.getLINK_LOSSES();
	    float pinSystem = simSet.getCHANNEL_POWER();
	    int numberAmplifiers = simSet.getNumberOfAmplifiers();

	    ObjectiveFunction function = new MaskOSNRFunction(functionAux, linLosses[0], false);
	    ObjectiveFunction functionWC = new MaskOSNRFunction(functionAux, linLosses[0], true);
	    BeckerNoiseFigureMetric nfMetric = new BeckerNoiseFigureMetric(linLosses);

	    double linkLength = linLosses[0] * 1000 / 0.2;
	    GNLIMetric gnliMetric = new GNLIMetric(28e9, 100e9, numberCh, pinSystem, linkLength);

	    // Definindo ganho máximo
	    float maxPout = simSet.getMaxOutputPower();
	    System.out.println(maxPout);
	    BruteForceInitialization bfIni = new BruteForceInitialization(type, false, maxPout);

	    PowerMaskSignal signal = new PowerMaskSignal(numberCh, type, simSet.getCHANNEL_POWER(), 30);
	    OpticalSignal inputSignal = signal.createSignal();
	    Amplifier[] amplifiers;
	    OpticalSignal endSignal;

	    double tempStr = 0;
	    NumberFormat nf = NumberFormat.getInstance();
	    nf.setMaximumFractionDigits(2);
	    nf.setMinimumFractionDigits(2);

	    System.out.println("---------------------");
	    //System.out.println(simSet.getNumberOfAmplifiers() + " AMPLIFICADORES\t");
	    System.out.println(linkLength / 1000 + " km");
	    System.out.println("---------------------");

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

	    amplifiers = heuristic.execute();
	    endSignal = heuristic.getMonitors()[numberAmplifiers - 1].getOutputSignal();

	    System.out.println("****** WAdGC ******");
	    tempStr = printResults(amplifiers, endSignal, nfMetric, gnliMetric, heuristic.calculateTilt(endSignal),
		    heuristic.calculateOSNR(endSignal));
	    sb.append(nf.format(tempStr) + "\t");

	    heuristic = new AdGC(numberAmplifiers, linLosses, inputSignal, functionWC);
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

	    amplifiers = heuristic.execute();
	    endSignal = heuristic.getMonitors()[numberAmplifiers - 1].getOutputSignal();

	    bfIni.setGains(heuristic.getGains());
	    bfIni.setAttenuations(heuristic.getVOAAttenuations());
	    amplifiers = bfIni.initialize(simSet.getNumberOfAmplifiers(), inputSignal.getTotalPower(),
		    inputSignal.getTotalPower(), simSet.getLINK_LOSSES(), function, inputSignal.clone());
	    endSignal = bfIni.getSignal();

	    System.out.println("****** WAdGC_WCM ******");
	    tempStr = printResults(amplifiers, endSignal, nfMetric, gnliMetric, heuristic.calculateTilt(endSignal),
		    heuristic.calculateOSNR(endSignal));
	    //sb.append(nf.format(amplifiers[amplifiers.length - 1].getFlatness()) + "\t");
	    sb.append(nf.format(tempStr));

	    /* heuristic = new LossComp(numberAmplifiers, linLosses, inputSignal, function);
	    heuristic.setInitialization(new UniformInitialization(type));
	    heuristic.setVoaMaxAttenuation(simSet.getVOA_MAX_ATT());
	    heuristic.setRoadmAttenuation(simSet.getROADM_ATT());
	    heuristic.setMaxOutputPower(maxPout);
	    amplifiers = heuristic.execute();
	    endSignal = heuristic.getMonitors()[numberAmplifiers - 1].getOutputSignal();
	    
	    System.out.println("****** LossComp ******");
	    tempStr = printResults(amplifiers, endSignal, nfMetric, gnliMetric, heuristic.calculateTilt(endSignal),
	        heuristic.calculateOSNR(endSignal));
	    // sb.append("LossComp\n");
	    sb.append(nf.format(tempStr));
	    
	    heuristic = new LossComp(numberAmplifiers, linLosses, inputSignal, functionWC);
	    heuristic.setInitialization(new UniformInitialization(type));
	    heuristic.setVoaMaxAttenuation(simSet.getVOA_MAX_ATT());
	    heuristic.setRoadmAttenuation(simSet.getROADM_ATT());
	    heuristic.setMaxOutputPower(maxPout);
	    amplifiers = heuristic.execute();
	    endSignal = heuristic.getMonitors()[numberAmplifiers - 1].getOutputSignal();
	    
	    bfIni.setGains(heuristic.getGains());
	    bfIni.setAttenuations(heuristic.getVOAAttenuations());
	    amplifiers = bfIni.initialize(simSet.getNumberOfAmplifiers(), inputSignal.getTotalPower(),
	        inputSignal.getTotalPower(), simSet.getLINK_LOSSES(), function, inputSignal.clone());
	    
	    System.out.println("****** LossComp_WC ******");
	    tempStr = printResults(amplifiers, endSignal, nfMetric, gnliMetric, heuristic.calculateTilt(endSignal),
	        heuristic.calculateOSNR(endSignal));*/
	    // sb.append(nf.format(tempStr) + "\n");

	    pinSystem -= 3;

	    sb.append("\n");
	}

	System.out.println(type);
	System.out.println(sb);
    }

    private static double printResults(Amplifier[] amplifiers, OpticalSignal endSignal,
	    BeckerNoiseFigureMetric nfMetric,
	    GNLIMetric gnliMetric, double tilt, double OSNR) {
	gnliMetric.evaluate(amplifiers);
	System.out.println("NF\tGF\tO_NLI\tO_ASE");
	System.out.printf("%2.3f\t%2.3f\t%2.3f\t%2.3f", nfMetric.evaluate(amplifiers), tilt, gnliMetric.worstOSNR_NLI(),
		gnliMetric.worstOSNR_ASE());


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
	System.out.println();

	// return gnliMetric.worstOSNR_NLI();
	// return gnliMetric.getTiltOSNR_NLI();
	return tilt;
    }

}
