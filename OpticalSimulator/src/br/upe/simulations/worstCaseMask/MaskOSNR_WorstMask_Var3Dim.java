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

public class MaskOSNR_WorstMask_Var3Dim {

    public static void main(String[] args) {
	ACOPHeuristic heuristic;
	AmplifierType type = AmplifierType.EDFA_1_PadTec;
	ObjectiveFunction functionAux = new LinearInterpolationFunction();

	int numberCh = 40;
	int[] numberAmps = { 2, 4, 8, 10, 15, 20 };
	float[] pin = { -21, -18, -15 };
	float[] losses = { 18 };

	StringBuffer sbX = new StringBuffer();
	StringBuffer sbY = new StringBuffer();
	StringBuffer sbZ1 = new StringBuffer();
	StringBuffer sbZ2 = new StringBuffer();

	for (int i = 0; i < numberAmps.length; i++) {
	    for (int j = 0; j < pin.length; j++) {
		for (int j2 = 0; j2 < losses.length; j2++) {
		    StringBuffer sb = new StringBuffer();
		    int numberAmp = numberAmps[i];
		    float pinSystem = pin[j];
		    float loss = losses[j2];
		    sb.append(numberAmp + "\t" + pinSystem + "\t");

		    sbX.append(numberAmp + ", ");
		    sbY.append(pinSystem + ", ");

		    SimulationSetup simSet = new SimSetAMPVOA(numberCh, pinSystem, 9.0f, numberAmp, loss);
		    float[] linLosses = simSet.getLINK_LOSSES();
		    int numberAmplifiers = simSet.getNumberOfAmplifiers();

		    ObjectiveFunction function = new MaskOSNRFunction(functionAux, linLosses[0], false);
		    ObjectiveFunction functionWC = new MaskOSNRFunction(functionAux, linLosses[0], true);
		    BeckerNoiseFigureMetric nfMetric = new BeckerNoiseFigureMetric(linLosses);

		    double linkLength = linLosses[0] * 1000 / 0.2;
		    GNLIMetric gnliMetric = new GNLIMetric(28e9, 100e9, numberCh, pinSystem, linkLength);

		    // Definindo ganho m�ximo
		    float maxPout = simSet.getMaxOutputPower();
		    BruteForceInitialization bfIni = new BruteForceInitialization(type, false, maxPout);

		    PowerMaskSignal signal = new PowerMaskSignal(numberCh, type, simSet.getCHANNEL_POWER(), 30);
		    OpticalSignal inputSignal = signal.createSignal();
		    Amplifier[] amplifiers;
		    OpticalSignal endSignal;

		    double tempStr = 0;
		    NumberFormat nf = NumberFormat.getInstance();
		    nf.setMaximumFractionDigits(2);
		    nf.setMinimumFractionDigits(2);

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

		    tempStr = printResults(amplifiers, endSignal, nfMetric, gnliMetric,
			    heuristic.calculateTilt(endSignal), heuristic.calculateOSNR(endSignal));
		    sb.append(nf.format(tempStr) + "\t");

		    sbZ1.append(tempStr + ", ");

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

		    tempStr = printResults(amplifiers, endSignal, nfMetric, gnliMetric,
			    heuristic.calculateTilt(endSignal), heuristic.calculateOSNR(endSignal));
		    sb.append(nf.format(tempStr) + "\t");
		    sbZ2.append(tempStr + ", ");

		    System.out.println(sb);
		}
	    }
	}

	System.out.println(sbX);
	System.out.println(sbY);
	System.out.println(sbZ1);
	System.out.println(sbZ2);
    }

    private static double printResults(Amplifier[] amplifiers, OpticalSignal endSignal,
	    BeckerNoiseFigureMetric nfMetric,
	    GNLIMetric gnliMetric, double tilt, double OSNR) {
	gnliMetric.evaluate(amplifiers);
	return gnliMetric.worstOSNR_NLI();
	// return gnliMetric.getTiltOSNR_NLI();
    }

}
