package br.upe.simulations.evalLaunchPower;

import br.upe.base.ACOPHeuristic;
import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalSignal;
import br.upe.heuristics.lossComp.LossComp;
import br.upe.initializations.UniformInitialization;
import br.upe.metrics.BeckerNoiseFigureMetric;
import br.upe.metrics.GNLIMetric;
import br.upe.objfunctions.linerInterpolation.LinearInterpolationFunction;
import br.upe.signal.factory.PowerMaskSignal;
import br.upe.simulations.simsetups.SimSetAMPVOA;
import br.upe.simulations.simsetups.SimulationSetup;

public class EvalLossComp {

    public static void main(String[] args) {
	ACOPHeuristic heuristic;
	AmplifierType type = AmplifierType.EDFA_2_PadTec;

	ObjectiveFunction function = new LinearInterpolationFunction();

	int numberCh = 40;
	float pinSystem = -18.0f;
	SimulationSetup simSet = new SimSetAMPVOA(numberCh, pinSystem, 9.0f, 10, 18.0f);
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

	heuristic = new LossComp(numberAmplifiers, linLosses, inputSignal, function);
	((LossComp) heuristic).setFirstAmplifierTargetGain(18); //Workout to edfa2
	heuristic.setInitialization(new UniformInitialization(type));
	heuristic.setVoaMaxAttenuation(simSet.getVOA_MAX_ATT());
	heuristic.setRoadmAttenuation(simSet.getROADM_ATT());
	heuristic.setMaxOutputPower(maxPout);
	amplifiers = heuristic.execute();
	endSignal = heuristic.getMonitors()[numberAmplifiers - 1].getOutputSignal();

	for (int i = 0; i < amplifiers.length; i++) {
	    System.out.format("%.4f\t", amplifiers[i].getOutputPower());
	}

    }

}
