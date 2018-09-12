package br.upe.selection;

import java.util.ArrayList;
import java.util.List;

import br.upe.base.Amplifier;

public class QuadraticSelection implements SelectionOperator {

	@Override
	public Amplifier select(Amplifier[] candidates) {
		double tempMask = 0;

		double minMask = Double.MAX_VALUE;
		int indexMin = 0;

		for (int i = 0; i < candidates.length; i++) {
			tempMask = (candidates[i].getNoiseFigure())*(candidates[i].getNoiseFigure());
			tempMask += (candidates[i].getFlatness())*(candidates[i].getFlatness());

			if(Math.sqrt(tempMask) < minMask){
				minMask = tempMask;
				indexMin = i;
			}
		}

		return candidates[indexMin];
	}
	
	private Amplifier select(List<Amplifier> listAmp){
		Amplifier[] array = new Amplifier[listAmp.size()];
		for (int i = 0; i < listAmp.size(); i++) {
			array[i] = listAmp.get(i);
		}
		
		return select(array);
	}

	@Override
	public Amplifier selectFirst(Amplifier[] candidates, float linkInputPower) {
		ArrayList<Amplifier> filteredCandidates = new ArrayList<Amplifier>();

		for (int i = 0; i < candidates.length; i++) {

			if(Math.abs(candidates[i].getInputPower()-linkInputPower) <= 0.5){
				filteredCandidates.add(candidates[i]);
			}
		}


		if(filteredCandidates.size() > 1){
			return select(filteredCandidates);
		}
		else if (filteredCandidates.size() == 1){
			return filteredCandidates.get(0);
		}
		else{
			return select(candidates);
		}
		/*New candidates empty
		else{
			double nearestPin = Double.MAX_VALUE;
			int indexNearest = 0;

			for (int i = 0; i < candidates.length; i++) {
				double distance = Math.abs(candidates[i].getInputPower()-linkInputPower);
				if(distance < nearestPin){
					nearestPin = distance;
					indexNearest = i;
				}
			}

			return candidates[indexNearest];
		}*/
	}

	@Override
	public Amplifier selectLast(Amplifier[] candidates, float linkOutputPower) {
		ArrayList<Amplifier> filteredCandidates = new ArrayList<Amplifier>();

		for (int i = 0; i < candidates.length; i++) {

			if(Math.abs(candidates[i].getOutputPower()-linkOutputPower) <= 0.5){
				filteredCandidates.add(candidates[i]);
			}
		}


		if(filteredCandidates.size() > 1){
			return select((Amplifier[])filteredCandidates.toArray());
		}
		else if (filteredCandidates.size() == 1){
			return filteredCandidates.get(0);
		}
		//New candidates empty
		else{
			double nearestPin = Double.MAX_VALUE;
			int indexNearest = 0;

			for (int i = 0; i < candidates.length; i++) {
				double distance = Math.abs(candidates[i].getOutputPower()-linkOutputPower);
				if(distance < nearestPin){
					nearestPin = distance;
					indexNearest = i;
				}
			}

			return candidates[indexNearest];
		}
	}



}
