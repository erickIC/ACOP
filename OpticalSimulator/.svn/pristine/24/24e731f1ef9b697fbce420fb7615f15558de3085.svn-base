package br.upe.mascara;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;

import br.upe.base.AmplifierType;

public class TransformPowerMaskToRNFile_PinCh {

	public static void main(String[] args) {
		PowerMask pm = PowerMaskFactory.getInstance().fabricatePowerMask(AmplifierType.EDFA_1_STG);

		File file = new File("EDFA_1_STG_PinCh.txt");

		boolean useFilter = false;

		PrintWriter printer = null;
		try {
			printer = new PrintWriter(file);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}

		Collections.shuffle(pm.getOperatingPoints());

		for (int j = 0; j < pm.getOperatingPoints().size(); j++) {
			OperatingPoint op = pm.getOperatingPoints().get(j);
			Collection<Double> frequencys = op.getGainPerChannel().keySet();
			List<Double> freqList = new ArrayList<Double>(frequencys);

			Collections.sort(freqList);

			for (int i = 0; i < freqList.size(); i++) {
				printer.print(op.getGainSet() + "\t");
				printer.print(op.getInputPowerPerChannel().get(freqList.get(i)) + "\t");
				printer.print(freqList.get(i) + "\t");

				float gainCh = 0;
				float nf = 0;
				
				if (i == 0 || i == (freqList.size() - 1) || !useFilter) {
					gainCh = op.getGainPerChannel().get(freqList.get(i));
					nf = op.getNoiseFigurePerChannel().get(freqList.get(i));
				} else {
					// Applying the mean filter (attenuation filter)
					gainCh = op.getGainPerChannel().get(freqList.get(i));
					gainCh += op.getGainPerChannel().get(freqList.get(i - 1));
					gainCh += op.getGainPerChannel().get(freqList.get(i + 1));

					nf = op.getNoiseFigurePerChannel().get(freqList.get(i));
					nf += op.getNoiseFigurePerChannel().get(freqList.get(i - 1));
					nf += op.getNoiseFigurePerChannel().get(freqList.get(i + 1));
					
					if (i == 1 || i == (freqList.size() - 2)) {
						gainCh /= 3.0f;
						nf /= 3.0f;
					}else{
						gainCh += op.getGainPerChannel().get(freqList.get(i - 2));
						gainCh += op.getGainPerChannel().get(freqList.get(i + 2));
						gainCh /= 5.0f;
						
						nf += op.getNoiseFigurePerChannel().get(freqList.get(i - 2));
						nf += op.getNoiseFigurePerChannel().get(freqList.get(i + 2));
						nf /= 5.0f;
					}
				}

				printer.print(gainCh + "\t" + nf + "\n");
			}
		}

		printer.close();
	}

}
