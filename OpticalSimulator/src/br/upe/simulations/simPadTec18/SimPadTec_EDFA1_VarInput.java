package br.upe.simulations.simPadTec18;

import java.io.File;
import java.io.FileNotFoundException;
import java.text.NumberFormat;
import java.util.ArrayList;
import java.util.Scanner;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalSignal;
import br.upe.objfunctions.linerInterpolation.LinearInterpolationFunction;
import br.upe.signal.factory.CustomSignal;
import br.upe.util.SignalFeatureCalculation;

public class SimPadTec_EDFA1_VarInput {
    public static void main(String[] args) {

	ObjectiveFunction functionAux = new LinearInterpolationFunction();

	double[] frequency = { 192.1e12, 192.2e12, 192.3e12, 192.4e12, 192.5e12, 192.6e12, 192.7e12, 192.8e12, 192.9e12,
		193e12, 193.1e12, 193.2e12, 193.3e12, 193.4e12, 193.5e12, 193.6e12, 193.7e12, 193.8e12, 193.9e12,
		194e12, 194.1e12, 194.2e12, 194.3e12, 194.4e12, 194.5e12, 194.6e12, 194.7e12, 194.8e12, 194.9e12,
		195e12, 195.1e12, 195.2e12, 195.3e12, 195.4e12, 195.5e12, 195.6e12, 195.7e12, 195.8e12, 195.9e12,
		196e12 };
	int gain = 14;

	// Ler arquivo com sinais de entrada e saida
	ArrayList<double[]> inputSignals = new ArrayList<double[]>();
	ArrayList<double[]> outputSignals = new ArrayList<double[]>();
	File file = new File("signalVariable.txt");
	Scanner reader = null;
	try {
	    reader = new Scanner(file);
	} catch (FileNotFoundException e) {
	    // TODO Auto-generated catch block
	    e.printStackTrace();
	}

	boolean input = true;
	double[] tempInput = new double[40];
	double[] tempOutput = new double[40];
	while (reader.hasNextLine()) {
	    String[] line = reader.nextLine().split("\t");
	    for (int i = 0; i < line.length; i++) {
		if (input)
		    tempInput[i] = Double.parseDouble(line[i]);
		else
		    tempOutput[i] = Double.parseDouble(line[i]);
	    }
	    if (input)
		inputSignals.add(tempInput.clone());
	    else
		outputSignals.add(tempOutput.clone());
	    input = !input;
	}

	reader.close();

	System.out.println("------");
	System.out.println("Freq. \t Pout_optSystem \t Pout_estimado");
	System.out.println("------");

	StringBuffer strBuff = new StringBuffer();
	NumberFormat nf = NumberFormat.getInstance();
	nf.setMaximumFractionDigits(3);

	ArrayList<Amplifier> amplifiers = new ArrayList<Amplifier>();

	for (int i = 0; i < inputSignals.size(); i++) {
	    // Para cada sinal de entrada definido no arquivo
	    CustomSignal signal = new CustomSignal(frequency, inputSignals.get(i), 40);
	    OpticalSignal inputSignal = signal.createSignal();
	    OpticalSignal outputSignal = null;

	    double tiltAvaliacao = 0;
	    do {
		// Calcular tilt para escolher máscara
		double tilt = SignalFeatureCalculation.calculateTiltNonLinearReg(inputSignal);
		AmplifierType type = getAmplifierType(tilt);

		// Passar sinal pelo amplificador
		Amplifier amplifier = new Amplifier(inputSignal.getTotalPower(), gain, type);
		functionAux.defineNewOperationPoint(amplifier, inputSignal);
		outputSignal = amplifier.transferFunction(inputSignal);

		// Colocar saída do amplificador como entrada do seguinte,
		// passando pela fibra
		SignalFeatureCalculation.linkTrasferFunction(gain, outputSignal);
		inputSignal = outputSignal;
		tiltAvaliacao = SignalFeatureCalculation.calculateTiltFixed(outputSignal);
	    } while (tiltAvaliacao < 20);

	    // Calcular tilt no sinal de saída
	    signal = new CustomSignal(frequency, outputSignals.get(i), 40);
	    OpticalSignal outputOptSys = signal.createSignal();
	    double tiltOptiSys = SignalFeatureCalculation.calculateTiltFixed(outputOptSys);

	    // Imprimir tilts
	    strBuff.append((i + 1) + "\t" + nf.format(tiltOptiSys) + "\t" + nf.format(tiltAvaliacao) + "\n");
	    System.out.println("# Signal " + (i + 1));
	    // Imprimir espectros
	    for (int j = 0; j < frequency.length; j++) {
		System.out.printf("%2.3f\t%2.3f\t%2.3f\n", (frequency[j] / 1e12),
			outputOptSys.getChannels().get(j).getSignalPower(),
			outputSignal.getChannels().get(j).getSignalPower());
	    }
	}

	System.out.println("\n------");
	System.out.println("Signal \t tilt_optSystem \t tilt_estimado");
	System.out.println("------");
	System.out.println(strBuff);
    }

    private static AmplifierType getAmplifierType(double tilt) {
	if (tilt < 0) {
	    if (tilt < -12.5)
		return AmplifierType.EDFA_1_Tm25_PadTec;
	} else {
	    if (tilt > 7.5)
		return AmplifierType.EDFA_1_T15_PadTec;
	}

	return AmplifierType.EDFA_1_PadTec;
    }
}
