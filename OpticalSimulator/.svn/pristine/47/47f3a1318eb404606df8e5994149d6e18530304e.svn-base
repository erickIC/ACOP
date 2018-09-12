package br.upe.metrics;

import br.upe.base.Amplifier;

public class GNLIMetric_old implements Metric {

    // Constants
    private static final double h = 6.6256e-34; // Planck's constant [J/s]
    private static final double nu = 299792458 / 1550e-9; // light frequency
    // [Hz]
    private static final double dB2Neper = 10 / Math.log(10);

    // System parameters
    private static final double D = 16.65; // ps/nm/km
    private static final double gamma = 1.3e-3; // 1/W/m
    private static final double alpha = 0.2e-3; // fibre attenuation (dB/m)
    private static final int N_pol = 2; // number of polarizations

    private double B_signal;
    private double delta_f;
    private double N_channel;
    private double P_Tx_dBm;
    private double Length;

    // Other Results
    private double SNR_NLI;
    private double SNR_ASE;
    private double OSNR_NLI;
    private double OSNR_EDFA;

    public GNLIMetric_old(double signalBandwidth, double channelSpacing, double numberCh, double pinSystem,
	    double spanLength) {
	this.B_signal = signalBandwidth;
	this.delta_f = channelSpacing;
	this.N_channel = numberCh;
	this.P_Tx_dBm = pinSystem;
	this.Length = spanLength;
    }

    @Override
    public double evaluate(Amplifier[] link) {
	double[] powerVec = new double[link.length];
	double[] G_tx_ch = new double[link.length];

	powerVec[0] = P_Tx_dBm + link[0].getGain();
	for (int i = 1; i < powerVec.length; i++) {
	    // Potência dos canais [dB] conforme o nº do span (posição do vetor)
	    powerVec[i] = powerVec[i - 1] - alpha * Length + link[i].getGain();
	}

	// Some more quantities
	// double B_total = N_channel*B_signal; //total system bandwidth
	double beta2 = -(1550e-9*1550e-9) * (D*1e-6) / (2*Math.PI*3e8);	//propagation constant
	double L_eff = ((1-Math.exp(-(alpha/dB2Neper)*Length))/(alpha/dB2Neper)); //effective length [m]
	double L_effa = 1/(alpha/dB2Neper); // asymptotic effective length [m]

	for(int i=0; i<link.length; i++){
	    G_tx_ch[i] = Math.pow(10, (powerVec[i]-30)/10)/B_signal; //[W/Hz]
	}

	//// CÁLCULO DA ASE ////
	// Coeficiente da Ase gerada no 1° amp
	double ASE_Coef = Math.pow(10, link[0].getNoiseFigure() / 10) / 2 * (Math.pow(10, link[0].getGain() / 10) - 1);

	for (int i = 1; i < link.length; i++) {
	    // Coeficiente da Ase gerada no i-ésimo amp somada à ASE propagante
	    // dos spans anteriores.
	    ASE_Coef = Math.pow(10, link[i].getNoiseFigure()/10)/2*(Math.pow(10, link[i].getGain()/10)-1) + ASE_Coef*Math.pow(10, ((link[i].getGain()-alpha*Length)/10));
	}

	double ASE = N_pol*h*nu*ASE_Coef; // Eq. (50) Ase total na sáida do último amp.

	//// IGN model	////
	double[] G_NLI_ss = new double[link.length];
	double[] G_NLI_ss_rx = new double[link.length];

	double[] linkPowerBudget = new double[link.length - 1];
	for (int i = 0; i < linkPowerBudget.length; i++) {
	    linkPowerBudget[i] = Math.pow(10, (link[i + 1].getGain() - alpha * Length) / 10);
	}

	for (int i = 0; i < G_NLI_ss.length; i++) {
	    G_NLI_ss[i] = (8.0 / 27.0) * gamma * gamma * Math.pow(G_tx_ch[i], 3) * L_eff * L_eff;
	    G_NLI_ss[i] *= asinh(0.5 * Math.PI * Math.PI * Math.abs(beta2) * L_effa * B_signal * B_signal*Math.pow(N_channel, 2.0*B_signal/delta_f))
		    / (Math.PI * Math.abs(beta2) * L_effa); // Eq. (36)

	    double[] temp = new double[linkPowerBudget.length - i];
	    for (int j = 0; j < temp.length; j++) {
		temp[j] = linkPowerBudget[linkPowerBudget.length - 1 - j];
	    }

	    G_NLI_ss_rx[i] = G_NLI_ss[i] * prod(temp);
	}

	double G_NLI = G_NLI_ss_rx[0];
	for (int i = 1; i < G_NLI_ss.length - 1; i++) {
	    G_NLI += G_NLI_ss_rx[i];
	}

	//SNR calculation
	SNR_NLI = 10 * Math.log10(G_tx_ch[G_tx_ch.length - 1] / (ASE + G_NLI));
	SNR_ASE = 10 * Math.log10(G_tx_ch[G_tx_ch.length - 1] / ASE);

	double SNR2OSNR = 10 * Math.log10(B_signal / 12.5e9 * N_pol / 2);
	// OSNR calculation
	OSNR_NLI = SNR_NLI + SNR2OSNR;
	OSNR_EDFA = SNR_ASE + SNR2OSNR;

	return G_NLI;
    }

    private double prod(double[] v) {
	if (v.length < 1)
	    return 1;

	double product = v[0];
	for (int i = 1; i < v.length; i++) {
	    product *= v[i];
	}

	return product;
    }

    private double asinh(double x) {
	return Math.log(x + Math.sqrt(x * x + 1.0));
    }

    public double getSNR_NLI() {
	return SNR_NLI;
    }

    public double getSNR_ASE() {
	return SNR_ASE;
    }

    public double getOSNR_NLI() {
	return OSNR_NLI;
    }

    public double getOSNR_EDFA() {
	return OSNR_EDFA;
    }
}
