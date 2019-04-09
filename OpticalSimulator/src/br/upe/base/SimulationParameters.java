package br.upe.base;

import br.upe.simulations.simsetups.SimulationSetup;

public class SimulationParameters {
    private int numberCh;
    private float inputPowerCh;
    private float linkLosses;
    private SimulationSetup simSet;

    public SimulationParameters(int numberCh, float inputPowerCh, float linkLosses, SimulationSetup simSet) {
	super();
	this.numberCh = numberCh;
	this.inputPowerCh = inputPowerCh;
	this.linkLosses = linkLosses;
	this.simSet = simSet;
    }

    public int getNumberCh() {
	return numberCh;
    }

    public void setNumberCh(int numberCh) {
	this.numberCh = numberCh;
    }

    public float getInputPowerCh() {
	return inputPowerCh;
    }

    public void setInputPowerCh(float inputPowerCh) {
	this.inputPowerCh = inputPowerCh;
    }

    public float getLinkLosses() {
	return linkLosses;
    }

    public void setLinkLosses(float linkLosses) {
	this.linkLosses = linkLosses;
    }

    public SimulationSetup getSimSet() {
	return simSet;
    }

    public void setSimSet(SimulationSetup simSet) {
	this.simSet = simSet;
    }
}
