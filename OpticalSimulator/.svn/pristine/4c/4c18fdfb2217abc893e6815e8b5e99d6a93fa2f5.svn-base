package br.upe.objfunctions.rn;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Scanner;

import br.upe.base.AmplifierType;
import br.upe.objfunctions.rn.base.Logger;
import br.upe.objfunctions.rn.base.MLP;
import br.upe.objfunctions.rn.base.SigmoidalFunction;
import br.upe.objfunctions.rn.util.NormalizationUtility;
import br.upe.objfunctions.rn.util.NormalizationUtilityFactory;

public class TrainingMaskSimple {

    private static AmplifierType type = AmplifierType.EDFA_2_2_STG;
    private static String AMP_PATH = "05_Com Tilt/EDFA_2_2_STG/";

    private static String TREINAMENTO = "./masks/" + AMP_PATH + "DadosTreinamento.txt";
    private static String VALIDACAO = "./masks/" + AMP_PATH + "DadosValidacao.txt";
    private static String TESTE = "./masks/" + AMP_PATH + "DadosTeste.txt";

    /**
     * @param args
     */
    public static void main(String[] args) {
	int[] layersSizes = { 3, 9, 2 };
	int runs = 30;
	String str = "9N_edfa22";
	Logger logger = new Logger(
		"C:\\Users\\Erick\\Google Drive\\Universidade\\Pesquisas\\02_Amplificadores Cognitivos\\Experimentos\\31_Treinamento RN com Tilt\\Erro_"
			+ str,
		runs, 51);

	// Valores normalizados
	double[][] inputs = readInput(TREINAMENTO, type);
	double[][] outputs = readOutput(TREINAMENTO, type);

	// Valores normalizados
	double[][] inputsVal = readInput(VALIDACAO, type);
	double[][] outputsVal = readOutput(VALIDACAO, type);

	// Valores NÃO normalizados
	double[][] inputsTest = readInput(TESTE, type);
	double[][] outputsTest = readOutput(TESTE, type);

	ArrayList<Double> testErrorsG = new ArrayList<Double>();
	ArrayList<Double> testErrorsNF = new ArrayList<Double>();

	NormalizationUtility nu = NormalizationUtilityFactory.getInstance().fabricate(type);

	MLP nn = null;

	int maxInterations = 7000;
	int step = maxInterations / 50;

	for (int i = 0; i < runs; i++) {
	    nn = new MLP(layersSizes, new SigmoidalFunction(), 1);
	    nn.onlineTraining(inputs, outputs, false, 0.3, 0.0001, maxInterations, 0.3, 0, 1, inputsVal, outputsVal);

	    logger.definirValoresTreinamento(i, nn.getErrorData(step)[0]);
	    logger.definirValoresValidacao(i, nn.getErrorData(step)[1]);

	    DecimalFormat format = new DecimalFormat();
	    format.setMaximumFractionDigits(3);
	    format.setMinimumFractionDigits(2);

	    ////// TESTING ///////////////////

	    double errorTest = 0;
	    double avErrorNF = 0;
	    double avErrorRp = 0;

	    testErrorsG.clear();
	    testErrorsNF.clear();

	    for (int j = 0; j < inputsTest.length; j++) {
		float gainSet = nu.normalizeGainSet((float) inputsTest[j][0]);
		float pIn = nu.normalizeInputPower((float) inputsTest[j][1]);
		float frequency = nu.normalizeFrequency((float) inputsTest[j][2]);

		double[] values = { gainSet, pIn, frequency };

		double[] output = nn.calculateOutput(values, true);

		double errorGChannel = nu.unNormalizeGainChannel((float) output[0]);
		errorGChannel = Math.abs(errorGChannel - (float) outputsTest[j][0]);

		double errorNF = nu.unNormalizeNoiseFigure((float) output[1]);

		errorNF = Math.abs(errorNF - (float) outputsTest[j][1]);

		avErrorNF += errorGChannel;
		avErrorRp += errorNF;

		errorTest += (errorGChannel + errorNF) / 2.0;

		testErrorsG.add(errorGChannel);
		testErrorsNF.add(errorNF);
	    }

	    // Imprimir erros separados
	    System.out.println(
		    i + "\tErro de Teste - eGainCh, eNF, eTotal:\t" + format.format(avErrorNF / outputsTest.length)
			    + " " + format.format(avErrorRp / outputsTest.length) + " "
			    + format.format(errorTest / outputsTest.length));

	    // Imprimir os pesos


	    ArrayList<Double> weigths = nn.getWeights();

	    for (Double d : weigths) {
		System.out.print(d + ", ");
	    }
	}

	try {
	    logger.imprimirResultado(step);

	    // Imprimir Erros de Teste
	    File file = new File(
		    "C:\\Users\\Erick\\Google Drive\\Universidade\\Pesquisas\\02_Amplificadores Cognitivos\\Experimentos\\31_Treinamento RN com Tilt\\Erro_Test_"
			    + str + ".txt");
	    PrintWriter pw = new PrintWriter(file);

	    for (int i = 0; i < testErrorsG.size(); i++) {
		pw.print(inputsTest[i][0] + "\t" + inputsTest[i][1] + "\t" + inputsTest[i][2] + "\t");
		pw.println(testErrorsG.get(i) + "\t" + testErrorsNF.get(i));
	    }

	    pw.close();
	} catch (FileNotFoundException e) {
	    // TODO Auto-generated catch block
	    e.printStackTrace();
	}
    }

    private static double[][] readInput(String path, AmplifierType type) {
	double[][] retorno = null;
	try {
	    ArrayList<double[]> listaTemp = new ArrayList<double[]>();
	    File file = new File(path);
	    Scanner reader = new Scanner(file);

	    while (reader.hasNextLine()) {
		String[] line = reader.nextLine().split("\t");
		double[] values = new double[3]; // G_set, Pin, Frequency, G_ch,
		// NF_ch

		values[0] = Float.parseFloat(line[0]);
		values[1] = Float.parseFloat(line[1]);
		values[2] = Float.parseFloat(line[2]);

		listaTemp.add(values);
	    }

	    reader.close();

	    retorno = new double[listaTemp.size()][2];

	    for (int i = 0; i < retorno.length; i++) {
		retorno[i] = listaTemp.get(i);
	    }

	} catch (FileNotFoundException e) {
	    e.printStackTrace();
	}

	return retorno;
    }

    private static double[][] readOutput(String path, AmplifierType type) {
	double[][] retorno = null;
	try {
	    ArrayList<double[]> listaTemp = new ArrayList<double[]>();
	    File file = new File(path);
	    Scanner reader = new Scanner(file);

	    while (reader.hasNextLine()) {
		String[] line = reader.nextLine().split("\t");
		double[] values = new double[2]; // G_set, Pin, Frequency, G_ch,
		// NF_ch

		values[0] = Float.parseFloat(line[3]);
		values[1] = Float.parseFloat(line[4]);

		listaTemp.add(values);
	    }

	    reader.close();

	    retorno = new double[listaTemp.size()][2];

	    for (int i = 0; i < retorno.length; i++) {
		retorno[i] = listaTemp.get(i);
	    }

	} catch (FileNotFoundException e) {
	    e.printStackTrace();
	}

	return retorno;
    }

}
