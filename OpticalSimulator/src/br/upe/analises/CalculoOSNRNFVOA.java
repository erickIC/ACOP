package br.upe.analises;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.text.NumberFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;
import java.util.Set;

public class CalculoOSNRNFVOA {

	public static void main(String[] args) {
		HashMap<Integer, ArrayList<Float>> hashSomaVOAOSNR = new HashMap<Integer, ArrayList<Float>>();
		File file3 = new File("SomaVOAxminOSNR.txt");
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

					String osnrBruto = readerPar.nextLine().split("\t")[0];
					osnrBruto = osnrBruto.replace(',', '.');

					float osnr = Float.parseFloat(osnrBruto);

					if(hashSomaVOAOSNR.get(soma) ==  null){
						ArrayList<Float> lista = new ArrayList<Float>();
						hashSomaVOAOSNR.put(soma, lista);
					}
									
					hashSomaVOAOSNR.get(soma).add(osnr);
				}

				reader.close();
				readerPar.close();
			}
		}

		NumberFormat nf = NumberFormat.getInstance();
		nf.setMaximumFractionDigits(2);
		Set<Integer> chaves = hashSomaVOAOSNR.keySet();
		for(Integer chave : chaves){
			if(chave > 5)
				break;
			
			printer.print(chave + "\t");			
			for(Float osnr : hashSomaVOAOSNR.get(chave)){
				printer.print(nf.format(osnr) + "\t");
			}

			printer.println();
		}

		printer.close();

	}

}
