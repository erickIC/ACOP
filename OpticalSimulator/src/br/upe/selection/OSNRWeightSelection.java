package br.upe.selection;

import java.util.ArrayList;

import br.upe.base.Amplifier;

public class OSNRWeightSelection implements SelectionOperator {

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

    public OSNRWeightSelection() {
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
			.atan(NFWeight * candidates[i].getMaskOSNR() / GFWeight * candidates[i].getFlatness());

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

    private double normalizeEquation(double value, double maxValue, double minValue) {
	return ((value - minValue) / (maxValue - minValue));
    }

    private double[] calculateFitness(Amplifier[] candidates) {
	double[] fitness = new double[candidates.length];
	double temp = 0;

	double maxOSNR = getMaxOSNR(candidates);
	double minOSNR = getMinOSNR(candidates);
	double maxFlatness = getMaxFlatness(candidates);
	double minFlatness = getMinFlatness(candidates);

	for (int i = 0; i < candidates.length; i++) {
	    double normalizedOSNR = normalizeEquation(1.0 / candidates[i].getMaskOSNR(), maxOSNR, minOSNR);
	    double normalizedFlatness = normalizeEquation(candidates[i].getFlatness(), maxFlatness, minFlatness);

	    if (maxFlatness == 0)
		normalizedFlatness = 1;

	    temp = (NFWeight * normalizedOSNR) * (NFWeight * normalizedOSNR);
	    temp += (GFWeight * normalizedFlatness) * (GFWeight * normalizedFlatness);

	    fitness[i] = Math.sqrt(temp);
	}

	return fitness;
    }


    private double getMaxOSNR(Amplifier[] candidates) {
	int maxOSNRindex = 0;
	for (int i = 1; i < candidates.length; i++) {
	    if ((1.0 / candidates[i].getMaskOSNR()) > (1.0 / candidates[maxOSNRindex].getMaskOSNR()))
		maxOSNRindex = i;
	}
	return 1.0 / candidates[maxOSNRindex].getMaskOSNR();
    }

    private double getMinOSNR(Amplifier[] candidates) {
	int minOSNRindex = 0;
	for (int i = 1; i < candidates.length; i++) {
	    if ((1.0 / candidates[i].getMaskOSNR()) < (1.0 / candidates[minOSNRindex].getMaskOSNR()))
		minOSNRindex = i;
	}
	return 1.0 / candidates[minOSNRindex].getMaskOSNR();
    }

    private double getMaxFlatness(Amplifier[] candidates) {
	int maxFlatindex = 0;
	for (int i = 1; i < candidates.length; i++) {
	    if (candidates[i].getFlatness() > candidates[maxFlatindex].getFlatness())
		maxFlatindex = i;
	}
	return candidates[maxFlatindex].getFlatness();
    }

    private double getMinFlatness(Amplifier[] candidates) {
	int minFlatindex = 0;
	for (int i = 1; i < candidates.length; i++) {
	    if (candidates[i].getFlatness() < candidates[minFlatindex].getFlatness())
		minFlatindex = i;
	}
	return candidates[minFlatindex].getFlatness();
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
