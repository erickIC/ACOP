package br.upe.analises;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;
import java.util.Set;

public class CalculoMenorNFVOA {

	public static void main(String[] args) {
		HashMap<Integer, Float> hashSomaVOANF = new HashMap<Integer, Float>();
		File file3 = new File("SomaVOAxmaxOSNR.txt");
		PrintWriter printer = null;

		try {
			printer = new PrintWriter(file3);
		} catch (FileNotFoundException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}

		for(int i=0; i<=4; i++){
			for(int j=12; j<=22; j++){
				String path = "C:\\Users\\Erick\\Desktop\\FB VOA\\";
				File file = new File(path + "40chVOABed_amp_" + i + "_" + j + ".txt");
				File file2 = new File(path + "40chVOABed_par_" + i + "_" + j +  ".txt");

				Scanner reader = null;
				Scanner readerPar = null;

				try {
					reader = new Scanner(file);
					readerPar = new Scanner(file2);
				} catch (FileNotFoundException e) {
					continue;
				}

				while(reader.hasNextLine()){
					String[] linha = reader.nextLine().split("],");

					int soma = 0;
					for(String s : linha){
						s = s.substring(3,4);

						soma += Integer.parseInt(s);
					}

					String nfBruto = readerPar.nextLine().split("\t")[0];
					nfBruto = nfBruto.replace(',', '.');

					float nf = Float.parseFloat(nfBruto);

					if(hashSomaVOANF.get(soma) ==  null){
						hashSomaVOANF.put(soma, nf);
					}
					else if(nf > hashSomaVOANF.get(soma)){
						hashSomaVOANF.put(soma, nf);
					}
				}

				reader.close();
				readerPar.close();
			}
		}

		Set<Integer> chaves = hashSomaVOANF.keySet();
		for(Integer chave : chaves){
			System.out.print(chave + "\t");

			System.out.print(hashSomaVOANF.get(chave) + "\t");

			System.out.println();
		}

		printer.close();

	}

}
