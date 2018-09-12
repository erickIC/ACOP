package br.upe.heuristics.bruteForce;

import java.text.NumberFormat;

import br.upe.base.Amplifier;

public class SolutionBFMethod {

	private Amplifier[] amplifiers;
	private int numberOfVariables;
	private int numberOfObjectives;
	private double[] fitness;

	public SolutionBFMethod(int numberOfObjectives)
	{
		this.numberOfObjectives = numberOfObjectives;
		this.fitness = new double[numberOfObjectives];
	}

	/**
	 * @param gains the gains to set
	 */
	public void setAmplifiers(Amplifier[] amplifiers) {
		this.amplifiers = amplifiers;
	}

	/**
	 * @return the numberOfVariables
	 */
	public int getNumberOfVariables() {
		return numberOfVariables;
	}

	/**
	 * @param numberOfVariables the numberOfVariables to set
	 */
	public void setNumberOfVariables(int numberOfVariables) {
		this.numberOfVariables = numberOfVariables;
	}

	/**
	 * @return the numberOfObjectives
	 */
	public int getNumberOfObjectives() {
		return numberOfObjectives;
	}

	/**
	 * @param numberOfObjectives the numberOfObjectives to set
	 */
	public void setNumberOfObjectives(int numberOfObjectives) {
		this.numberOfObjectives = numberOfObjectives;
	}

	/**
	 * @return the fitness
	 */
	public double[] getFitness() {
		return fitness;
	}

	/**
	 * @param fitness the fitness to set
	 */
	public void setFitness(double[] fitness) {
		this.fitness = fitness;
	}

	public void setFitness(int objective, double fitness){
		this.fitness[objective] = fitness;
	}

	@Override
	public String toString() {
		StringBuffer strBuff = new StringBuffer();
		NumberFormat nf = NumberFormat.getInstance();
		nf.setMaximumFractionDigits(4);
		nf.setMinimumFractionDigits(2);
		
		for(int i=0; i<fitness.length; i++){
			strBuff.append(nf.format(fitness[i]) + "\t");
		}

		return strBuff.toString();
	}

	public String printAmps()
	{
		StringBuffer strBuff = new StringBuffer();

		strBuff.append("[");
		for(int i=0; i<amplifiers.length; i++){
			strBuff.append(amplifiers[i]);

			if(i == amplifiers.length-1){
				strBuff.append("]");
			}else{
				strBuff.append(", ");
			}
		}
				
		return strBuff.toString();
	}
}
