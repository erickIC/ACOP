package br.upe.analises;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;
import java.util.Set;

public class CalculoNFSomaVOA {

	public static void main(String[] args) {
		HashMap<Integer, ArrayList<Float>> hashSomaVOANF = new HashMap<Integer, ArrayList<Float>>();
		
		File file = new File("1dBm_40chVOA_amp_1.txt");
		File file2 = new File("1dBm_40chVOA_par_1.txt");
		File file3 = new File("SomaVOAxNF.txt");
		
		Scanner reader = null;
		Scanner readerPar = null;
		PrintWriter printer = null;
		try {
			reader = new Scanner(file);
			readerPar = new Scanner(file2);
			printer = new PrintWriter(file3);
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
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
				ArrayList<Float> lista = new ArrayList<Float>();
				hashSomaVOANF.put(soma, lista);
			}
			
			hashSomaVOANF.get(soma).add(nf);
		}
		
		Set<Integer> chaves = hashSomaVOANF.keySet();
		for(Integer chave : chaves){
			printer.print(chave + "\t");
			
			for(Float nf : hashSomaVOANF.get(chave)){
				printer.print(nf + "\t");
			}
			
			printer.println();
		}

		reader.close();
		readerPar.close();
		printer.close();

	}

}
