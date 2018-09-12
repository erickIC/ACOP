package br.upe.analises;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;
import java.util.Set;

public class CalculoMaiorOSNRVOA {

	public static void main(String[] args) {
		HashMap<Integer, Float> hashSomaVOAOSNR = new HashMap<Integer, Float>();
		File file3 = new File("SomaVOAxminOSNR.txt");
		PrintWriter printer = null;

		try {
			printer = new PrintWriter(file3);
		} catch (FileNotFoundException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}

		File file = new File("m2.5dBm_VOA_L21_6Aamp.txt");
		File file2 = new File("m2.5dBm_VOA_L21_6Apar.txt");

		Scanner reader = null;
		Scanner readerPar = null;

		try {
			reader = new Scanner(file);
			readerPar = new Scanner(file2);
		} catch (FileNotFoundException e) {
			//continue;
		}

		while(reader.hasNextLine()){
			String[] linha = reader.nextLine().split("],");

			int soma = 0;
			for(int i=0; i<linha.length-1; i++){
				String s = linha[i];
				String[] valores = s.split("\t");
				valores = valores[2].split(" ");
				s = valores[1].substring(1,2);

				soma += Integer.parseInt(s);
			}

			String nfBruto = readerPar.nextLine().split("\t")[0];
			nfBruto = nfBruto.replace(',', '.');

			float osnr = Float.parseFloat(nfBruto);

			if(hashSomaVOAOSNR.get(soma) ==  null){
				hashSomaVOAOSNR.put(soma, osnr);
			}
			else if(osnr > hashSomaVOAOSNR.get(soma)){
				hashSomaVOAOSNR.put(soma, osnr);
			}
		}

		reader.close();
		readerPar.close();

		Set<Integer> chaves = hashSomaVOAOSNR.keySet();
		for(Integer chave : chaves){
			System.out.print(chave + "\t");

			System.out.printf("%2.2f", hashSomaVOAOSNR.get(chave));

			System.out.println();
		}

		printer.close();

	}

}
