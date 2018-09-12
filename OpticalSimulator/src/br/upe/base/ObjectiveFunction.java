package br.upe.base;

import java.util.ArrayList;

import br.upe.util.DecibelConverter;

public abstract class ObjectiveFunction {


    /**
     * Calculates the amplifer's new operation point
     * 
     * @param amplifier
     *            The amplifier
     */
    public abstract void defineNewOperationPoint(Amplifier amplifier, OpticalSignal signal);

    /**
     * Calculates the amplifer's new operation point considering worst case
     * mask. Worst case mask does not consider channel info, thus the NF and
     * gain are the same for all channels. The NF is the worst among channels,
     * and the gain is the gain set.
     * 
     * @param amplifier
     *            The amplifier
     */
    public abstract void defineNewOperationPointWorstCase(Amplifier amplifier, OpticalSignal signal);

    /**
     * Returns a set of possible amplifiers according to the current input
     * signal, or gain, of the amplifier
     * 
     * @param amplifier
     *            The current amplifier
     * @param signal
     *            The input signal of the amplifier
     * @param useInput
     *            If true, uses the input power. Else, uses the gain.
     * @return A set of amplifiers
     */
    public abstract Amplifier[] getAmplifiersCandidate(Amplifier amplifier, OpticalSignal signal, boolean useInput);

    /**
     * Returns a set of possible amplifiers according to the current input
     * signal of the amplifier
     * 
     * @param amplifier
     *            The current amplifier
     * @param signal
     *            The input signal of the amplifier
     * @return A set of amplifiers
     */
    public Amplifier[] getAmplifiersCandidate(Amplifier amplifier, OpticalSignal signal) {
	return getAmplifiersCandidate(amplifier, signal, true);
    }

    /**
     * Returns a set of possible amplifiers according to the input signal of the
     * current amplifier, restricted to the a maximum output Power
     * 
     * @param amplifier
     *            The current amplifier
     * @param signal
     *            The input signal of the amplifier
     * @param maxOutputpower
     *            The maximum output power
     * @return A set of amplifiers
     */
    public Amplifier[] getAmplifiersCandidate(Amplifier amplifier, OpticalSignal signal, float maxOutputPower) {
	Amplifier[] candidates = getAmplifiersCandidate(amplifier, signal, true);
	ArrayList<Amplifier> candidatesCorrectOutput = new ArrayList<Amplifier>();

	for (int i = 0; i < candidates.length; i++) {
	    if (candidates[i].getOutputPower() < (maxOutputPower + 0.5f))
		candidatesCorrectOutput.add(candidates[i]);
	}

	candidates = new Amplifier[candidatesCorrectOutput.size()];
	candidatesCorrectOutput.toArray(candidates);

	return candidates;
    }

    /**
     * Returns a set of possible amplifiers according to the input signal, or
     * gain, of the current amplifier, restricted to the a maximum output Power
     * 
     * @param amplifier
     *            The current amplifier
     * @param signal
     *            The input signal of the amplifier
     * @param useInput
     *            If true, uses the input power. Else, uses the gain.
     * @param maxOutputpower
     *            The maximum output power
     * @return A set of amplifiers
     */
    public Amplifier[] getAmplifiersCandidate(Amplifier amplifier, OpticalSignal signal, boolean useInput,
	    float maxOutputPower) {
	Amplifier[] candidates = getAmplifiersCandidate(amplifier, signal, useInput);
	ArrayList<Amplifier> candidatesCorrectOutput = new ArrayList<Amplifier>();

	for (int i = 0; i < candidates.length; i++) {
	    if (candidates[i].getOutputPower() < (maxOutputPower + 0.5f))
		candidatesCorrectOutput.add(candidates[i]);
	}

	candidates = new Amplifier[candidatesCorrectOutput.size()];
	candidatesCorrectOutput.toArray(candidates);

	return candidates;
    }

    /**
     * Calculate the tilt of the signal
     * 
     * @param outputPower
     *            Vector with the channel powers
     * @return The tilt in dB
     */
    protected float calculateRipple(double[] outputPower) {
	int maior = 0, menor = 0;
	for (int i = 1; i < outputPower.length; i++) {
	    if (outputPower[i] < outputPower[menor])
		menor = i;
	    if (outputPower[i] > outputPower[maior])
		maior = i;
	}

	double tilt = outputPower[maior] / outputPower[menor];
	return (float) (DecibelConverter.toDecibelScale(tilt));
    }

    /**
     * Calculate the maximum noise figure of the signal
     * 
     * @param noiseFigure
     * @return Maximum noise figure in dB
     */
    protected float calculateNFMax(double[] noiseFigure) {
	int maxIndex = 0;
	for (int i = 1; i < noiseFigure.length; i++) {
	    if (noiseFigure[i] > noiseFigure[maxIndex])
		maxIndex = i;
	}

	return (float) noiseFigure[maxIndex];
    }
}
