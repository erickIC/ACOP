package br.upe.optimizationUtil;

import br.upe.base.AmplifierType;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalSignal;
import br.upe.simulations.simsetups.SimulationSetup;

public class OptimizationParameters {
    private HeuristicsEnum heuristic;
    private AmplifierType amplifierType;
    private ObjectiveFunction function;
    private SimulationSetup simulationSetup;
    private double[][] voaLossPerChannel;
    private OpticalSignal inputSignal;

    public OptimizationParameters(HeuristicsEnum heuristic, AmplifierType amplifierType, ObjectiveFunction function,
	    SimulationSetup simulationSetup, double[][] voaLossPerChannel, OpticalSignal inputSignal) {
	super();
	this.heuristic = heuristic;
	this.amplifierType = amplifierType;
	this.function = function;
	this.simulationSetup = simulationSetup;
	this.voaLossPerChannel = voaLossPerChannel;
	this.inputSignal = inputSignal;
    }

    public HeuristicsEnum getHeuristic() {
	return heuristic;
    }

    public void setHeuristic(HeuristicsEnum heuristic) {
	this.heuristic = heuristic;
    }

    public AmplifierType getAmplifierType() {
	return amplifierType;
    }

    public void setAmplifierType(AmplifierType type) {
	this.amplifierType = type;
    }

    public ObjectiveFunction getFunction() {
	return function;
    }

    public void setFunction(ObjectiveFunction function) {
	this.function = function;
    }

    public SimulationSetup getSimulationSetup() {
	return simulationSetup;
    }

    public void setSimulationSetup(SimulationSetup simulationSetup) {
	this.simulationSetup = simulationSetup;
    }

    public double[][] getVoaLossPerChannel() {
	return voaLossPerChannel;
    }

    public void setVoaLossPerChannel(double[][] voaLossPerChannel) {
	this.voaLossPerChannel = voaLossPerChannel;
    }

    public OpticalSignal getInputSignal() {
	return inputSignal;
    }

    public void setInputSignal(OpticalSignal inputSignal) {
	this.inputSignal = inputSignal;
    }
}
