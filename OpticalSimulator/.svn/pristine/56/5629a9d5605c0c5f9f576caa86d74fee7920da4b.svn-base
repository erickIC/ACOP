package br.upe.mascara;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;

import br.upe.base.AmplifierType;

public class TransformPowerMaskToRNFile_PinParImpar {

	public static void main(String[] args) {
		PowerMask pm = PowerMaskFactory.getInstance().fabricatePowerMask(AmplifierType.EDFA_1_STG_PAR);

		File fileImpar = new File("EDFA_1_STG_Pin_Par.txt");
		// File filePar = new File("EDFA_1_STG_Pin_Par.txt");

		boolean useFilter = false;

		PrintWriter printerI = null;
		// PrintWriter printerP = null;
		try {
			printerI = new PrintWriter(fileImpar);
			// printerP = new PrintWriter(filePar);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}

		Collections.shuffle(pm.getOperatingPoints());

		for (int j = 0; j < pm.getOperatingPoints().size(); j++) {
			OperatingPoint op = pm.getOperatingPoints().get(j);
			Collection<Double> frequencys = op.getGainPerChannel().keySet();
			List<Double> freqList = new ArrayList<Double>(frequencys);

			Collections.sort(freqList);

			float[] gainChFiltred = new float[freqList.size()];
			float[] nfFiltred = new float[freqList.size()];

			for (int i = 0; i < freqList.size(); i++) {
				printerI.print(op.getGainSet() + "\t");
				printerI.print(op.getTotalInputPower() + "\t");
				printerI.print(freqList.get(i) + "\t");
				/*
				 * if ((j + 1) % 2 == 0) { printerI.print(op.getGainSet() +
				 * "\t"); printerI.print(op.getTotalInputPower() + "\t");
				 * printerI.print(freqList.get(i) + "\t"); } else {
				 * printerP.print(op.getGainSet() + "\t");
				 * printerP.print(op.getTotalInputPower() + "\t");
				 * printerP.print(freqList.get(i) + "\t"); }
				 */

				if (i == 0 || i == freqList.size() - 1 || !useFilter) {
					gainChFiltred[i] = op.getGainPerChannel().get(freqList.get(i));
					nfFiltred[i] = op.getNoiseFigurePerChannel().get(freqList.get(i));
				} else {
					// Applying the mean filter (attenuation filter)
					float gainCh = op.getGainPerChannel().get(freqList.get(i));
					gainCh += gainChFiltred[i - 1];
					gainCh += op.getGainPerChannel().get(freqList.get(i + 1));
					gainCh /= 3.0f;

					gainChFiltred[i] = gainCh;

					float nf = op.getNoiseFigurePerChannel().get(freqList.get(i));
					nf += nfFiltred[i - 1];
					nf += op.getNoiseFigurePerChannel().get(freqList.get(i + 1));
					nf /= 3.0f;

					nfFiltred[i] = nf;
				}
				
				/*if ((j + 1) % 2 == 0) {
					printerI.print(gainChFiltred[i] + "\t");
					printerI.println(nfFiltred[i]);
				} else {
					printerP.print(gainChFiltred[i] + "\t");
					printerP.println(nfFiltred[i]);
				}*/
				printerI.print(gainChFiltred[i] + "\t");
				printerI.println(nfFiltred[i]);

			}
		}

		printerI.close();
		// printerP.close();
	}

}
