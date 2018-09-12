package br.upe.selection;

import java.util.ArrayList;

import br.upe.base.Amplifier;

public class UiaraSelection implements SelectionOperator {

	@Override
	public Amplifier select(Amplifier[] candidates) {
		
		double[] fitness = calculateFitness(candidates);
		
		normalizeFitness(fitness);
		
		int[] bestFitness = getBestFitness(fitness);
		
		return fitnessSelection(candidates, bestFitness);
	}
	
	

	private Amplifier fitnessSelection(Amplifier[] candidates, int[] bestFitness) {
		
		if(bestFitness.length == 1){
			return candidates[bestFitness[0]];
		}
		else{
			double minAngle = Double.MAX_VALUE;
			int minIndex = 0;
			double tmpAngle;
			for (int i = 0; i < bestFitness.length; i++) {
				tmpAngle = Math.atan(candidates[i].getNoiseFigure()/candidates[i].getFlatness());
				
				if(tmpAngle < minAngle){
					minAngle = tmpAngle;
					minIndex = i;
				}
			}
			
			return candidates[minIndex];
		}
	}



	private int[] getBestFitness(double[] fitness) {
		double minMetric = Double.MAX_VALUE;
		ArrayList<Integer> indexs = new ArrayList<Integer>();
		
		for (int i = 0; i < fitness.length; i++) {
			if(fitness[i] < minMetric){
				minMetric = fitness[i];
				while(indexs.size() > 0){
					indexs.remove(0);
				}
				
				indexs.add(i);
			}
			else if(fitness[i] == minMetric){
				indexs.add(i);
			}
		}
		
		int[] retorno = new int[indexs.size()];
		for (int i = 0; i < retorno.length; i++) {
			retorno[i] = indexs.get(i);
		}
 		
		return retorno;
	}



	private void normalizeFitness(double[] fitness) {
		int minValue = 0;
		int maxValue = 10;
		
		for (int i = 0; i < fitness.length; i++) {
			fitness[i] = normalizeEquation(fitness[i], maxValue, minValue);
		}
	}

	private double normalizeEquation(double value, double maxValue, double minValue){
		return ((value-minValue)/(maxValue-minValue));
	}

	private double[] calculateFitness(Amplifier[] candidates) {
		double[] fitness = new double[candidates.length];
		double temp = 0;
		for(int i=0; i<candidates.length; i++){
			temp = (candidates[i].getNoiseFigure())*(candidates[i].getNoiseFigure());
			temp += (candidates[i].getFlatness())*(candidates[i].getFlatness());
			
			fitness[i] = Math.sqrt(temp);
		}
		
		return fitness;
	}



	@Override
	public Amplifier selectFirst(Amplifier[] candidates, float linkInputPower) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Amplifier selectLast(Amplifier[] candidates, float linkOutputPower) {
		// TODO Auto-generated method stub
		return null;
	}

}
