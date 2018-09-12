package br.upe.optimizationUtil;

import br.upe.base.ACOPHeuristic;
import br.upe.base.AmplifierType;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalSignal;
import br.upe.heuristics.AsHB.AsHBFlex;
import br.upe.heuristics.lossComp.LossComp;
import br.upe.heuristics.maxGain.MaxGain;
import br.upe.heuristics.uiara.AdGC;
import br.upe.initializations.UniformInitialization;
import br.upe.selection.MaxGainSelection;
import br.upe.selection.UiaraWeightSelection;
import br.upe.simulations.simsetups.SimulationSetup;

public abstract class CalculateFitness {

    protected ACOPHeuristic heuristic;

    private void createHeuristic(OptimizationParameters parameters) {

	SimulationSetup simSet = parameters.getSimulationSetup();
	int numberAmplifiers = simSet.getNumberOfAmplifiers();
	float[] linLosses = simSet.getLINK_LOSSES();
	OpticalSignal inputSignal = parameters.getInputSignal();
	ObjectiveFunction function = parameters.getFunction();
	AmplifierType type = parameters.getAmplifierType();
	float maxPout = simSet.getMaxOutputPower();

	ACOPHeuristic heuristic = null;

	switch (parameters.getHeuristic()) {
	case MAXGAIN:
	    heuristic = new MaxGain(numberAmplifiers, linLosses, inputSignal, function);
	    heuristic.setSelectionOp(new MaxGainSelection());
	    break;
	case ADGC:
	    heuristic = new AdGC(numberAmplifiers, linLosses, inputSignal, function);
	    heuristic.setInitialization(new UniformInitialization(type));
	    heuristic.setSelectionOp(new UiaraWeightSelection());

	    // When the selection uses weight
	    if (heuristic.getSelectionOp() instanceof UiaraWeightSelection) {
		((UiaraWeightSelection) heuristic.getSelectionOp()).setNFWeight(1);
		((UiaraWeightSelection) heuristic.getSelectionOp()).setGFWeight(0.5);
	    }
	    break;
	case ASHBFLEX:
	    heuristic = new AsHBFlex(numberAmplifiers, linLosses, inputSignal, function);
	    heuristic.setSelectionOp(new UiaraWeightSelection());
	    ((AsHBFlex) heuristic).setMaxIteration(5);
	    break;
	case LOSSCOMP:
	    heuristic = new LossComp(numberAmplifiers, linLosses, inputSignal, function);
	    break;
	}

	heuristic.setInitialization(new UniformInitialization(type));
	heuristic.setVoaMaxAttenuation(simSet.getVOA_MAX_ATT());
	heuristic.setRoadmAttenuation(simSet.getROADM_ATT());
	heuristic.setMaxOutputPower(maxPout);
	heuristic.setVoaLosses(parameters.getVoaLossPerChannel());

	this.heuristic = heuristic;
    }

    public double calculate(OptimizationParameters parameters) {
	createHeuristic(parameters);

	return getFitness(parameters);
    }

    public abstract double getFitness(OptimizationParameters parameters);

    public ACOPHeuristic getHeuristic() {
	return this.heuristic;
    }
}
