package br.upe.objfunctions.rn.base;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;

public class Logger {
	private File arquivo;
	private double[][] dadosTreinamento;
	private double[][] dadosValidacao;

	public Logger(String caminho, int execucoes, int tamanhoDados) {
		arquivo = new File(caminho);

		dadosTreinamento = new double[execucoes][tamanhoDados];
		dadosValidacao = new double[execucoes][tamanhoDados];
	}

	public void definirValoresTreinamento(int execucao, double[] valores) {
		dadosTreinamento[execucao] = valores;
	}

	public void definirValoresValidacao(int execucao, double[] valores) {
		dadosValidacao[execucao] = valores;
	}

	public void imprimirResultado(int step) throws FileNotFoundException {
		PrintWriter printerTrein = new PrintWriter(arquivo + "_treinamento.txt");
		PrintWriter printerVal = new PrintWriter(arquivo + "_validacao.txt");

		for (int i = 0; i < dadosTreinamento[0].length; i++) {
			printerTrein.print((i * step) + "\t");
			printerVal.print((i * step) + "\t");
			for (int j = 0; j < dadosTreinamento.length; j++) {
				printerTrein.print(dadosTreinamento[j][i]);
				printerVal.print(dadosValidacao[j][i]);
				if (j == dadosTreinamento.length - 1) {
					printerTrein.print("\n");
					printerVal.print("\n");
				} else {
					printerTrein.print("\t");
					printerVal.print("\t");
				}
			}
		}

		printerTrein.close();
		printerVal.close();
	}

	/*
	 * public void imprimirResultadoEmLinha() throws FileNotFoundException{
	 * printer = new PrintWriter(arquivo+".txt");
	 * 
	 * for (int i = 0; i < dadosTreinamento[0].length; i++) { for (int j = 0; j
	 * < dadosTreinamento.length; j++) {
	 * printer.print(dadosTreinamento[j][i]+","); } }
	 * 
	 * printer.close(); }
	 */

}