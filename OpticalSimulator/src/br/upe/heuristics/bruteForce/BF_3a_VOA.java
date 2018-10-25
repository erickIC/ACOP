package br.upe.heuristics.bruteForce;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;

import com.sun.jmx.snmp.Timestamp;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierVOA;
import br.upe.base.OpticalSignal;
import br.upe.mascara.PowerMask;
import br.upe.mascara.PowerMaskFactory;

public class BF_3a_VOA extends BFMethod {

    public BF_3a_VOA() {
	super(3);
    }

    @Override
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

	File arquivoT = new File("time.txt");
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

			    float m = pm.getMaxGain() - shift;
			    while (m >= pm.getMinGain()) { // G3

				float n = simSet.getVOA_MAX_ATT() - shift;
				while (n >= 0) { // VOA3

				    float[] gains = { i, k, m };
				    float[] attenuations = { j, l, n };

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
					n -= STEP;
					contador++;
					continue;
				    }

				    SolutionBFMethod solution = null;

				    float ampVoaAtt = ((AmplifierVOA) amplifiers[amplifiers.length - 1])
					    .getVoaOutAttenuation();
				    float voaAttenuation = (float) (amplifiers[amplifiers.length - 1].getOutputPower()
					    - ampVoaAtt - INPUT_POWER - simSet.getROADM_ATT());
				    ((AmplifierVOA) amplifiers[amplifiers.length - 1])
					    .increaseVoaOutAttenuation(voaAttenuation);

				    // If the output power of the link is less
				    // than the
				    // input power, then the solution isn't
				    // desirable.
				    // And, if the output power is greater than
				    // the
				    // input
				    // power + voa max attenuation + roadm
				    // attenuation,
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

				    n -= STEP;
				    contador++;
				}

				m -= STEP;
			    }
			    l -= STEP;
			}
			k -= STEP;
		    }

		    j -= STEP;

		    double perc = (contador / totalComb) * 100;
		    System.out.println(perc);

		    /*
		     * long te = System.currentTimeMillis(); System.out.println(
		     * "End = " + (te -ti) + " msec.\n\n");
		     */

		}

		try {
		    printExternalArchive(i + "");
		    Timestamp timeEnd = new Timestamp();
		    PrintWriter time = new PrintWriter(arquivoT);
		    time.println("Start = " + timeIni.getDate());
		    time.println("End = " + timeEnd.getDate());
		    time.close();
		} catch (Exception e) {

		}

		i -= STEP;
	    }
	    shift += STEP;
	}

	try {
	    printParetoFront();
	} catch (FileNotFoundException e) {
	    // TODO Auto-generated catch block
	    e.printStackTrace();
	}
	Timestamp timeEnd = new Timestamp();
	System.out.println("Start = " + timeIni.getDate());
	System.out.println("End = " + timeEnd.getDate());

    }

    public static void main(String[] args) {
	int runs = 1;
	for (int i = 0; i < runs; i++) {
	    BF_3a_VOA bf = new BF_3a_VOA();

	    bf.run();
	}
    }
}