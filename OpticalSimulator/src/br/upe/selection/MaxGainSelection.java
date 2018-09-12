package br.upe.selection;

import br.upe.base.Amplifier;

public class MaxGainSelection implements SelectionOperator {

    @Override
    public Amplifier select(Amplifier[] candidates) {
	int maxGainIndex = 0;
	for (int i = 1; i < candidates.length; i++) {
	    if (candidates[i].getGain() > candidates[maxGainIndex].getGain())
		maxGainIndex = i;
	}

	return candidates[maxGainIndex];
    }

    @Override
    public Amplifier selectFirst(Amplifier[] candidates, float linkInputPower) {
	return select(candidates);
    }

    @Override
    public Amplifier selectLast(Amplifier[] candidates, float linkOutputPower) {
	return select(candidates);
    }



}
