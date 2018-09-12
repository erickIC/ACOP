package br.upe.objfunctions.rn.util;

public class NormalizationUtility {
	private float maxGainSet;
	private float minGainSet;
	private float maxInputPower;
	private float minInputPower;
	private float maxFrequency;
	private float minFrequency;
	private float maxGainChannel;
	private float minGainChannel;
	private float maxNoiseFigure;
	private float minNoiseFigure;

	public float getMaxGainSet() {
		return maxGainSet;
	}

	public void setMaxGainSet(float maxGainSet) {
		this.maxGainSet = maxGainSet;
	}

	public float getMinGainSet() {
		return minGainSet;
	}

	public void setMinGainSet(float minGainSet) {
		this.minGainSet = minGainSet;
	}

	public float getMaxInputPower() {
		return maxInputPower;
	}

	public void setMaxInputPower(float maxInputPower) {
		this.maxInputPower = maxInputPower;
	}

	public float getMinInputPower() {
		return minInputPower;
	}

	public void setMinInputPower(float minInputPower) {
		this.minInputPower = minInputPower;
	}

	public float getMaxFrequency() {
		return maxFrequency;
	}

	public void setMaxFrequency(float maxFrequency) {
		this.maxFrequency = maxFrequency;
	}

	public float getMinFrequency() {
		return minFrequency;
	}

	public void setMinFrequency(float minFrequency) {
		this.minFrequency = minFrequency;
	}

	public float getMaxGainChannel() {
		return maxGainChannel;
	}

	public void setMaxGainChannel(float maxGainChannel) {
		this.maxGainChannel = maxGainChannel;
	}

	public float getMinGainChannel() {
		return minGainChannel;
	}

	public void setMinGainChannel(float minGainChannel) {
		this.minGainChannel = minGainChannel;
	}

	public float getMaxNoiseFigure() {
		return maxNoiseFigure;
	}

	public void setMaxNoiseFigure(float maxNoiseFigure) {
		this.maxNoiseFigure = maxNoiseFigure;
	}

	public float getMinNoiseFigure() {
		return minNoiseFigure;
	}

	public void setMinNoiseFigure(float minNoiseFigure) {
		this.minNoiseFigure = minNoiseFigure;
	}

	public float normalizeGainSet(float value) {
		return normalizeEquation(value, maxGainSet, minGainSet);
	}

	public float normalizeInputPower(float value) {
		return normalizeEquation(value, maxInputPower, minInputPower);
	}

	public float normalizeFrequency(float value) {
		return normalizeEquation(value, maxFrequency, minFrequency);
	}

	public float unNormalizeNoiseFigure(float value) {
		return unNormalizeEquation(value, maxNoiseFigure, minNoiseFigure);
	}
	
	public float unNormalizeGainChannel(float value) {
		return unNormalizeEquation(value, maxGainChannel, minGainChannel);
	}

	private static float unNormalizeEquation(float value, float maxValue, float minValue){
		return (float) (((value - 0.1) * (maxValue - minValue)) / 0.8 + minValue);
	}
	
	private static float normalizeEquation(float value, float maxValue, float minValue){
		return (float) (((value - minValue) / (maxValue - minValue)) * 0.8 + 0.1); // y
																					// =
																					// (
																					// (value-minValue)/(maxValue-minValue)
																					// )
	}

	public static void main(String[] args) {
		NormalizationUtility nu = new NormalizationUtility();
		nu.setMaxGainSet(30);
		nu.setMinGainSet(20);
		nu.setMaxInputPower(-0.46785313f);
		nu.setMinInputPower(-29.97248f);
		nu.setMaxFrequency(195995000000000f);
		nu.setMinFrequency(192094000000000f);
		nu.setMaxGainChannel(32.244614f);
		nu.setMinGainChannel(15.966766f);
		nu.setMaxNoiseFigure(5.899117f);
		nu.setMinNoiseFigure(3.5057163f);

	}
}
