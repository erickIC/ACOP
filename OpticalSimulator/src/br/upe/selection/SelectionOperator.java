package br.upe.selection;

import br.upe.base.Amplifier;

public interface SelectionOperator {

	/**
	 * Select the best amplifier among the candidates
	 * @param candidates
	 * @return
	 */
	public Amplifier select(Amplifier[] candidates);
	
	public Amplifier selectFirst(Amplifier[] candidates, float linkInputPower);
	
	public Amplifier selectLast(Amplifier[] candidates, float linkOutputPower);
}
