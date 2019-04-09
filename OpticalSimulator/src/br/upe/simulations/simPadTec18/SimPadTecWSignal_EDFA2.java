package br.upe.simulations.simPadTec18;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.AmplifierVOA;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalSignal;
import br.upe.objfunctions.linerInterpolation.LinearInterpolationFunction;
import br.upe.signal.factory.CustomSignal;
import br.upe.util.SignalFeatureCalculation;

public class SimPadTecWSignal_EDFA2 {
    public static void main(String[] args) {
	float gain = 22f;
	int numberOfAmplifiers = 1;
	int maxAmp = 20;


	double[] frequency = { 192.1e12, 192.2e12, 192.3e12, 192.4e12, 192.5e12, 192.6e12, 192.7e12, 192.8e12, 192.9e12,
		193e12, 193.1e12, 193.2e12, 193.3e12, 193.4e12, 193.5e12, 193.6e12, 193.7e12, 193.8e12, 193.9e12,
		194e12, 194.1e12, 194.2e12, 194.3e12, 194.4e12, 194.5e12, 194.6e12, 194.7e12, 194.8e12, 194.9e12,
		195e12, 195.1e12, 195.2e12, 195.3e12, 195.4e12, 195.5e12, 195.6e12, 195.7e12, 195.8e12, 195.9e12,
		196e12 };
	// EDFA 2 STG, G=22dB, Pout=16dBm
	double[] signalPower = { -22.02112, -22.021029, -22.021029, -22.0211, -22.021024, -22.021039, -22.021024,
		-22.021027, -22.021057, -22.021036, -22.021024, -22.021022, -22.021027, -22.021032, -22.021053,
		-22.021128, -22.021084, -22.021026, -22.021033, -22.021076, -22.021033, -22.021021, -22.021028,
		-22.021027, -22.021059, -22.021048, -22.021042, -22.021022, -22.021075, -22.021062, -22.021023,
		-22.021023, -22.021023, -22.021082, -22.021036, -22.021028, -22.021051, -22.021022, -22.021053,
		-22.021029 };
	
	for (int i = 0; i < signalPower.length; i++) {
	    signalPower[i] -= 0.03;
	}
	
	CustomSignal signal = new CustomSignal(frequency, signalPower, 40);
	OpticalSignal inputSignal = signal.createSignal();
	ObjectiveFunction functionAux = new LinearInterpolationFunction();

	double gfM = Double.MAX_VALUE;
	double osnrM = Double.MAX_VALUE;

	System.out.println("#Amps\tTilt\tOSNR");

	while (numberOfAmplifiers <= maxAmp) {// && osnrM > 10.0) {
	    Amplifier[] amplifiers = new Amplifier[numberOfAmplifiers];

	    OpticalSignal ampInput = inputSignal.clone();

	    for (int i = 0; i < amplifiers.length; i++) {

		double tilt = SignalFeatureCalculation.calculateTiltNonLinearReg(ampInput);

		AmplifierType type = getAmplifierTypeIni(tilt);

		if (i == amplifiers.length - 1) {
		    amplifiers[i] = new AmplifierVOA(ampInput.getTotalPower(), gain, type);
		} else {
		    amplifiers[i] = new Amplifier(ampInput.getTotalPower(), gain, type);
		}

		functionAux.defineNewOperationPoint(amplifiers[i], ampInput);
		ampInput = amplifiers[i].transferFunction(ampInput);
		if (numberOfAmplifiers == maxAmp)
		    System.out.println("#" + (i + 1) + "\t" + ampInput);
		SignalFeatureCalculation.linkTrasferFunction(gain, ampInput);
	    }

	    osnrM = SignalFeatureCalculation.calculateMinOSNR(ampInput);

	    gfM = SignalFeatureCalculation.calculateTiltFixed(ampInput);

	    System.out.printf("%d\t%2.3f\t%2.3f\t", numberOfAmplifiers, gfM, osnrM);
	    System.out.println(amplifiers[numberOfAmplifiers - 1].getType());
	    numberOfAmplifiers++;

	}

    }

    private static AmplifierType getAmplifierTypeIni(double tilt) {
	if (tilt < 0.25)
	    return AmplifierType.EDFA_2_PadTec;

	if (tilt >= 0.25 && tilt < 0.75)
	    return AmplifierType.EDFA_2_Tm0v5_PadTec;

	if (tilt >= 0.75 && tilt < 1.25)
	    return AmplifierType.EDFA_2_Tm1_PadTec;

	if (tilt >= 1.25 && tilt < 1.75)
	    return AmplifierType.EDFA_2_Tm1v5_PadTec;

	if (tilt >= 1.75 && tilt < 2.25)
	    return AmplifierType.EDFA_2_Tm2_PadTec;

	if (tilt >= 2.25 && tilt < 2.75)
	    return AmplifierType.EDFA_2_Tm2v5_PadTec;

	if (tilt >= 2.75 && tilt < 3.25)
	    return AmplifierType.EDFA_2_Tm3_PadTec;

	if (tilt >= 3.25 && tilt < 3.75)
	    return AmplifierType.EDFA_2_Tm3v5_PadTec;

	if (tilt >= 3.75 && tilt < 4.25)
	    return AmplifierType.EDFA_2_Tm4_PadTec;

	if (tilt >= 4.25 && tilt < 4.75)
	    return AmplifierType.EDFA_2_Tm4v5_PadTec;

	if (tilt >= 4.75 && tilt < 5.25)
	    return AmplifierType.EDFA_2_Tm5_PadTec;

	return AmplifierType.EDFA_2_Tm8_PadTec;
    }
}
