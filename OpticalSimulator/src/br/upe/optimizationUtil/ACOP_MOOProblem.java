
package br.upe.optimizationUtil;

import java.util.ArrayList;
import java.util.Collections;

import br.upe.base.ACOPHeuristic;
import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.AmplifierVOA;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalChannel;
import br.upe.base.OpticalSignal;
import br.upe.base.SimulationParameters;
import br.upe.heuristics.maxGain.MaxGain;
import br.upe.heuristics.uiara.AdGC;
import br.upe.initializations.BruteForceInitialization;
import br.upe.initializations.UniformInitializationVOA;
import br.upe.objfunctions.linerInterpolation.LinearInterpolationFunction;
import br.upe.selection.MaxGainSelection;
import br.upe.selection.UiaraWeightSelection;
import br.upe.signal.factory.PowerMaskSignal;
import br.upe.simulations.simPadTec19.SimSetPadTec;
import br.upe.simulations.simsetups.SimulationSetup;
import br.upe.util.DecibelConverter;
import br.upe.util.LinearRegression;
import br.upe.util.SignalFeatureCalculation;

public class ACOP_MOOProblem {

	private Amplifier[] amplifiers;
	private AmplifierType type;
	private int numAmps;
	private ACOP_LOCAL_PROBLEM localProblem;
	private SimulationParameters simParams;
	private int preTilt;

	public ACOP_MOOProblem(AmplifierType type, int numberOfAmplifiers, SimulationParameters parameters) {
		this.type = type;
		this.numAmps = numberOfAmplifiers;
		this.localProblem = ACOP_LOCAL_PROBLEM.AdGC;
		this.simParams = parameters;
	}

	public ACOP_MOOProblem(AmplifierType type, int numberOfAmplifiers, SimulationParameters parameters, int preTilt) {
		this.type = type;
		this.numAmps = numberOfAmplifiers;
		this.localProblem = ACOP_LOCAL_PROBLEM.AdGC;
		this.simParams = parameters;
		this.preTilt = preTilt;
	}

	public ACOP_MOOProblem(AmplifierType type, int numberOfAmplifiers, SimulationParameters parameters,
			ACOP_LOCAL_PROBLEM localProblem) {
		this.type = type;
		this.numAmps = numberOfAmplifiers;
		this.localProblem = localProblem;
		this.simParams = parameters;
	}

	public double[] evaluateJustAttenuations(float[] attenuations) {
		return evaluate(null, attenuations);
	}

	/***
	 * 
	 * @param gains
	 * @return linear tilt, -osnr, ripple
	 */
	public double[] evaluateJustGains(float[] gains) {
		return evaluate(gains, null);
	}

	public double[] evaluate(float[] gains, float[] attenuations) {

		// NormalizationUtility nu =
		// NormalizationUtilityFactory.getInstance().fabricate(type);
		ObjectiveFunction function = new LinearInterpolationFunction();

		double linkLength = simParams.getLinkLosses() * 1000 / 0.2;

		PowerMaskSignal signal = new PowerMaskSignal(simParams.getNumberCh(), type,
				simParams.getSimSet().getCHANNEL_POWER(), 40);
		OpticalSignal inputSignal = signal.createSignal();

		float totalInputPowerBeforePreTilt = inputSignal.getTotalPower();
		
		applyPreTilt(inputSignal);

		float totalInputPower = inputSignal.getTotalPower();

		Amplifier[] amplifiers;
		double[] tilts = new double[1];
		OpticalSignal[] outSignals = new OpticalSignal[1];

		float voaAttenuation;
		if(gains == null) {
			ACOPHeuristic heuristic = null;

			switch (localProblem) {
			case MaxGain:
				heuristic = new MaxGain(numAmps, simParams.getSimSet().getLINK_LOSSES(), inputSignal, function);
				heuristic.setSelectionOp(new MaxGainSelection());
				break;
			case AdGC:
				heuristic = new AdGC(numAmps, simParams.getSimSet().getLINK_LOSSES(), inputSignal, function);
				heuristic.setSelectionOp(new UiaraWeightSelection());
				break;
			default:
				heuristic = new AdGC(numAmps, simParams.getSimSet().getLINK_LOSSES(), inputSignal, function);
			}

			heuristic.setInitialization(new UniformInitializationVOA(type, attenuations));
			heuristic.setVoaMaxAttenuation(simParams.getSimSet().getVOA_MAX_ATT());
			heuristic.setRoadmAttenuation(simParams.getSimSet().getROADM_ATT());
			heuristic.setMaxOutputPower(simParams.getSimSet().getMaxOutputPower());
			amplifiers = heuristic.execute();

			if (amplifiers == null)
				return null;

			voaAttenuation = ((AmplifierVOA) amplifiers[amplifiers.length - 1]).getVoaOutAttenuation();
		} else {

			boolean hasVOA = true;
			if (attenuations == null)
				hasVOA = false;

			BruteForceInitialization initialization = new BruteForceInitialization(type, hasVOA,
					simParams.getSimSet().getMaxOutputPower());
			initialization.setGains(gains);
			initialization.setAttenuations(attenuations);

			// System.out.println(inputSignal);

			amplifiers = initialization.initialize(simParams.getSimSet().getNumberOfAmplifiers(), totalInputPower, 0,
					simParams.getSimSet().getLINK_LOSSES(), function, inputSignal);
			tilts = initialization.getTiltsOut();
			outSignals = initialization.getSignalOut();

			if (amplifiers == null)
				return null;

			float ampVoaAtt = ((AmplifierVOA) amplifiers[amplifiers.length - 1]).getVoaOutAttenuation();
			voaAttenuation = (float) (amplifiers[amplifiers.length - 1].getOutputPower() - ampVoaAtt
					- totalInputPower - simParams.getSimSet().getROADM_ATT());
			((AmplifierVOA) amplifiers[amplifiers.length - 1]).increaseVoaOutAttenuation(voaAttenuation);

		}

		// If the output power of the link is less than the
		// input power, then the solution isn't desirable.
		// And, if the output power is greater than the
		// input
		// power + voa max attenuation + roadm attenuation,
		// then
		// the solution is not desirable
		if(!Float.isNaN(simParams.getMinChannelOutputPower()) &&
				SignalFeatureCalculation.calculateMinPower(inputSignal) >= simParams.getMinChannelOutputPower() &&
				SignalFeatureCalculation.calculateMaxPower(inputSignal) <= (simParams.getMaxChannelOutputPower() + simParams.getSimSet().getVOA_MAX_ATT()
						+ simParams.getSimSet().getROADM_ATT())) {
			return prepareReturn(inputSignal);
		}
		else if (amplifiers[amplifiers.length - 1].getOutputPower() >= totalInputPowerBeforePreTilt
				&& ((AmplifierVOA) amplifiers[amplifiers.length - 1])
				.getOutputPowerAfterVOA() <= (totalInputPower + simParams.getSimSet().getVOA_MAX_ATT()
						+ simParams.getSimSet().getROADM_ATT())
				&& voaAttenuation >= 0
				&& Float.isNaN(simParams.getMinChannelOutputPower())
				) {

			
		
			
	   /* System.out.println("-------------------------------------------------------------");
	    System.out.print("SOLUTION: ");
	    for (int i = 0; i < gains.length; i++) {
	    System.out.printf("%.1f\t", gains[i]);
	    }

	    System.out.printf("\nTilt: %.2f, BitRate: %.1f, Ripple: %.2f\n", result[0], 1.0 / result[3], result[2]);

	    System.out.println("***** Potência (dBm) *****");
	    for (int i = 0; i < outSignals.length; i++) {
	    for(OpticalChannel ch : outSignals[i].getChannels()) {
	        System.out.printf("%.2f\t", ch.getSignalPower());
	    }
	    System.out.println();
	    }

	    System.out.println("***** OSNR (dB) *****");
	    for (int i = 0; i < outSignals.length; i++) {
	    double[] osnr = SignalFeatureCalculation.calculateOSNR(outSignals[i]);
	    for (int j = 0; j < osnr.length; j++) {
	        System.out.printf("%.2f\t", osnr[j]);
	    }
	    System.out.println();
	    }
	    System.out.println("-------------------------------------------------------------");
			 */

			return prepareReturn(inputSignal);
		} else {
			return null;
		}
	}
	
	private double[] prepareReturn(OpticalSignal inputSignal) {
		double[] result = new double[3];

		result[OptimizationObjectives.MIN_TILT.ordinal()] = Math.abs(SignalFeatureCalculation.calculateTiltLinearReg(inputSignal));

		result[OptimizationObjectives.MAX_OSNR.ordinal()] = -1 * SignalFeatureCalculation.calculateMinOSNR(inputSignal); // maximizar

		result[OptimizationObjectives.MIN_RIPPLE_OSNR.ordinal()] = SignalFeatureCalculation.calculateRippleOSNR(inputSignal);
		
		/*System.out.printf("%.2f\t%.2f\t|\t%.2f\t%.2f\t%.2f\n", 
				 SignalFeatureCalculation.calculateMaxPower(inputSignal), 
				 SignalFeatureCalculation.calculateMinPower(inputSignal),
				 result[0], -1*result[1], result[2]);*/
		
		return result;
	}

	private void applyPreTilt(OpticalSignal inputSignal) {
		if (preTilt == 0)
			return;

		double factor = Math.abs(preTilt) / (simParams.getNumberCh() - 1.0);

		Collections.sort(inputSignal.getChannels());
		if (preTilt < 0)
			Collections.reverse(inputSignal.getChannels());

		double adjust = 0;
		for (OpticalChannel ch : inputSignal.getChannels()) {
			ch.setSignalPower(ch.getSignalPower() + adjust);
			ch.setNoisePower(ch.getNoisePower() + adjust);
			adjust -= factor;
		}
	}

	private static double calculateTiltLinearReg(OpticalSignal signal) {
		ArrayList<OpticalChannel> channels = signal.getChannels();
		double[] frequencies = new double[channels.size()];
		double[] power = new double[channels.size()];

		int indexMaxFreq = 0, indexMinFreq = 0;

		for (int i = 0; i < power.length; i++) {
			frequencies[i] = channels.get(i).getFrequency();
			power[i] = channels.get(i).getSignalPower();

			if (frequencies[i] < frequencies[indexMinFreq])
				indexMinFreq = i;
			else if (frequencies[i] > frequencies[indexMaxFreq])
				indexMaxFreq = i;
		}

		// normalizing frequencies
		double maxFreq = frequencies[indexMaxFreq];
		double minFreq = frequencies[indexMinFreq];
		for (int i = 0; i < frequencies.length; i++) {
			frequencies[i] = (frequencies[i] - minFreq) / (maxFreq - minFreq);
		}

		LinearRegression lr = new LinearRegression(frequencies, power);

		return lr.Tilt();
	}

	private double calculateTilt(OpticalSignal signal) {
		double maxPeak = Double.MIN_VALUE;
		double minPeak = Double.MAX_VALUE;

		for (OpticalChannel c : signal.getChannels()) {
			double signalLin = DecibelConverter.toLinearScale(c.getSignalPower());

			if (signalLin > maxPeak) {
				maxPeak = signalLin;
			}
			if (signalLin < minPeak) {
				minPeak = signalLin;
			}
		}

		return DecibelConverter.toDecibelScale(maxPeak / minPeak);
	}

	public Amplifier[] getAmplifiers() {
		return amplifiers;
	}

	public void setPreTilt(int i) {
		this.preTilt = i;

	}

	public static void main(String[] args) {

		float chPower = -18.0f; // -20 dBm/ch = -4 dBm ;; -19 dBm/ch = -3 dBm
		int numberCh = 40;
		int numberAmps = 4;
		float loss = 18.0f;

		SimulationSetup simSet = new SimSetPadTec(numberCh, chPower, numberAmps, loss);

		SimulationParameters simParams = new SimulationParameters(numberCh, chPower, loss, simSet);

		ACOP_MOOProblem problem = new ACOP_MOOProblem(AmplifierType.EDFA_1_PadTec, simSet.getNumberOfAmplifiers(),
				simParams);

		float[] gains = { 15, 18, 20, 23 };
		float[] attenuations = { 1, 0, 1, 1 };
		problem.evaluate(gains, attenuations);
	}
}
