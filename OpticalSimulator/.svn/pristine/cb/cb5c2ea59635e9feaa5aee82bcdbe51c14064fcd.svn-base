package br.upe.selection;

import java.util.ArrayList;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;

public class UiaraWeightSelection implements SelectionOperator {

    private double NFWeight;
    private double GFWeight;

    /**
     * @return the gFWeight
     */
    private double getGFWeight() {
	return GFWeight;
    }

    /**
     * @param gFWeight
     *            the gFWeight to set
     */
    public void setGFWeight(double gFWeight) {
	GFWeight = gFWeight;
    }

    /**
     * @return the nFWeight
     */
    private double getNFWeight() {
	return NFWeight;
    }

    /**
     * @param nFWeight
     *            the nFWeight to set
     */
    public void setNFWeight(double nFWeight) {
	NFWeight = nFWeight;
    }

    public UiaraWeightSelection() {
	NFWeight = 1;
	GFWeight = 1;
    }

    @Override
    public Amplifier select(Amplifier[] candidates) {

	// Calcula o fitness de cada amplificador
	double[] fitness = calculateFitness(candidates);

	// Normalizing between 0 - 10
	// normalizeFitness(fitness, candidates);

	// Escolhe o melhor fitness, usando o angulo como criterio de desempate
	int[] bestFitness = getBestFitness(fitness);

	// retorna o amplificador que tem o melhor fitness
	return fitnessSelection(candidates, bestFitness);
    }



    private Amplifier fitnessSelection(Amplifier[] candidates, int[] bestFitness) {

	if (bestFitness.length == 1) {
	    return candidates[bestFitness[0]];
	} else {
	    double minAngle = Double.MAX_VALUE;
	    int minIndex = 0;
	    double tmpAngle;
	    for (int i = 0; i < bestFitness.length; i++) {
		tmpAngle = Math
			.atan(NFWeight * candidates[i].getNoiseFigure() / GFWeight * candidates[i].getFlatness());

		if (tmpAngle < minAngle) {
		    minAngle = tmpAngle;
		    minIndex = bestFitness[i];
		}
	    }

	    return candidates[minIndex];
	}
    }



    private int[] getBestFitness(double[] fitness) {
	double minMetric = Double.MAX_VALUE;
	ArrayList<Integer> indexs = new ArrayList<Integer>();

	for (int i = 0; i < fitness.length; i++) {
	    if (fitness[i] < minMetric) {
		minMetric = fitness[i];
		while (indexs.size() > 0) {
		    indexs.remove(0);
		}

		indexs.add(i);
	    } else if (fitness[i] == minMetric) {
		indexs.add(i);
	    }
	}

	int[] retorno = new int[indexs.size()];
	for (int i = 0; i < retorno.length; i++) {
	    retorno[i] = indexs.get(i);
	}

	return retorno;
    }


    private void normalizeFitness(double[] fitness, Amplifier[] candidates) {
	double minValue = 0;
	double maxValue = 10;

	// Applying the normalization
	for (int i = 0; i < fitness.length; i++) {
	    minValue = getMinFitness(candidates[i].getType());
	    maxValue = getMaxFitness(candidates[i].getType());

	    fitness[i] = normalizeEquation(fitness[i], maxValue, minValue) * 10;
	}
    }

    private double normalizeEquation(double value, double maxValue, double minValue) {
	return ((value - minValue) / (maxValue - minValue));
    }

    private double[] calculateFitness(Amplifier[] candidates) {
	double[] fitness = new double[candidates.length];
	double temp = 0;
	for (int i = 0; i < candidates.length; i++) {
	    temp = (NFWeight * candidates[i].getNoiseFigure()) * (NFWeight * candidates[i].getNoiseFigure());
	    temp += (GFWeight * candidates[i].getFlatness()) * (GFWeight * candidates[i].getFlatness());

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

    // TODO: Elaborar metodo automatico para definif Fitness Max e Min.
    private double getMaxFitness(AmplifierType type) {
	switch (type) {
	case P14_L21:
	    if (GFWeight == 1 && NFWeight == 1)
		return 7.5975;
	    else
		return 6.5994;
	case B21_L21:
	case B21_L24:
	    if (GFWeight == 1 && NFWeight == 1)
		return 6.6414;
	    else
		return 6.0223;
	default:
	    return -1;
	}
    }

    private double getMinFitness(AmplifierType type) {
	switch (type) {
	case P14_L21:
	    if (GFWeight == 1 && NFWeight == 1)
		return 4.807;
	    else
		return 4.7989;
	case B21_L21:
	case B21_L24:
	    if (GFWeight == 1 && NFWeight == 1)
		return 4.7355;
	    else
		return 4.727;
	default:
	    return -1;
	}
    }

}
