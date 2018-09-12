package br.upe.simulations.simPadTec;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Set;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalSignal;
import br.upe.mascara.OperatingPoint;
import br.upe.mascara.PowerMask;
import br.upe.mascara.PowerMaskFactory;
import br.upe.objfunctions.linerInterpolation.LinearInterpolationFunction;
import br.upe.signal.factory.CustomSignal;
import br.upe.util.SignalFeatureCalculation;

public class SimPadTec_EDFA1_Alone {
    public static void main(String[] args) {

	ObjectiveFunction functionAux = new LinearInterpolationFunction();

	double[] frequency = { 192.1e12, 192.2e12, 192.3e12, 192.4e12, 192.5e12, 192.6e12, 192.7e12, 192.8e12, 192.9e12,
		193e12, 193.1e12, 193.2e12, 193.3e12, 193.4e12, 193.5e12, 193.6e12, 193.7e12, 193.8e12, 193.9e12,
		194e12, 194.1e12, 194.2e12, 194.3e12, 194.4e12, 194.5e12, 194.6e12, 194.7e12, 194.8e12, 194.9e12,
		195e12, 195.1e12, 195.2e12, 195.3e12, 195.4e12, 195.5e12, 195.6e12, 195.7e12, 195.8e12, 195.9e12,
		196e12 };
	int gain = 14;
	float inputPower = 2.0f;


	//Para cada tilt com máscara disponível
	for (int tilt = 8; tilt < 25; tilt++) {
	    // Criar sinal de entrada com tilt
	    double[][] signalPower = getSignalPower(tilt, inputPower, gain);
	    if (signalPower == null)
		continue;
	    CustomSignal signal = new CustomSignal(frequency, signalPower[0], 40);
	    OpticalSignal inputSignal = signal.createSignal();

	    // Passar sinal pelo amplificador
	    Amplifier amplifier = new Amplifier(inputSignal.getTotalPower(), gain, AmplifierType.EDFA_1_PadTec);
	    functionAux.defineNewOperationPoint(amplifier, inputSignal);
	    OpticalSignal outputSignal = amplifier.transferFunction(inputSignal);
	    
	    // Calcular tilt no sinal de saída
	    double tiltEstimado = SignalFeatureCalculation.calculateTiltLinearReg(outputSignal);
	    
	    CustomSignal signalMask = new CustomSignal(frequency, signalPower[1], 40);
	    double tiltMascara = SignalFeatureCalculation.calculateTiltLinearReg(signalMask.createSignal());
	    
	    // Imprimir tilt de entrada e erro
	    System.out.println(tilt + "\t" + (tiltEstimado - tiltMascara));
	}
    }

    /**
     * Deve retornar o sinal de entrada e o sinal de saída para um determinado
     * ponto de operação
     * 
     * @param tilt
     * @param edfa1Padtec
     * @return
     */
    private static double[][] getSignalPower(int tilt, float inputPower, int gain) {
	// Dado o tilt pegar a máscara correta
	AmplifierType type = getAmplifierType(tilt);
	if (type == null)
	    return null;
	PowerMask pm = PowerMaskFactory.getInstance().fabricatePowerMask(type);

	// Dado a máscara pegar o ponto de operação com o mesmo gain e pin
	OperatingPoint op = getOperatingPoint(pm, inputPower, gain);
	if (op == null)
	    return null;

	// Dado o ponto de operação pegar o espectro de entrada e calcular o de
	// saída
	Set<Double> frequencys = op.getInputPowerPerChannel().keySet();
	ArrayList<Double> freqs = new ArrayList<>(frequencys);
	Collections.sort(freqs);

	double[][] signals = new double[2][frequencys.size()];
	for (int i = 0; i < freqs.size(); i++) {
	    signals[0][i] = op.getInputPowerPerChannel().get(freqs.get(i));
	    Float gainTemp = op.getGainPerChannel().get(freqs.get(i));
	    signals[1][i] = signals[0][i] + gainTemp;
	}

	return signals;
    }

    private static AmplifierType getAmplifierType(double tilt) {
	if (tilt >= 0)
	    return getAmplifierType1dBPositive(tilt);
	else
	    return getAmplifierType1dBNegative(-1 * tilt);
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
	case 16:
	    return AmplifierType.EDFA_1_T16_PadTec;
	case 21:
	    return AmplifierType.EDFA_1_T21_PadTec;
	case 25:
	    return AmplifierType.EDFA_1_T25_PadTec;
	default:
	    return null;
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
	case 17:
	    return AmplifierType.EDFA_1_Tm16_PadTec;
	case 18:
	    return AmplifierType.EDFA_1_Tm18_PadTec;
	case 19:
	    return AmplifierType.EDFA_1_Tm19_PadTec;
	case 22:
	    return AmplifierType.EDFA_1_Tm22_PadTec;
	case 25:
	    return AmplifierType.EDFA_1_Tm25_PadTec;
	case 26:
	    return AmplifierType.EDFA_1_Tm26_PadTec;
	default:
	    return null;
	}
    }

    private static OperatingPoint getOperatingPoint(PowerMask pm, float inputPower, int gain) {
	OperatingPoint op = null;
	ArrayList<OperatingPoint> ops = pm.getOperatingPoints();
	ArrayList<OperatingPoint> opsSameGain = new ArrayList<OperatingPoint>();

	if (gain < pm.getMinGain() || gain > pm.getMaxGain())
	    return null;

	for (OperatingPoint op2 : ops) {
	    if (op2.getGainSet() == gain)
		opsSameGain.add(op2);
	}

	Collections.sort(opsSameGain);

	for (int i = 0; i < opsSameGain.size(); i++) {
	    if (i == 0)
		op = opsSameGain.get(0);
	    else if (inputPower < (opsSameGain.get(i).getTotalInputPower() - 0.5f)) {
		op = opsSameGain.get(i - 1);
		break;
	    }
	}

	return op;
    }
}
