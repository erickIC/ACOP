package br.upe.optimizationUtil;

import br.upe.base.ACOPHeuristic;
import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalSignal;
import br.upe.objfunctions.rn.NNFunction;
import br.upe.objfunctions.rn.util.NormalizationUtility;
import br.upe.objfunctions.rn.util.NormalizationUtilityFactory;
import br.upe.signal.factory.PowerMaskSignal;
import br.upe.simulations.simsetups.SimSetAMPVOA;
import br.upe.simulations.simsetups.SimulationSetup;

public class TestCalculateMinOSNRNLI {

    public static void main(String[] args) {
	HeuristicsEnum heuristic = HeuristicsEnum.MAXGAIN;
	AmplifierType amplifierType = AmplifierType.EDFA_1_STG;
	NormalizationUtility nu = NormalizationUtilityFactory.getInstance().fabricate(amplifierType);
	ObjectiveFunction function = new NNFunction(nu); // LinearInterpolationFunction();

	int numberCh = 39;
	float pinSystem = -21f;
	SimulationSetup simSet = new SimSetAMPVOA(numberCh, pinSystem, 9f);

	double[][] voaLossPerChannel = new double[3][39];
	for (int i = 0; i < voaLossPerChannel[0].length; i++) {
	    voaLossPerChannel[0][i] = 0.0;
	}

	PowerMaskSignal signal = new PowerMaskSignal(numberCh, amplifierType, simSet.getCHANNEL_POWER(), 30);
	OpticalSignal inputSignal = signal.createSignal();

	OptimizationParameters parameters = new OptimizationParameters(heuristic, amplifierType, function, simSet,
		voaLossPerChannel, inputSignal);

	CalculateMinOSNRNLI calculator = new CalculateMinOSNRNLI();

	double OSNR = calculator.calculate(parameters);

	ACOPHeuristic heuristicRes = calculator.getHeuristic();

	Amplifier[] amplifiers = heuristicRes.getAmplifiers();
	OpticalSignal endSignal = heuristicRes.getMonitors()[amplifiers.length - 1].getOutputSignal();

	System.out.println("****** MaxGain ******");
	printResults(amplifiers, endSignal, OSNR, heuristicRes.calculateTilt(endSignal));
    }

    private static void printResults(Amplifier[] amplifiers, OpticalSignal endSignal, double OSNR,
	    double tilt) {
	System.out.println("OSNR\tRipple");
	System.out.printf("%2.3f\t%2.3f", OSNR, tilt);

	System.out.println();
	for (int i = 0; i < amplifiers.length; i++) {
	    System.out.println(amplifiers[i]);
	}
	System.out.println();
    }


}
