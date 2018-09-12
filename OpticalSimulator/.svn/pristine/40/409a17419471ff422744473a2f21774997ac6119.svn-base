package br.upe.mascara;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.Scanner;

public class TransformCompletePMFileToOld {

	public static void main(String[] args) {
		try {
			String path = "./masks/05_Com Tilt/EDFA_2/";
			File file = new File("complete_power_mask_edfa2.txt");
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

				for (int i = 0; i < numberOfChannels; i++) {
					String wavelength = line[3 + i + 3 * numberOfChannels];
					
					printerPeakPin.println(wavelength + "\t" + line[3 + i]);
					double pin = Double.parseDouble(line[3 + i]);
					
					printerPeakPout.println(wavelength + "\t" + line[3 + i + numberOfChannels]);
					double pout = Double.parseDouble(line[3 + i + numberOfChannels]);

					gainCh[i] = pout - pin;

					nf[i] = Double.parseDouble(line[3 + i + 2 * numberOfChannels]);
					// If nf is less than 3 dB, it was an error in the
					// characterization
					if (nf[i] < 3)
						nf[i] += 3; // Sum 3 dB or duplicate

					printerNF.println(wavelength + "\t" + nf[i]);
				}

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
