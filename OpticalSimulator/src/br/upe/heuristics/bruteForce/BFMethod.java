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
import br.upe.metrics.GNLIMetric;
import br.upe.objfunctions.linerInterpolation.LinearInterpolationFunction;
import br.upe.signal.factory.PowerMaskSignal;
import br.upe.simulations.simsetups.SimSetAMPVOA;
import br.upe.simulations.simsetups.SimulationSetup;
import br.upe.util.DecibelConverter;
import br.upe.util.Dominance;

public abstract class BFMethod {

    protected float INPUT_POWER = 0; // dBm
    protected static final int NUMBER_OBJ = 2;
    protected static final float STEP = 1f; // dB
    protected static float MAX_OUT_POWER = 0.0f; // dBm

    protected BruteForceInitialization initialization;
    protected ObjectiveFunction function;
    protected File arquivo;
    protected SimulationSetup simSet;
    protected OpticalSignal inputSignal;
    protected AmplifierType ampType;
    protected float inputPower;

    protected ArrayList<SolutionBFMethod> externalArchive;
    protected ArrayList<SolutionBFMethod> paretoFront;
    protected GNLIMetric gnliMetric;

    public BFMethod(int numberOfAmplifiers) {
	ampType = AmplifierType.EDFA_1_PadTec;
	String fileStr = "FB_results/VOA_110km_e1_";

	function = new LinearInterpolationFunction();

	int numberCh = 40;
	float inputPowerCh = -18f;
	float linkLosses = 22.0f;
	simSet = new SimSetAMPVOA(numberCh, inputPowerCh, 9.0f, numberOfAmplifiers);
	double linkLength = linkLosses * 1000 / 0.2;

	PowerMaskSignal signal = new PowerMaskSignal(numberCh, ampType, simSet.getCHANNEL_POWER(), 40);
	inputSignal = signal.createSignal();

	this.gnliMetric = new GNLIMetric(28e9, 100e9, numberCh, inputPowerCh, linkLength);

	// Definindo ganho máximo
	MAX_OUT_POWER = simSet.getMaxOutputPower();
	// System.out.println(MAX_OUT_POWER);

	boolean considerVOA = true;
	initialization = new BruteForceInitialization(ampType, considerVOA, MAX_OUT_POWER);

	INPUT_POWER = inputSignal.getTotalPower();
	
	try {
	    arquivo = new File(fileStr + numberOfAmplifiers + "amps_");
	} catch (Exception e) {

	}

    }

    public abstract void run();

    protected void printExternalArchive(String k) throws FileNotFoundException {

	if (externalArchive.size() == 0)
	    return;

	PrintWriter parameters = new PrintWriter(arquivo + "" + k + "_par.txt");
	PrintWriter amps = new PrintWriter(arquivo + "" + k + "_amp.txt");

	for (SolutionBFMethod s : externalArchive) {
	    parameters.print(s + "\n");
	    amps.print(s.printAmps() + "\n");
	    // System.out.println(s);
	}

	externalArchive.clear();
	parameters.close();
	amps.close();
    }

    protected void printParetoFront() throws FileNotFoundException {
	PrintWriter parameters = new PrintWriter(arquivo + "pareto_par.txt");
	PrintWriter amps = new PrintWriter(arquivo + "pareto_amp.txt");

	for (SolutionBFMethod s : paretoFront) {
	    parameters.print(s + "\n");
	    amps.print(s.printAmps() + "\n");
	    // System.out.println(s);
	}

	parameters.close();
	amps.close();
    }

    protected boolean isOutputPowerCorrect(Amplifier[] amplifiers) {
	for (int i = 0; i < amplifiers.length; i++) {
	    if (amplifiers[i] instanceof AmplifierVOA)
		continue;

	    if (amplifiers[i].getOutputPower() > MAX_OUT_POWER + 0.5f) {
		return false;
	    }
	}

	return true;
    }

    protected void addSolutionEA(SolutionBFMethod solution) {
	if (externalArchive == null) {
	    externalArchive = new ArrayList<SolutionBFMethod>();
	    paretoFront = new ArrayList<SolutionBFMethod>();

	    externalArchive.add(solution);
	} else {
	    externalArchive.add(solution);
	    for (SolutionBFMethod s : paretoFront) {
		if (compareSolutionByDominace(s, solution) == Dominance.DOMINATES || isEqual(s, solution)) {
		    return;
		}
	    }

	    ArrayList<SolutionBFMethod> tempPareto = new ArrayList<>();
	    for (int i = 0; i < paretoFront.size(); i++) {
		SolutionBFMethod s = paretoFront.get(i);
		if (compareSolutionByDominace(solution, s) != Dominance.DOMINATES) {
		    tempPareto.add(s);
		}
	    }
	    paretoFront = tempPareto;
	}

	paretoFront.add(solution);
    }

    protected boolean isEqual(SolutionBFMethod s1, SolutionBFMethod s2) {
	for (int i = 0; i < s1.getNumberOfObjectives(); i++) {
	    if (s1.getFitness()[i] != s2.getFitness()[i])
		return false;
	}
	return true;
    }

    protected Dominance compareSolutionByDominace(SolutionBFMethod solution, SolutionBFMethod anotherSolution) {
	int numObj = NUMBER_OBJ;
	boolean lostInAllDimensions = true;
	boolean winInAllDimensions = true;
	double[] fitness = solution.getFitness();
	double[] anotherFitness = anotherSolution.getFitness();

	for (int currentObj = 0; currentObj < numObj; currentObj++) {

	    if (currentObj == 1) {
		fitness[currentObj] *= -1;
		anotherFitness[currentObj] *= -1;
	    }

	    if (fitness[currentObj] > anotherFitness[currentObj]) {
		winInAllDimensions = false;
	    }

	    if (fitness[currentObj] < anotherFitness[currentObj]) {
		lostInAllDimensions = false;
	    }

	    if (currentObj == 1) {
		fitness[currentObj] *= -1;
		anotherFitness[currentObj] *= -1;
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

    protected double calculateOSNR(OpticalSignal signal) {
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

    protected double calculateTilt(OpticalSignal signal) {
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
}
