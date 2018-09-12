package br.teste.upe;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

import br.upe.util.DecibelConverter;
import main.java.org.orangepalantir.leastsquares.Function;
import main.java.org.orangepalantir.leastsquares.fitters.NonLinearSolver;
import main.java.org.orangepalantir.leastsquares.functions.ExponentialFunction;

public class CalculateTiltOptiSystem {

    public static void main(String[] args) {

	// criar array com frequencias normalizadas
	double[] x_old = { 0.0, 0.02564102564102564, 0.05128205128205128, 0.07692307692307693, 0.10256410256410256,
		0.1282051282051282, 0.15384615384615385, 0.1794871794871795, 0.20512820512820512, 0.23076923076923078,
		0.2564102564102564, 0.28205128205128205, 0.3076923076923077, 0.3333333333333333, 0.358974358974359,
		0.38461538461538464, 0.41025641025641024, 0.4358974358974359, 0.46153846153846156, 0.48717948717948717,
		0.5128205128205128, 0.5384615384615384, 0.5641025641025641, 0.5897435897435898, 0.6153846153846154,
		0.6410256410256411, 0.6666666666666666, 0.6923076923076923, 0.717948717948718, 0.7435897435897436,
		0.7692307692307693, 0.7948717948717948, 0.8205128205128205, 0.8461538461538461, 0.8717948717948718,
		0.8974358974358975, 0.9230769230769231, 0.9487179487179487, 0.9743589743589743, 1.0 };

	// para cada saida do optisistem:
	// calcular o titl e imprimir
	double[][] signals = null;
	try {
	    signals = readSignal(20, 40);
	} catch (FileNotFoundException e) {
	    // TODO Auto-generated catch block
	    e.printStackTrace();
	}
	double[][] x = new double[x_old.length][1];
	for (int i = 0; i < x_old.length; i++) {
	    x[i][0] = x_old[i];
	}

	Function exponential = new ExponentialFunction();
	NonLinearSolver non_linear = new NonLinearSolver(exponential);

	for (int i = 0; i < signals.length; i++) {

	    non_linear.setData(x, signalToLinear(signals[i]));

	    // it kinda takes a good guess.
	    non_linear.setParameters(new double[] { 1, -1 });

	    // coarse fit.
	    non_linear.fitData();

	    double[] results = non_linear.getParameters();

	    double value = results[0] * Math.exp(x_old[0] * results[1]);
	    value = DecibelConverter.toDecibelScale(value);

	    double value2 = results[0] * Math.exp(x_old[x_old.length - 1] * results[1]);
	    value2 = DecibelConverter.toDecibelScale(value2);

	    System.out.printf("%2.3f\t%2.3f\t%2.3f\t%2.3f\n", (value - value2), results[0], results[1],
		    non_linear.calculateErrors());
	}
    }

    private static double[] signalToLinear(double[] ds) {
	double[] ret = new double[ds.length];
	for (int i = 0; i < ds.length; i++) {
	    ret[i] = DecibelConverter.toLinearScale(ds[i]);
	}
	return ret;
    }

    private static double[][] readSignal(int numberSignals, int numberChannels) throws FileNotFoundException {
	double[][] signals = new double[numberSignals][numberChannels];

	File file = new File("signals.txt");
	Scanner reader = new Scanner(file);

	int index = 0;
	while (reader.hasNextLine() && index < numberSignals) {
	    String[] line = reader.nextLine().split("\t");
	    for (int i = 0; i < line.length; i++) {
		signals[index][i] = Double.parseDouble(line[i]);
	    }
	    index++;
	}

	reader.close();

	return signals;
    }

}
