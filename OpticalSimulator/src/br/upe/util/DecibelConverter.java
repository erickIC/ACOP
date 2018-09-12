package br.upe.util;

public class DecibelConverter {

	public static double toLinearScale(double dbValue){
		return Math.pow(10, (dbValue/10.0));
	}

	public static double toDecibelScale(double linearValue){
		return 10.0*Math.log10(linearValue);
	}
	
	/**
	 * 
	 * @param channelsNum Number of channels
	 * @param channelPower in dBm
	 * @return the power in dBm
	 */
	public static float calculateInputPower(int channelsNum, float channelPower){
		double linearPower = toLinearScale(channelPower);
		
		return (float)toDecibelScale(channelsNum*linearPower);
	}

}
