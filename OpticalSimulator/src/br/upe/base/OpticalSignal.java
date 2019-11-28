package br.upe.base;

import java.text.NumberFormat;
import java.util.ArrayList;

import br.upe.util.DecibelConverter;

public class OpticalSignal{
    private ArrayList<OpticalChannel> channels;

    /**
     * Largura de banda óptica que será considerada no projeto.
     */
    public static final double B0 = 1.25e10;

    /**
     * 
     * @param channels
     * @param spacing
     *            in GHz
     */
    public OpticalSignal(ArrayList<OpticalChannel> channels) {
	super();
	this.channels = channels;
    }

    public ArrayList<OpticalChannel> getChannels() {
	return channels;
    }

    public void setChannels(ArrayList<OpticalChannel> channels) {
	this.channels = channels;
    }

    public OpticalSignal clone() {
	ArrayList<OpticalChannel> channelsCopy = new ArrayList<OpticalChannel>();
	for (OpticalChannel ch : channels) {
	    channelsCopy.add(ch.clone());
	}
	return new OpticalSignal(channelsCopy);
    }

    public float getTotalPower() {
	double totalInputPower = 0;
	int j = 0;
	for (OpticalChannel ch : channels) {
	    totalInputPower += DecibelConverter.toLinearScale(ch.getSignalPower());
	    double noiseLin = DecibelConverter.toLinearScale(ch.getNoisePower());
	    totalInputPower += noiseLin;
	    
	    // ASE between channels
	    /*if(j>0){
	    OpticalChannel previousCh = channels.get(j - 1);
	    double noiseLinPrevCh = DecibelConverter.toLinearScale(previousCh.getNoisePower());
	    double delta_f = ch.getFrequency() - previousCh.getFrequency();
	    totalInputPower += (noiseLin + noiseLinPrevCh) * delta_f / (2 * B0);
	    }*/

	    j++;
	}
	return (float) DecibelConverter.toDecibelScale(totalInputPower);
    }

    public OpticalSignal adjustByFactor(double factor) {
	ArrayList<OpticalChannel> channelsCopy = new ArrayList<OpticalChannel>();
	for (OpticalChannel ch : channels) {
	    OpticalChannel newCh = new OpticalChannel(ch.getFrequency(), ch.getSignalPower() + factor,
		    ch.getNoisePower() + factor);
	    channelsCopy.add(newCh);
	}
	return new OpticalSignal(channelsCopy);
    }

    @Override
    public String toString() {
	NumberFormat nf = NumberFormat.getInstance();
	nf.setMaximumFractionDigits(2);
	nf.setMinimumFractionDigits(2);

	StringBuffer strBuff = new StringBuffer();

	for (OpticalChannel ch : channels) {
	    strBuff.append(ch.toString() + "\n");
	}

	return strBuff.toString();
    }
}
