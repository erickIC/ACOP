package br.upe.objfunctions.linerInterpolation;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.OpticalSignal;
import br.upe.mascara.OperatingPoint;
import br.upe.mascara.PowerMask;
import br.upe.mascara.PowerMaskFactory;
import br.upe.signal.factory.PowerMaskSignal;
import br.upe.util.DecibelConverter;

public class CalculateInterpolationError {

	public static void main(String[] args) {
		AmplifierType notLearnead = AmplifierType.EDFA_1_STG_IMPAR;
		PowerMask pm = PowerMaskFactory.getInstance().fabricatePowerMask(notLearnead);
		LinearInterpolationFunction function = new LinearInterpolationFunction();

		// Imprimir Erros de Teste
		File file = new File(
				"C:\\Users\\Erick\\Google Drive\\Universidade\\Pesquisas\\02_Amplificadores Cognitivos\\Experimentos\\31_Treinamento RN com Tilt\\Erro_Test_Interp.txt");

		PrintWriter pw = null;
		try {
			pw = new PrintWriter(file);
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}


		for (OperatingPoint op : pm.getOperatingPoints()) {
			float linkInputPower = op.getTotalInputPower();
			float channelInputPower = (float) DecibelConverter
					.toDecibelScale(DecibelConverter.toLinearScale(linkInputPower) / 39.0);
			PowerMaskSignal signal = new PowerMaskSignal(39, AmplifierType.EDFA_1_STG, channelInputPower, 30);
			OpticalSignal inputSignal = signal.createSignal();

			int ganho = op.getGainSet();

			Amplifier amplifier = new Amplifier(linkInputPower, ganho, (linkInputPower + ganho), 0.0f, 0.0f, 0.0f,
					AmplifierType.EDFA_1_STG_PAR);

			function.defineNewOperationPoint(amplifier, inputSignal);
			
			if (amplifier.getGainPerChannel() == null)
				continue;

			Collection<Double> frequencys = op.getGainPerChannel().keySet();
			List<Double> opFreqList = new ArrayList<Double>(frequencys);
			Collections.sort(opFreqList);

			Collection<Double> frequencys2 = amplifier.getGainPerChannel().keySet();
			List<Double> ampFreqList = new ArrayList<Double>(frequencys2);
			Collections.sort(ampFreqList);

			int j = 1;
			for (int i = 0; i < opFreqList.size(); i++) {
				pw.print(op.getGainSet() + "\t" + op.getTotalInputPower() + "\t" + opFreqList.get(i) + "\t");

				float expectedGain = op.getGainPerChannel().get(opFreqList.get(i));
				float actualGain = amplifier.getGainPerChannel().get(ampFreqList.get(j));
				pw.print(Math.abs(expectedGain - actualGain) + "\t");

				float expectedNF = op.getNoiseFigurePerChannel().get(opFreqList.get(i));
				float actualNF = amplifier.getNoiseFigurePerChannel().get(ampFreqList.get(j));
				pw.println(Math.abs(expectedNF - actualNF));

				j += 2;
			}
		}

		pw.close();
	}

}
