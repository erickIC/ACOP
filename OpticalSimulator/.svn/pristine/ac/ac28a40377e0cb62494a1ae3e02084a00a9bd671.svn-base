package br.upe.mascara;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.Scanner;

public class TransformCompletePMFile_Filter {

	public static void main(String[] args) {
		try {
			String path = "./masks/05_Com Tilt/EDFA_1_STG_FreqImpar_Filt/";
			File file = new File("complete_power_mask.txt");
			File fileTotal = new File(path + "TotalInfo.txt");

			Scanner reader = new Scanner(file);
			PrintWriter totalInfo = new PrintWriter(fileTotal); // G, A, Pin,
																// Pout, NF

			int numberOfChannels = Integer.parseInt(reader.nextLine());
			int gain = 0, aParameter = 0, gainAux = 0;

			while (reader.hasNextLine()) {
				String[] line = reader.nextLine().split("\t"); // Pin, Pout, G,
																// Pin[#ch],
																// Pout[#ch],
																// NF[#ch],
																// WaveL[#ch]

				gainAux = Integer.parseInt(line[2]);

				if (gainAux != gain) {
					gain = gainAux;
					aParameter = 0;
				} else {
					aParameter++;
				}

				totalInfo.print(line[2] + "\t" + aParameter + "\t" + line[0] + "\t" + line[1] + "\t");

				File filePinPeak = new File(path + "PinPeak_G" + gain + "_A" + aParameter + ".txt");
				File filePoutPeak = new File(path + "PoutPeak_G" + gain + "_A" + aParameter + ".txt");
				File fileNF = new File(path + "NF_G" + gain + "_A" + aParameter + ".txt");

				PrintWriter printerPeakPin = new PrintWriter(filePinPeak);
				PrintWriter printerPeakPout = new PrintWriter(filePoutPeak);
				PrintWriter printerNF = new PrintWriter(fileNF);

				double[] nf = new double[numberOfChannels];
				double[] gainCh = new double[numberOfChannels];

				double[] pin = new double[numberOfChannels];
				double[] pout = new double[numberOfChannels];

				String[] wavelength = new String[numberOfChannels];

				for (int i = 0; i < numberOfChannels; i++) {
					wavelength[i] = line[3 + i + 3 * numberOfChannels];
					
					pin[i] = Double.parseDouble(line[3 + i]);
					pout[i] = Double.parseDouble(line[3 + i + numberOfChannels]);

					nf[i] = Double.parseDouble(line[3 + i + 2 * numberOfChannels]);
					// If nf is less than 3 dB, it was an error in the
					// characterization
					if (nf[i] < 3)
						nf[i] += 3; // Sum 3 dB or duplicate
				}

				// printerPeakPin.println(wavelength[0] + "\t" + pin[0]);
				// printerPeakPout.println(wavelength[0] + "\t" + pout[0]);
				// printerNF.println(wavelength[0] + "\t" + nf[0]);

				for (int i = 1; i < numberOfChannels - 1; i += 2) {
					// Applying the mean filter (attenuation filter)
					pin[i] += pin[i - 1] + pin[i + 1];
					pout[i] += pout[i - 1] + pout[i + 1];
					nf[i] += nf[i - 1] + nf[i + 1];

					if (i == 1 || i == (numberOfChannels - 2)) {
						pin[i] /= 3.0f;
						pout[i] /= 3.0f;
						nf[i] /= 3.0f;
					} else {
						pin[i] += pin[i - 2] + pin[i + 2];
						pout[i] += pout[i - 2] + pout[i + 2];
						nf[i] += nf[i - 2] + nf[i + 2];

						pin[i] /= 5.0f;
						pout[i] /= 5.0f;
						nf[i] /= 5.0f;
					}

					gainCh[i] = pout[i] - pin[i];

					printerPeakPin.println(wavelength[i] + "\t" + pin[i]);
					printerPeakPout.println(wavelength[i] + "\t" + pout[i]);
					printerNF.println(wavelength[i] + "\t" + nf[i]);
				}

				//printerPeakPin.println(wavelength[numberOfChannels - 1] + "\t" + pin[numberOfChannels - 1]);
				//printerPeakPout.println(wavelength[numberOfChannels - 1] + "\t" + pout[numberOfChannels - 1]);
				//printerNF.println(wavelength[numberOfChannels - 1] + "\t" + nf[numberOfChannels - 1]);

				printerPeakPin.close();
				printerPeakPout.close();
				printerNF.close();

				totalInfo.println(calcMaxNF(nf) + "\t" + calcTilt(gainCh));
			}

			totalInfo.close();
			reader.close();

		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}

	}

	private static double calcMaxNF(double[] nf) {
		int maxIndex = 0;
		for (int i = 1; i < nf.length; i++) {
			if (nf[i] > nf[maxIndex])
				maxIndex = i;
		}

		return nf[maxIndex];
	}

	private static double calcTilt(double[] pout) {
		int maxIndex = 0, minIndex = 0;
		for (int i = 1; i < pout.length; i++) {
			if (pout[i] > pout[maxIndex])
				maxIndex = i;
			if (pout[i] < pout[minIndex])
				minIndex = i;
		}

		return pout[maxIndex] - pout[minIndex];
	}

}
