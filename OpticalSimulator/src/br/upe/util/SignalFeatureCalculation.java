package br.upe.util;

import java.util.ArrayList;

import br.upe.base.OpticalChannel;
import br.upe.base.OpticalSignal;
import main.java.org.orangepalantir.leastsquares.Function;
import main.java.org.orangepalantir.leastsquares.fitters.NonLinearSolver;
import main.java.org.orangepalantir.leastsquares.functions.ExponentialFunction;

public class SignalFeatureCalculation {

    /**
     * Calculates the power difference between the first and last channel.
     * 
     * @param signal
     * @return
     */
    public static double calculateTiltFixed(OpticalSignal signal) {
	OpticalChannel first = signal.getChannels().get(0);
	OpticalChannel last = signal.getChannels().get(signal.getChannels().size() - 1);

	double firstSignal = DecibelConverter.toLinearScale(first.getSignalPower());
	double lastSignal = DecibelConverter.toLinearScale(last.getSignalPower());

	double maxPeak, minPeak, tiltSignal;

	if (firstSignal > lastSignal) {
	    maxPeak = firstSignal;
	    minPeak = lastSignal;
	    tiltSignal = 1;
	} else {
	    maxPeak = lastSignal;
	    minPeak = firstSignal;
	    tiltSignal = -1.0;
	}

	return tiltSignal * DecibelConverter.toDecibelScale(maxPeak / minPeak);
    }

    /**
     * Calculates the power difference between the average of the three first
     * and three last channels.
     * 
     * @param signal
     * @return
     */
    public static double calculateTiltAverage(OpticalSignal signal) {
	double firstSignal = 1, lastSignal = 1;

	for (int i = 0; i < 3; i++) {
	    OpticalChannel first = signal.getChannels().get(i);
	    OpticalChannel last = signal.getChannels().get(signal.getChannels().size() - 1 - i);

	    firstSignal += first.getSignalPower();
	    lastSignal += last.getSignalPower();
	}

	firstSignal /= 3.0;
	lastSignal /= 3.0;

	firstSignal = DecibelConverter.toLinearScale(firstSignal);
	lastSignal = DecibelConverter.toLinearScale(lastSignal);

	double maxPeak, minPeak;
	double tiltSignal = 1.0;

	if (firstSignal > lastSignal) {
	    maxPeak = firstSignal;
	    minPeak = lastSignal;
	} else {
	    maxPeak = lastSignal;
	    minPeak = firstSignal;
	    tiltSignal = -1.0;
	}

	return tiltSignal * DecibelConverter.toDecibelScale(maxPeak / minPeak);
    }

    /**
     * Calculates the power difference between the channel with highest and
     * lowest power.
     * 
     * @param signal
     * @return
     */
    public static double calculateTiltFree(OpticalSignal signal) {
	double maxPeak = Double.MIN_VALUE;
	double minPeak = Double.MAX_VALUE;

	for (OpticalChannel c : signal.getChannels()) {
	    double signalLin = DecibelConverter.toLinearScale(c.getSignalPower());

	    if (signalLin > maxPeak) {
		maxPeak = signalLin;
	    }
	    if (signalLin < minPeak) {
		minPeak = signalLin;
	    }
	}

	return DecibelConverter.toDecibelScale(maxPeak / minPeak);
    }

    public static double calculateTiltLinearReg(OpticalSignal signal) {
	ArrayList<OpticalChannel> channels = signal.getChannels();
	double[] frequencies = new double[channels.size()];
	double[] power = new double[channels.size()];

	int indexMaxFreq = 0, indexMinFreq = 0;


	for (int i = 0; i < power.length; i++) {
	    frequencies[i] = channels.get(i).getFrequency();
	    power[i] = channels.get(i).getSignalPower();

	    if (frequencies[i] < frequencies[indexMinFreq])
		indexMinFreq = i;
	    else if (frequencies[i] > frequencies[indexMaxFreq])
		indexMaxFreq = i;
	}

	// normalizing frequencies
	double maxFreq = frequencies[indexMaxFreq];
	double minFreq = frequencies[indexMinFreq];
	for (int i = 0; i < frequencies.length; i++) {
	    frequencies[i] = (frequencies[i] - minFreq) / (maxFreq - minFreq);
	}

	LinearRegression lr = new LinearRegression(frequencies, power);

	return -1.0 * lr.slope();
    }

    public static double calculateTiltNonLinearReg(OpticalSignal signal) {
	ArrayList<OpticalChannel> channels = signal.getChannels();
	double[] frequencies = new double[channels.size()];
	double[] power = new double[channels.size()];

	int indexMaxFreq = 0, indexMinFreq = 0;

	for (int i = 0; i < power.length; i++) {
	    frequencies[i] = channels.get(i).getFrequency();
	    power[i] = channels.get(i).getSignalPower();

	    if (frequencies[i] < frequencies[indexMinFreq])
		indexMinFreq = i;
	    else if (frequencies[i] > frequencies[indexMaxFreq])
		indexMaxFreq = i;
	}

	// normalizing frequencies
	double maxFreq = frequencies[indexMaxFreq];
	double minFreq = frequencies[indexMinFreq];
	for (int i = 0; i < frequencies.length; i++) {
	    frequencies[i] = (frequencies[i] - minFreq) / (maxFreq - minFreq);
	}

	Function exponential = new ExponentialFunction();
	NonLinearSolver non_linear = new NonLinearSolver(exponential);
	double[][] x = new double[frequencies.length][1];
	for (int i = 0; i < frequencies.length; i++) {
	    x[i][0] = frequencies[i];
	}
	non_linear.setData(x, signalToLinear(power));

	// it kinda takes a good guess.
	non_linear.setParameters(new double[] { 1, -1 });

	// coarse fit.
	non_linear.fitData();

	double[] results = non_linear.getParameters();

	double value = results[0] * Math.exp(frequencies[0] * results[1]);
	value = DecibelConverter.toDecibelScale(value);

	double value2 = results[0] * Math.exp(frequencies[frequencies.length - 1] * results[1]);
	value2 = DecibelConverter.toDecibelScale(value2);

	return (value - value2);
    }

    private static double[] signalToLinear(double[] ds) {
	double[] ret = new double[ds.length];
	for (int i = 0; i < ds.length; i++) {
	    ret[i] = DecibelConverter.toLinearScale(ds[i]);
	}
	return ret;
    }

    public static double[] calculateOSNR(OpticalSignal signal) {
	double[] OSNR = new double[signal.getChannels().size()];
	int i = 0;
	for (OpticalChannel c : signal.getChannels()) {
	    double signalLin = DecibelConverter.toLinearScale(c.getSignalPower());
	    double noiseLin = DecibelConverter.toLinearScale(c.getNoisePower());
	    OSNR[i++] = DecibelConverter.toDecibelScale(signalLin / noiseLin);
	}

	return OSNR;
    }

    public static double calculateMinOSNR(OpticalSignal signal) {
	double minOSNR = Double.MAX_VALUE;
	for (OpticalChannel c : signal.getChannels()) {
	    double signalLin = DecibelConverter.toLinearScale(c.getSignalPower());
	    double noiseLin = DecibelConverter.toLinearScale(c.getNoisePower());
	    double OSNR = signalLin / noiseLin;

	    if (OSNR < minOSNR) {
		minOSNR = OSNR;
	    }
	}

	return DecibelConverter.toDecibelScale(minOSNR);
    }

    public static void linkTrasferFunction(float linkLoss, OpticalSignal signal) {
	for (OpticalChannel c : signal.getChannels()) {
	    // Signal Total Gain
	    double signalLin = DecibelConverter.toLinearScale(c.getSignalPower());
	    signalLin *= DecibelConverter.toLinearScale(-1 * linkLoss);
	    // Noise Gain
	    double noiseLin = DecibelConverter.toLinearScale(c.getNoisePower());
	    noiseLin *= DecibelConverter.toLinearScale(-1 * linkLoss);

	    c.setSignalPower(DecibelConverter.toDecibelScale(signalLin));
	    c.setNoisePower(DecibelConverter.toDecibelScale(noiseLin));
	}
    }

    public static double calculateTiltOSNRFixed(OpticalSignal ampInput) {
	OpticalChannel c1 = ampInput.getChannels().get(0);
	OpticalChannel c2 = ampInput.getChannels().get(ampInput.getChannels().size() - 1);

	double signalLin = DecibelConverter.toLinearScale(c1.getSignalPower());
	double noiseLin = DecibelConverter.toLinearScale(c1.getNoisePower());
	double OSNR = signalLin / noiseLin;

	signalLin = DecibelConverter.toLinearScale(c2.getSignalPower());
	noiseLin = DecibelConverter.toLinearScale(c2.getNoisePower());
	OSNR /= (signalLin / noiseLin);

	return DecibelConverter.toDecibelScale(OSNR);
    }

}
