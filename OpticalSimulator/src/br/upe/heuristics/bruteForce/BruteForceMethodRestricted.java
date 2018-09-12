package br.upe.heuristics.bruteForce;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.ArrayList;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.AmplifierVOA;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalChannel;
import br.upe.base.OpticalSignal;
import br.upe.initializations.BruteForceInitialization;
import br.upe.mascara.PowerMask;
import br.upe.mascara.PowerMaskFactory;
import br.upe.metrics.GNLIMetric;
import br.upe.objfunctions.linerInterpolation.LinearInterpolationFunction;
import br.upe.objfunctions.rn.util.NormalizationUtility;
import br.upe.objfunctions.rn.util.NormalizationUtilityFactory;
import br.upe.signal.factory.PowerMaskSignal;
import br.upe.simulations.simsetups.SimSetAMPVOA;
import br.upe.simulations.simsetups.SimulationSetup;
import br.upe.util.DecibelConverter;
import br.upe.util.Dominance;

public class BruteForceMethodRestricted {

    private float INPUT_POWER = 0; // dBm
    private static final int NUMBER_OBJ = 3;
    private static final float STEP = 1f; // dB
    private static float MAX_OUT_POWER = 0.0f; // dBm

    private BruteForceInitialization initialization;
    private ObjectiveFunction function;
    private File arquivo;
    private SimulationSetup simSet;
    private OpticalSignal inputSignal;
    private AmplifierType ampType;
    private float inputPower;

    private ArrayList<SolutionBFMethod> externalArchive;

    public BruteForceMethodRestricted() {
	ampType = AmplifierType.EDFA_1_STG;

	NormalizationUtility nu = NormalizationUtilityFactory.getInstance().fabricate(ampType);
	function = new LinearInterpolationFunction();

	int numberCh = 39;
	inputPower = -21.0f;
	simSet = new SimSetAMPVOA(numberCh, inputPower, 9.0f);

	PowerMaskSignal signal = new PowerMaskSignal(numberCh, ampType, simSet.getCHANNEL_POWER(), 30);
	inputSignal = signal.createSignal();

	// Definindo ganho máximo
	MAX_OUT_POWER = simSet.getMaxOutputPower();
	System.out.println(MAX_OUT_POWER);

	boolean considerVOA = true;
	initialization = new BruteForceInitialization(ampType, considerVOA, MAX_OUT_POWER);

	INPUT_POWER = inputSignal.getTotalPower();

	try {
	    arquivo = new File("FB_results/LI_edfa1_nliEase_-21_");
	} catch (Exception e) {

	}

    }

    public void run() {

	// long ti = System.currentTimeMillis();
	// System.out.println("Start");
	GNLIMetric gnliMetric = new GNLIMetric(28e9, 100e9, 39, inputPower, 100e3);

	PowerMask pm = PowerMaskFactory.getInstance().fabricatePowerMask(ampType);

	double totalComb = pm.getMaxGain() - pm.getMinGain() + 1;
	totalComb = totalComb * totalComb * totalComb * totalComb;

	double contador = 0;

	float shift = 0.0f;

	while (shift < STEP) {
	    float i = 27 - shift;// pm.getMaxGain() - shift;
	    while (i >= pm.getMinGain()) { // G1

		float j = 27 - shift;// pm.getMaxGain() - shift;
		while (j >= pm.getMinGain()) { // G2

		    float k = 27 - shift;// pm.getMaxGain() - shift;
		    while (k >= pm.getMinGain()) { // G3

			float l = 27 - shift;// pm.getMaxGain() - shift;
			while (l >= pm.getMinGain()) { // G4

			    float[] gains = { i, j, k, l };
			    float[] attenuations = { 0, 0, 0, 0 };
			    initialization.setGains(gains);
			    initialization.setAttenuations(attenuations);
			    OpticalSignal signalTemp = inputSignal.clone();
			    Amplifier[] amplifiers = initialization.initialize(simSet.getNumberOfAmplifiers(),
				    INPUT_POWER, 0, simSet.getLINK_LOSSES(), function, signalTemp);

			    // Solucao fora das restricoes
			    if (amplifiers == null
				    || Math.abs(amplifiers[0].getInputPower()) > (Math.abs(INPUT_POWER) + 0.5)
				    || Math.abs(amplifiers[0].getInputPower()) < (Math.abs(INPUT_POWER) - 0.5)
				    || !this.isOutputPowerCorrect(amplifiers)) { // restriction
				// to
				// guarantee
				// the
				// maximum
				// output
				// power
				l -= STEP;
				contador++;
				continue;
			    }

			    SolutionBFMethod solution = null;

			    float ampVoaAtt = ((AmplifierVOA) amplifiers[amplifiers.length - 1]).getVoaOutAttenuation();
			    float voaAttenuation = (float) (amplifiers[amplifiers.length - 1].getOutputPower()
				    - ampVoaAtt - INPUT_POWER - simSet.getROADM_ATT());
			    ((AmplifierVOA) amplifiers[amplifiers.length - 1])
				    .increaseVoaOutAttenuation(voaAttenuation);

			    // If the output power of the link is less than the
			    // input power, then the solution isn't desirable.
			    // And, if the output power is greater than the
			    // input
			    // power + voa max attenuation + roadm attenuation,
			    // then
			    // the solution is not desirable
			    if (amplifiers[amplifiers.length - 1].getOutputPower() >= INPUT_POWER
				    && ((AmplifierVOA) amplifiers[amplifiers.length - 1])
					    .getOutputPowerAfterVOA() <= (INPUT_POWER + simSet.getVOA_MAX_ATT()
						    + simSet.getROADM_ATT())) {

				solution = new SolutionBFMethod(NUMBER_OBJ);

				solution.setAmplifiers(amplifiers);

				// solution.setFitness(0,
				// nfMetric.evaluate(amplifiers)); // nf
				solution.setFitness(0, calculateTilt(signalTemp)); // gf

				gnliMetric.evaluate(amplifiers);
				solution.setFitness(1, gnliMetric.worstOSNR_ASE()); // OSNR
				solution.setFitness(2, gnliMetric.worstOSNR_NLI()); // OSNR

				// Choose best solution
				/*
				 * double[] fitness = solution.getFitness();
				 * double solutionDi = Math.sqrt(fitness[2] *
				 * fitness[2] / fitness[1] * fitness[1]);
				 * 
				 * if (solutionDi > bestDi) { bestSol =
				 * solution; bestDi = solutionDi; }
				 */
			    }

			    if (solution != null) {
				this.addSolutionEA(solution);
			    }

			    l -= STEP;
			    contador++;
			}

			k -= STEP;
		    }

		    j -= STEP;

		    double perc = (contador / totalComb) * 100;
		    System.out.printf("%3.2f \n", perc);

		    /*
		     * long te = System.currentTimeMillis(); System.out.println(
		     * "End = " + (te -ti) + " msec.\n\n");
		     */

		}

		i -= STEP;
	    }
	    shift += STEP;// 0.1f;
	}

	// System.out.println("Best NF = " + bestDi);
	// System.out.println(bestSol);
	// System.out.println(bestSol.printAmps());

	try {
	    printExternalArchive();
	} catch (Exception e) {

	}
    }

    private void printExternalArchive() throws FileNotFoundException {
	PrintWriter pareto = new PrintWriter(arquivo + "par.txt");
	PrintWriter amps = new PrintWriter(arquivo + "amp.txt");

	for (SolutionBFMethod s : externalArchive) {
	    pareto.print(s + "\n");
	    amps.print(s.printAmps() + "\n");
	    // System.out.println(s);
	}

	pareto.close();
	amps.close();
    }

    private boolean isOutputPowerCorrect(Amplifier[] amplifiers) {
	for (int i = 0; i < amplifiers.length; i++) {
	    if (amplifiers[i] instanceof AmplifierVOA)
		continue;

	    if (amplifiers[i].getOutputPower() > MAX_OUT_POWER + 0.5f) {
		return false;
	    }
	}

	return true;
    }

    private void addSolutionEA(SolutionBFMethod solution) {

	if (externalArchive == null) {
	    externalArchive = new ArrayList<SolutionBFMethod>();
	} /*else {
	    for (SolutionBFMethod s : externalArchive) {
		if (compareSolutionByDominace(s, solution) == Dominance.DOMINATES) {
		    return;
		}
	    }

	    for (int i = 0; i < externalArchive.size(); i++) {
		SolutionBFMethod s = externalArchive.get(i);
		if (compareSolutionByDominace(solution, s) == Dominance.DOMINATES) {
		    externalArchive.remove(i);
		}
	    }
	}*/

	externalArchive.add(solution);

    }

    protected Dominance compareSolutionByDominace(SolutionBFMethod solution, SolutionBFMethod anotherSolution) {
	int numObj = NUMBER_OBJ;
	boolean lostInAllDimensions = true;
	boolean winInAllDimensions = true;
	double[] fitness = solution.getFitness();
	double[] anotherFitness = anotherSolution.getFitness();

	for (int currentObj = 0; currentObj < numObj; currentObj++) {

	    if (fitness[currentObj] > anotherFitness[currentObj]) {
		winInAllDimensions = false;
	    }

	    if (fitness[currentObj] < anotherFitness[currentObj]) {
		lostInAllDimensions = false;
	    }

	    if (!winInAllDimensions && !lostInAllDimensions) {
		return Dominance.INCOMPARABLE;
	    }
	}

	if (winInAllDimensions && lostInAllDimensions) {
	    return Dominance.INCOMPARABLE;
	}

	if (winInAllDimensions) {
	    return Dominance.DOMINATES;
	}

	if (lostInAllDimensions) {
	    return Dominance.DOMINATED;
	}

	return Dominance.INCOMPARABLE;

    }

    public double calculateOSNR(OpticalSignal signal) {
	double minOSNR = Double.MAX_VALUE;
	for (OpticalChannel c : signal.getChannels()) {
	    double signalLin = DecibelConverter.toLinearScale(c.getSignalPower());
	    double noiseLin = DecibelConverter.toLinearScale(c.getNoisePower());
	    double OSNR = signalLin / noiseLin;

	    if (OSNR < minOSNR) {
		minOSNR = OSNR;
	    }
	}

	return DecibelConverter.toDecibelScale(minOSNR);
    }

    public double calculateTilt(OpticalSignal signal) {
	double maxPeak = Double.MIN_VALUE;
	double minPeak = Double.MAX_VALUE;

	for (OpticalChannel c : signal.getChannels()) {
	    double signalLin = DecibelConverter.toLinearScale(c.getSignalPower());

	    if (signalLin > maxPeak) {
		maxPeak = signalLin;
	    }
	    if (signalLin < minPeak) {
		minPeak = signalLin;
	    }
	}

	return DecibelConverter.toDecibelScale(maxPeak / minPeak);
    }

    public static void main(String[] args) {
	int runs = 1;

	for (int i = 0; i < runs; i++) {
	    long ti = System.currentTimeMillis();

	    BruteForceMethodRestricted bf = new BruteForceMethodRestricted();

	    bf.run();

	    System.out.println(System.currentTimeMillis() - ti);
	}
    }


}
