package br.upe.heuristics.bruteForce;

import com.sun.jmx.snmp.Timestamp;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierVOA;
import br.upe.base.OpticalSignal;
import br.upe.mascara.PowerMask;
import br.upe.mascara.PowerMaskFactory;

public class BFMethod_2amps extends BFMethod {

    public BFMethod_2amps(int numberOfAmplifiers) {
	super(numberOfAmplifiers);
    }

    public void run() {

	// long ti = System.currentTimeMillis();
	// System.out.println("Start");
	PowerMask pm = PowerMaskFactory.getInstance().fabricatePowerMask(ampType);

	double totalCombAmp = pm.getMaxGain() - pm.getMinGain() + 1;
	double totalCombVoa = simSet.getVOA_MAX_ATT();

	totalCombAmp = Math.pow(totalCombAmp, simSet.getNumberOfAmplifiers());
	totalCombVoa = Math.pow(totalCombVoa, simSet.getNumberOfAmplifiers());

	double totalComb = totalCombAmp * totalCombVoa;

	double contador = 0;

	float shift = 0.0f;

	Timestamp timeIni = new Timestamp();

	while (shift < STEP) {
	    float i = pm.getMaxGain() - shift;
	    while (i >= pm.getMinGain()) { // G1

		float j = simSet.getVOA_MAX_ATT() - shift;
		while (j >= 0) { // VOA1

		    float k = pm.getMaxGain() - shift;
		    while (k >= pm.getMinGain()) { // G2

			float l = simSet.getVOA_MAX_ATT() - shift;
			while (l >= 0) { // VOA2
			    float[] gains = { i, k };
			    float[] attenuations = { j, l };

			    initialization.setGains(gains);
			    initialization.setAttenuations(attenuations);
			    OpticalSignal signalTemp = inputSignal.clone();
			    Amplifier[] amplifiers = initialization.initialize(simSet.getNumberOfAmplifiers(),
				    INPUT_POWER, 0, simSet.getLINK_LOSSES(), function, signalTemp);

			    // Solucao fora das restricoes
			    if (amplifiers == null
				    || Math.abs(amplifiers[0].getInputPower()) > (Math.abs(INPUT_POWER) + 0.5)
				    || Math.abs(amplifiers[0].getInputPower()) < (Math.abs(INPUT_POWER) - 0.5)
				    || !this.isOutputPowerCorrect(amplifiers)) { // restriction
				// to
				// guarantee
				// the
				// maximum
				// output
				// power
				l -= STEP;
				contador++;
				continue;
			    }

			    SolutionBFMethod solution = null;

			    float ampVoaAtt = ((AmplifierVOA) amplifiers[amplifiers.length - 1]).getVoaOutAttenuation();
			    float voaAttenuation = (float) (amplifiers[amplifiers.length - 1].getOutputPower()
				    - ampVoaAtt - INPUT_POWER - simSet.getROADM_ATT());
			    ((AmplifierVOA) amplifiers[amplifiers.length - 1])
				    .increaseVoaOutAttenuation(voaAttenuation);

			    // If the output power of the link is less than the
			    // input power, then the solution isn't desirable.
			    // And, if the output power is greater than the
			    // input
			    // power + voa max attenuation + roadm attenuation,
			    // then
			    // the solution is not desirable
			    if (amplifiers[amplifiers.length - 1].getOutputPower() >= INPUT_POWER
				    && ((AmplifierVOA) amplifiers[amplifiers.length - 1])
					    .getOutputPowerAfterVOA() <= (INPUT_POWER + simSet.getVOA_MAX_ATT()
						    + simSet.getROADM_ATT())
				    && voaAttenuation >= 0) {

				solution = new SolutionBFMethod(NUMBER_OBJ);

				solution.setAmplifiers(amplifiers);

				gnliMetric.evaluate(amplifiers);

				solution.setFitness(0, gnliMetric.getTiltOSNR_NLI()); // tilt_OSNR
				solution.setFitness(1, gnliMetric.worstOSNR_NLI()); // OSNR

				// Choose best solution
				/*
				 * double[] fitness = solution.getFitness();
				 * double solutionDi = Math.sqrt(fitness[2] *
				 * fitness[2] / fitness[1] * fitness[1]);
				 * 
				 * if (solutionDi > bestDi) { bestSol =
				 * solution; bestDi = solutionDi; }
				 */
			    }

			    if (solution != null) {
				this.addSolutionEA(solution);
			    }

			    l -= STEP;
			    contador++;
			}

			k -= STEP;
		    }

		    j -= STEP;

		    double perc = (contador / totalComb) * 100;
		    // System.out.printf("%3.2f \n", perc);

		    /*
		     * long te = System.currentTimeMillis(); System.out.println(
		     * "End = " + (te -ti) + " msec.\n\n");
		     */

		}
		i -= STEP;
	    }
	    shift += STEP;
	}

	try {
	    printExternalArchive(0);
	    printParetoFront();
	} catch (Exception e) {

	}

	Timestamp timeEnd = new Timestamp();

	System.out.println("Start = " + timeIni.getDate());
	System.out.println("End = " + timeEnd.getDate());

	// System.out.println("Best NF = " + bestDi);
	// System.out.println(bestSol);
	// System.out.println(bestSol.printAmps());
    }

    public static void main(String[] args) {
	int runs = 1;
	for (int i = 0; i < runs; i++) {
	    BFMethod_2amps bf = new BFMethod_2amps(2);

	    bf.run();
	}
    }
}
