package br.upe.heuristics.bruteForce;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.Scanner;

public class ManyFilesToOneFile {

    public static void main(String[] args) {

	PrintWriter paretoPrint = null;
	PrintWriter ampsPrint = null;
	try {
	    paretoPrint = new PrintWriter("edfa1_3amps_par.txt");
	    ampsPrint = new PrintWriter("edfa1_3amps_amp.txt");
	} catch (FileNotFoundException e1) {
	    // TODO Auto-generated catch block
	    e1.printStackTrace();
	}

	File arquivos[];
	File diretorio = new File("edfa1_3amps");
	arquivos = diretorio.listFiles();
	for (int i = 0; i < arquivos.length; i++) {
	    String[] name = arquivos[i].getName().split("_");
	    Scanner reader = null;
	    try {
		reader = new Scanner(arquivos[i]);
	    } catch (FileNotFoundException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	    }

	    while (reader.hasNextLine()) {
		if (name[3].equals("par.txt")) {
		    paretoPrint.println(reader.nextLine());
		} else {
		    ampsPrint.println(reader.nextLine());
		}
	    }

	    reader.close();
	}

	paretoPrint.close();
	ampsPrint.close();
    }

}
