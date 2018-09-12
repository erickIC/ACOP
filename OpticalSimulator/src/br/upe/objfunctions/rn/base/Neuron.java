package br.upe.objfunctions.rn.base;

import java.util.ArrayList;

public class Neuron {
	public Function activationFunction;
    public double[] inputWeights;
    public boolean isBias;
    public double storedValue;
    public double sensibility;
    public ArrayList<Double> oldWeightChanges;

    public Neuron(Function activationFunction, double[] inputWeights, boolean isBias)
    {
        this.activationFunction = activationFunction;
        this.inputWeights = inputWeights;
        this.isBias = isBias;
        this.storedValue = 0.0;
        this.sensibility = 0.0;
        this.oldWeightChanges = new ArrayList<Double>();
        
        for (int i = 0; i < this.inputWeights.length; i++)
        {
            this.oldWeightChanges.add(0.0);
        }
    }

    public double functionCall()
    {
        return this.activationFunction.call(this.storedValue);
    }

    public double derivativeFunctionCall()
    {
        return this.activationFunction.derivativeCall(this.storedValue);    
    }
}
