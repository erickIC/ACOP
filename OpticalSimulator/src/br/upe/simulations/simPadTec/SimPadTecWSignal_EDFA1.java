package br.upe.simulations.simPadTec;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalChannel;
import br.upe.base.OpticalSignal;
import br.upe.objfunctions.linerInterpolation.LinearInterpolationFunction;
import br.upe.signal.factory.CustomSignal;
import br.upe.util.DecibelConverter;
import br.upe.util.SignalFeatureCalculation;

public class SimPadTecWSignal_EDFA1 {
    private static final int MAX_AMP = 20;
    private static final String FILE_SUFIX = "varGains2";

    public static void main(String[] args) {
	double[] frequency = { 192.1e12, 192.2e12, 192.3e12, 192.4e12, 192.5e12, 192.6e12, 192.7e12, 192.8e12, 192.9e12,
		193e12, 193.1e12, 193.2e12, 193.3e12, 193.4e12, 193.5e12, 193.6e12, 193.7e12, 193.8e12, 193.9e12,
		194e12, 194.1e12, 194.2e12, 194.3e12, 194.4e12, 194.5e12, 194.6e12, 194.7e12, 194.8e12, 194.9e12,
		195e12, 195.1e12, 195.2e12, 195.3e12, 195.4e12, 195.5e12, 195.6e12, 195.7e12, 195.8e12, 195.9e12,
		196e12 };

	// G14@16dBm
	/*double[] signalPower = { -14.024605, -14.028875, -14.023219, -14.026891, -14.02502, -14.02137, -14.02473,
		-14.027222, -14.022975, -14.02314, -14.024824, -14.025928, -14.026592, -14.026278, -14.02552,
		-14.027601, -14.029779, -14.025141, -14.022104, -14.028345, -14.021887, -14.027182, -14.025332,
		-14.024798, -14.02708, -14.025339, -14.024127, -14.023705, -14.024369, -14.023563, -14.025313,
		-14.025937, -14.020915, -14.026135, -14.025844, -14.023048, -14.023051, -14.027951, -14.027024,
		-14.024125 }; */

	// G20@16dBm
	/*double[] signalPower = { -20.025092, -20.021728, -20.022224, -20.031265, -20.022239, -20.027141, -20.026382,
		-20.030923, -20.028404, -20.026137, -20.022242, -20.023396, -20.036137, -20.025501, -20.02247,
		-20.025408, -20.030799, -20.023686, -20.021555, -20.023588, -20.024153, -20.026078, -20.028377,
		-20.027062, -20.023553, -20.021099, -20.024659, -20.023461, -20.026288, -20.023532, -20.034978,
		-20.029988, -20.020439, -20.029406, -20.024788, -20.024882, -20.026718, -20.021866, -20.022276,
		-20.027701 };*/

	// VarGains2
	double[] signalPower = { -14.026399, -14.027312, -14.021201, -14.025083, -14.026052, -14.022385, -14.030815,
		-14.024419, -14.02598, -14.025135, -14.022469, -14.024351, -14.031226, -14.027681, -14.021254,
		-14.024779, -14.023546, -14.025254, -14.023568, -14.025513, -14.022224, -14.027749, -14.024848,
		-14.031543, -14.029478, -14.026741, -14.02378, -14.025019, -14.02496, -14.027533, -14.021969, -14.02758,
		-14.025173, -14.025364, -14.021813, -14.023514, -14.022609, -14.026529, -14.024937, -14.025318 };

	/* Var Gains
	 * double[] signalPower = { -19.022781, -19.029764, -19.027329, -19.025059, -19.021674, -19.033985, -19.032455,
		-19.022807, -19.0219, -19.023694, -19.024141, -19.026583, -19.02655, -19.022424, -19.02055, -19.025278,
		-19.02604, -19.023258, -19.028556, -19.022145, -19.027095, -19.022143, -19.021354, -19.029566,
		-19.027837, -19.026646, -19.022782, -19.024506, -19.02549, -19.024855, -19.020844, -19.025719,
		-19.023485, -19.02499, -19.02338, -19.027223, -19.022108, -19.02633, -19.028155, -19.023855 };
	
	double[] noisePower = { -60.714894, -68.112932, -64.531787, -68.065328, -66.908441, -66.179224, -65.304661,
		-63.428967, -61.037253, -64.724589, -59.553533, -61.992345, -63.631829, -61.128763, -62.979851,
		-60.741492, -64.000216, -63.517971, -64.240726, -64.654354, -64.279422, -64.81207, -64.530765,
		-62.247209, -62.706012, -64.467091, -63.822295, -64.092683, -60.772164, -62.286127, -65.442052,
		-62.844168, -64.333546, -65.237673, -66.616216, -67.499696, -65.82394, -65.400022, -68.440265,
		-67.685778 };
	 */

	CustomSignal signal = new CustomSignal(frequency, signalPower, 50);
	OpticalSignal inputSignal = signal.createSignal();
	ObjectiveFunction functionAux = new LinearInterpolationFunction();

	double gfM = Double.MAX_VALUE;

	Amplifier[] amplifiers = new Amplifier[MAX_AMP];

	int[] gains = { 14, 24, 14, 24, 14, 24, 14, 24, 14, 24, 14, 24, 14, 24, 14, 24, 14, 24, 14, 24 };
	int[] losses = { 24, 14, 24, 14, 24, 14, 24, 14, 24, 14, 24, 14, 24, 14, 24, 14, 24, 14, 24 };
	// int gain = 20;
	// int loss = 20;

	// System.out.println("*******\nTilt_aval | MAPE | WAE | Tilt_deci |
	// Type\n*******");

	OpticalSignal ampInput = inputSignal.clone();

	StringBuffer strBffSignals = new StringBuffer();

	System.out.println("***\tMascara_4_12dB\t***");

	for (int i = 0; i < MAX_AMP; i++) {
	    double tilt = SignalFeatureCalculation.calculateTiltNonLinearReg(ampInput);

	    AmplifierType type = getAmplifierType4_12(tilt);

	    amplifiers[i] = new Amplifier(ampInput.getTotalPower(), gains[i], type);
	    functionAux.defineNewOperationPoint(amplifiers[i], ampInput);
	    ampInput = amplifiers[i].transferFunction(ampInput);

	    try {
		double erro = calculateMAPE(ampInput.getChannels(), i);

		double[] osnr = SignalFeatureCalculation.calculateOSNR(ampInput);
		double osnrErro = calculateOSNRWAE(osnr, i);

		double tiltOsnr = SignalFeatureCalculation.calculateTiltOSNRFixed(ampInput);
		gfM = SignalFeatureCalculation.calculateTiltFixed(ampInput);

		System.out.printf("%2.3f\t%2.3f\t%2.3f\t%2.3f\t%2.3f\t%2.3f\t", gfM, erro,
			calculateWAE(ampInput.getChannels(), i), tilt, osnrErro, tiltOsnr);
		System.out.println(amplifiers[i].getType());

		strBffSignals.append("#" + (i + 1) + "\t" + ampInput + "\n");
		if (i == MAX_AMP - 1) {
		    System.out.print(strBffSignals);
		}

	    } catch (FileNotFoundException e) {
		e.printStackTrace();
	    }
	    if (i < amplifiers.length - 1)
		SignalFeatureCalculation.linkTrasferFunction(losses[i], ampInput);
	}

    }

    private static double calculateMSE(ArrayList<OpticalChannel> channels, int indexAmp) throws FileNotFoundException {
	double[][] optiSystemSignals = readSignal(MAX_AMP, channels.size());

	double erro = 0;
	for (int i = 0; i < optiSystemSignals[indexAmp].length; i++) {
	    erro += (channels.get(i).getSignalPower() - optiSystemSignals[indexAmp][i])
		    * (channels.get(i).getSignalPower() - optiSystemSignals[indexAmp][i]);
	}

	return (erro / (optiSystemSignals[indexAmp].length * 1.0));
    }

    /**
     * Mean Absolute Percentage Error
     * 
     * @param channels
     * @param indexAmp
     * @return
     * @throws FileNotFoundException
     */
    private static double calculateMAPE(ArrayList<OpticalChannel> channels, int indexAmp) throws FileNotFoundException {
	double[][] optiSystemSignals = readSignal(MAX_AMP, channels.size());

	double error = 0;
	for (int i = 0; i < optiSystemSignals[indexAmp].length; i++) {
	    double chPowerLin = DecibelConverter.toLinearScale(channels.get(i).getSignalPower());
	    double optSPowerLin = DecibelConverter.toLinearScale(optiSystemSignals[indexAmp][i]);
	    error += Math.abs(optSPowerLin - chPowerLin) / optSPowerLin;
	}

	return (error / optiSystemSignals[indexAmp].length);
    }

    /**
     * OSNR Worst Absolute Error
     * 
     * @param osnr
     * @param indexAmp
     * @return
     * @throws FileNotFoundException
     */
    private static double calculateOSNRWAE(double[] osnr, int indexAmp) throws FileNotFoundException {
	double[][] optiSystemOSNR = readOSNR(MAX_AMP, osnr.length);

	double maxError = 0;
	int maxIndex = 0;
	for (int i = 0; i < optiSystemOSNR[indexAmp].length; i++) {
	    double chOSNRLin = DecibelConverter.toLinearScale(osnr[i]);
	    double optSOSNRLin = DecibelConverter.toLinearScale(optiSystemOSNR[indexAmp][i]);
	    double error = optSOSNRLin - chOSNRLin;

	    if (Math.abs(error) > maxError)
		maxIndex = i;

	}

	return (optiSystemOSNR[indexAmp][maxIndex] - osnr[maxIndex]);
    }

    /**
     * Worst absolute Error
     * 
     * @param channels
     * @param indexAmp
     * @return
     * @throws FileNotFoundException
     */
    private static double calculateWAE(ArrayList<OpticalChannel> channels, int indexAmp)
	    throws FileNotFoundException {
	double[][] optiSystemSignals = readSignal(MAX_AMP, channels.size());

	double maxError = 0;
	for (int i = 0; i < optiSystemSignals[indexAmp].length; i++) {
	    double chPowerLin = channels.get(i).getSignalPower();
	    double optSPowerLin = optiSystemSignals[indexAmp][i];
	    double error = Math.abs(optSPowerLin - chPowerLin);

	    if (error > maxError)
		maxError = error;
	}

	return maxError;
    }

    /**
     * Worst absolute Error
     * 
     * @param channels
     * @param indexAmp
     * @return
     * @throws FileNotFoundException
     */
    private static double calculateWAELin(ArrayList<OpticalChannel> channels, int indexAmp)
	    throws FileNotFoundException {
	double[][] optiSystemSignals = readSignal(MAX_AMP, channels.size());

	double maxError = 0;
	for (int i = 0; i < optiSystemSignals[indexAmp].length; i++) {
	    double chPowerLin = DecibelConverter.toLinearScale(channels.get(i).getSignalPower());
	    double optSPowerLin = DecibelConverter.toLinearScale(optiSystemSignals[indexAmp][i]);
	    double error = Math.abs(optSPowerLin - chPowerLin);

	    if (error > maxError)
		maxError = error;
	}

	return DecibelConverter.toDecibelScale(maxError);
    }

    private static double[][] readSignal(int numberSignals, int numberChannels) throws FileNotFoundException {
	double[][] signals = new double[numberSignals][numberChannels];

	File file = new File("signals_" + FILE_SUFIX + ".txt");
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

    private static double[][] readOSNR(int numberSignals, int numberChannels) throws FileNotFoundException {
	double[][] signals = new double[numberSignals][numberChannels];

	File file = new File("osnr_" + FILE_SUFIX + ".txt");
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

    private static AmplifierType getAmplifierTypeFromTwoMasks(double tiltSignal, double tiltSecondMask,
	    AmplifierType typeSecondMask) {
	tiltSecondMask /= 2.0;

	if (Math.abs(tiltSignal) < Math.abs(tiltSecondMask))
	    return AmplifierType.EDFA_1_PadTec;

	return typeSecondMask;
    }

    private static AmplifierType getAmplifierType1dB(double tilt) {
	if (tilt >= 0)
	    return getAmplifierType1dBPositive(tilt);
	else
	    return getAmplifierType1dBNegative(-1 * tilt);
    }

    private static AmplifierType getAmplifierType4_12(double tilt) {
	if (tilt < 0) {
	    tilt *= -1;
	    if (tilt < 2)
		return AmplifierType.EDFA_1_PadTec;
	    else if (tilt >= 2 && tilt < 8)
		return AmplifierType.EDFA_1_Tm4_PadTec;
	    else
		return AmplifierType.EDFA_1_Tm12_PadTec;
	} else {
	    if (tilt < 2)
		return AmplifierType.EDFA_1_PadTec;
	    else if (tilt >= 2 && tilt < 8)
		return AmplifierType.EDFA_1_T4_PadTec;
	    else
		return AmplifierType.EDFA_1_T12_PadTec;
	}
    }

    private static AmplifierType getAmplifierType1dBPositive(double tilt) {
	int tiltRounded = Math.round((float) tilt);

	switch (tiltRounded) {
	case 0:
	    return AmplifierType.EDFA_1_PadTec;
	case 1:
	    return AmplifierType.EDFA_1_T1_PadTec;
	case 2:
	    return AmplifierType.EDFA_1_T2_PadTec;
	case 3:
	    return AmplifierType.EDFA_1_T3_PadTec;
	case 4:
	    return AmplifierType.EDFA_1_T4_PadTec;
	case 5:
	    return AmplifierType.EDFA_1_T5_PadTec;
	case 6:
	    return AmplifierType.EDFA_1_T6_PadTec;
	case 7:
	    return AmplifierType.EDFA_1_T7_PadTec;
	case 8:
	    // default:
	    return AmplifierType.EDFA_1_T8_PadTec;
	case 9:
	    return AmplifierType.EDFA_1_T9_PadTec;
	case 10:
	    return AmplifierType.EDFA_1_T10_PadTec;
	case 11:
	    return AmplifierType.EDFA_1_T11_PadTec;
	case 12:
	    return AmplifierType.EDFA_1_T12_PadTec;
	case 13:
	    return AmplifierType.EDFA_1_T13_PadTec;
	case 14:
	    return AmplifierType.EDFA_1_T14_PadTec;
	case 15:
	    return AmplifierType.EDFA_1_T15_PadTec;
	case 17:
	    return AmplifierType.EDFA_1_T17_PadTec;
	case 20:
	    return AmplifierType.EDFA_1_T20_PadTec;
	case 25:
	    return AmplifierType.EDFA_1_T25_PadTec;
	case 30:
	default:
	    return AmplifierType.EDFA_1_T30_PadTec;
	}
    }

    private static AmplifierType getAmplifierType1dBNegative(double tilt) {
	int tiltRounded = Math.round((float) tilt);

	switch (tiltRounded) {
	case 0:
	    return AmplifierType.EDFA_1_PadTec;
	case 1:
	    return AmplifierType.EDFA_1_Tm1_PadTec;
	case 2:
	    return AmplifierType.EDFA_1_Tm2_PadTec;
	case 3:
	    return AmplifierType.EDFA_1_Tm3_PadTec;
	case 4:
	    return AmplifierType.EDFA_1_Tm4_PadTec;
	case 5:
	    return AmplifierType.EDFA_1_Tm5_PadTec;
	case 6:
	    return AmplifierType.EDFA_1_Tm6_PadTec;
	case 7:
	    return AmplifierType.EDFA_1_Tm7_PadTec;
	case 8:
	    return AmplifierType.EDFA_1_Tm8_PadTec;
	case 9:
	    return AmplifierType.EDFA_1_Tm9_PadTec;
	case 10:
	    return AmplifierType.EDFA_1_Tm10_PadTec;
	case 11:
	    return AmplifierType.EDFA_1_Tm11_PadTec;
	case 12:
	    return AmplifierType.EDFA_1_Tm12_PadTec;
	case 13:
	    return AmplifierType.EDFA_1_Tm13_PadTec;
	case 14:
	    return AmplifierType.EDFA_1_Tm14_PadTec;
	case 15:
	    return AmplifierType.EDFA_1_Tm15_PadTec;
	case 16:
	    return AmplifierType.EDFA_1_Tm16_PadTec;
	case 17:
	    return AmplifierType.EDFA_1_Tm17_PadTec;
	case 18:
	    return AmplifierType.EDFA_1_Tm18_PadTec;
	case 19:
	    return AmplifierType.EDFA_1_Tm19_PadTec;
	case 20:
	    return AmplifierType.EDFA_1_Tm20_PadTec;
	case 25:
	    return AmplifierType.EDFA_1_Tm25_PadTec;
	case 30:
	default:
	    return AmplifierType.EDFA_1_Tm30_PadTec;
	}
    }
}
