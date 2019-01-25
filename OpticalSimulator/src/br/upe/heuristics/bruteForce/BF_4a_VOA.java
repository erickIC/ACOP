package br.upe.heuristics.bruteForce;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierVOA;
import br.upe.base.OpticalSignal;
import br.upe.mascara.PowerMask;
import br.upe.mascara.PowerMaskFactory;

public class BF_4a_VOA extends BFMethod {

    private int maxG1, minG1;
    private int maxG2, minG2;

    public BF_4a_VOA(int maxG1, int minG1, int maxG2, int minG2) {
	super(4);
	this.maxG1 = maxG1;
	this.minG1 = minG1;
	this.maxG2 = maxG2;
	this.minG2 = minG2;
    }

    @Override
    public void run() {

	PowerMask pm = PowerMaskFactory.getInstance().fabricatePowerMask(ampType);

	double totalCombAmp = pm.getMaxGain() - pm.getMinGain() + 1;
	double totalCombVoa = simSet.getVOA_MAX_ATT();

	totalCombAmp = Math.pow(totalCombAmp, simSet.getNumberOfAmplifiers());
	totalCombVoa = Math.pow(totalCombVoa, simSet.getNumberOfAmplifiers());

	double totalComb = totalCombAmp * totalCombVoa;

	double contador = 0;

	float shift = 0.0f;

	File arquivoT = new File("4_time.txt");
	// Timestamp timeIni = new Timestamp();

	float G1MaxLimit = maxG1;
	float G1MinLimit = minG1;
	float G2MaxLimit = maxG2;
	float G2MinLimit = minG2;

	if (maxG1 == Integer.MIN_VALUE)
	    G1MaxLimit = pm.getMaxGain();
	if (minG1 == Integer.MAX_VALUE)
	    G1MinLimit = pm.getMinGain();
	if (maxG2 == Integer.MIN_VALUE)
	    G2MaxLimit = pm.getMaxGain();
	if (minG2 == Integer.MAX_VALUE)
	    G2MinLimit = pm.getMinGain();

	while (shift < STEP) {
	    float i = G1MaxLimit - shift;
	    while (i >= G1MinLimit) { // G1

		float j = simSet.getVOA_MAX_ATT() - shift;
		while (j >= 0) { // VOA1

		    float k = G2MaxLimit - shift;
		    while (k >= G2MinLimit) { // G2

			float l = simSet.getVOA_MAX_ATT() - shift;
			while (l >= 0) { // VOA2

			    float m = pm.getMaxGain() - shift;
			    while (m >= pm.getMinGain()) { // G3

				float n = simSet.getVOA_MAX_ATT() - shift;
				while (n >= 0) { // VOA3

				    float o = pm.getMaxGain() - shift;
				    while (o >= pm.getMinGain()) { // G4

					float p = simSet.getVOA_MAX_ATT() - shift;
					while (p >= 0) { // VOA4

					    if (i == 23f && j == 15f)
						System.out.println();

					    float[] gains = { i, k, m, o };
					    float[] attenuations = { j, l, n, p };

					    // float[] gains = { 23, 27, 27,
					    // 27};
					    // float[] attenuations = { 15, 7,
					    // 9, 0 };
					    
					    initialization.setGains(gains);
					    initialization.setAttenuations(attenuations);
					    OpticalSignal signalTemp = inputSignal.clone();
					    Amplifier[] amplifiers = initialization.initialize(
						    simSet.getNumberOfAmplifiers(), INPUT_POWER, 0,
						    simSet.getLINK_LOSSES(), function, signalTemp);

					    // Solucao fora das restricoes
					    if (amplifiers == null
						    || Math.abs(amplifiers[0].getInputPower()) > (Math.abs(INPUT_POWER)
							    + 0.5)
						    || Math.abs(amplifiers[0].getInputPower()) < (Math.abs(INPUT_POWER)
							    - 0.5)
						    || !this.isOutputPowerCorrect(amplifiers)) { // restriction
						// to
						// guarantee
						// the
						// maximum
						// output
						// power
						p -= STEP;
						contador++;
						continue;
					    }

					    SolutionBFMethod solution = null;

					    float ampVoaAtt = ((AmplifierVOA) amplifiers[amplifiers.length - 1])
						    .getVoaOutAttenuation();
					    float voaAttenuation = (float) (amplifiers[amplifiers.length - 1]
						    .getOutputPower() - ampVoaAtt - INPUT_POWER
						    - simSet.getROADM_ATT());
					    ((AmplifierVOA) amplifiers[amplifiers.length - 1])
						    .increaseVoaOutAttenuation(voaAttenuation);

					    // If the output power of the link
					    // is less than the
					    // input power, then the solution
					    // isn't desirable.
					    // And, if the output power is
					    // greater than the
					    // input
					    // power + voa max attenuation +
					    // roadm attenuation,
					    // then
					    // the solution is not desirable
					    if (amplifiers[amplifiers.length - 1].getOutputPower() >= INPUT_POWER
						    && ((AmplifierVOA) amplifiers[amplifiers.length - 1])
							    .getOutputPowerAfterVOA() <= (INPUT_POWER
								    + simSet.getVOA_MAX_ATT() + simSet.getROADM_ATT())
						    && voaAttenuation >= 0) {

						solution = new SolutionBFMethod(NUMBER_OBJ);

						solution.setAmplifiers(amplifiers);

						gnliMetric.evaluate(amplifiers);

						solution.setFitness(0, gnliMetric.getTiltOSNR_NLI()); // tilt_OSNR
						solution.setFitness(1, gnliMetric.worstOSNR_NLI()); // OSNR

						// Choose best solution
						/*
						 * double[] fitness =
						 * solution.getFitness(); double
						 * solutionDi =
						 * Math.sqrt(fitness[2] *
						 * fitness[2] / fitness[1] *
						 * fitness[1]);
						 * 
						 * if (solutionDi > bestDi) {
						 * bestSol = solution; bestDi =
						 * solutionDi; }
						 */
					    }

					    if (solution != null) {
						this.addSolutionEA(solution);
					    }

					    p -= STEP;
					    contador++;
					}

					o -= STEP;
				    }
				    n -= STEP;
				}

				m -= STEP;
			    }
			    l -= STEP;
			}
			try {
			    printExternalArchive(i + "-" + j + "-" + k);
			    // Timestamp timeEnd = new Timestamp();
			    // PrintWriter time = new PrintWriter(arquivoT);
			    // time.println("Start = " + timeIni.getDate());
			    // time.println("End = " + timeEnd.getDate());
			    // time.close();
			} catch (Exception e) {

			}

			k -= STEP;
		    }

		    j -= STEP;
		}
		i -= STEP;

		double perc = (contador / totalComb) * 100;
		System.out.println(perc);
	    }
	    shift += STEP;
	}

	try {
	    printParetoFront();
	} catch (FileNotFoundException e) {
	    // TODO Auto-generated catch block
	    e.printStackTrace();
	}
	// Timestamp timeEnd = new Timestamp();
	// System.out.println("Start = " + timeIni.getDate());
	// System.out.println("End = " + timeEnd.getDate());
    }

    public static void main(String[] args) {
	int runs = 1;
	int g1mx, g1min, g2mx, g2min;
	String selection;

	if (args.length == 0) {
	    g1mx = Integer.MIN_VALUE;
	    g1min = Integer.MAX_VALUE;
	    g2mx = Integer.MIN_VALUE;
	    g2min = Integer.MAX_VALUE;
	    selection = "S";
	}
	else {
	    g1mx = Integer.parseInt(args[0]);
	    g1min = Integer.parseInt(args[1]);
	    g2mx = Integer.MIN_VALUE;
	    g2min = Integer.MAX_VALUE;

	    System.out.println(
		    "G1Max = " + args[0] + " G1Min = " + args[1]);
	    System.out.print("Confirma valores (S/N):");

	    Scanner ler = new Scanner(System.in);
	    selection = ler.nextLine();
	    ler.close();
	}

	if (selection.equals("S") || selection.equals("s")) {
	    BF_4a_VOA bf = new BF_4a_VOA(g1mx, g1min, g2mx, g2min);

	    bf.run();
	}
    }

}