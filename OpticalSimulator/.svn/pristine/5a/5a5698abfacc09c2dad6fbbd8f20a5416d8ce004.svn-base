package br.upe.objfunctions.rn.util;

import br.upe.base.AmplifierType;

public class NormalizationUtilityFactory {
    private static NormalizationUtilityFactory instance;

    public static NormalizationUtilityFactory getInstance() {
	if (instance == null)
	    instance = new NormalizationUtilityFactory();

	return instance;
    }

    public NormalizationUtility fabricate(AmplifierType type) {
	switch (type) {
	case EDFA_1_STG:
	    return fabricateEdfa1Stg();
	case EDFA_2_STG:
	    return fabricateEdfa2Stg();
	case EDFA_2_2_STG:
	    return fabricateEdfa22Stg();
	default:
	    return null;
	}
    }

    private NormalizationUtility fabricateEdfa22Stg() {
	NormalizationUtility nu = new NormalizationUtility();
	nu.setMaxGainSet(27);
	nu.setMinGainSet(17);
	nu.setMaxInputPower(4.000484f);
	nu.setMinInputPower(-27.999516f);
	nu.setMaxFrequency(195987000000000f);
	nu.setMinFrequency(192086000000000f);
	nu.setMaxGainChannel(26.933067f);
	nu.setMinGainChannel(14.965725f);
	nu.setMaxNoiseFigure(10.0239f);
	nu.setMinNoiseFigure(5.2135115f);


	return nu;
    }

    private NormalizationUtility fabricateEdfa2Stg() {
	NormalizationUtility nu = new NormalizationUtility();

	nu.setMaxGainSet(30);
	nu.setMinGainSet(20);
	nu.setMaxInputPower(0.59440035f);
	nu.setMinInputPower(-29.938555f);
	nu.setMaxFrequency(195991000000000f);
	nu.setMinFrequency(192086000000000f);
	nu.setMaxGainChannel(30.849255f);
	nu.setMinGainChannel(16.62081f);
	nu.setMaxNoiseFigure(12.819446f);
	nu.setMinNoiseFigure(3.0038574f);

	return nu;
    }

    private NormalizationUtility fabricateEdfa1Stg() {
	NormalizationUtility nu = new NormalizationUtility();
	// Máscara total
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

	// Máscara com filtro5
	/*
	 * nu.setMaxGainSet(30); nu.setMinGainSet(20);
	 * nu.setMaxInputPower(-0.46785313f); nu.setMinInputPower(-29.97248f);
	 * nu.setMaxFrequency(1.959950E+14f); nu.setMinFrequency(1.920940E+14f);
	 * nu.setMaxGainChannel(32.088066f); nu.setMinGainChannel(15.966766f);
	 * nu.setMaxNoiseFigure(5.709846f); nu.setMinNoiseFigure(3.6376302f);
	 */

	// Máscara com Pin por canal

	/*
	 * nu.setMaxGainSet(30); nu.setMinGainSet(20);
	 * nu.setMaxInputPower(-16.241293f); nu.setMinInputPower(-47.250664f);
	 * nu.setMaxFrequency(195995000000000f);
	 * nu.setMinFrequency(192094000000000f);
	 * nu.setMaxGainChannel(32.244614f); nu.setMinGainChannel(15.966766f);
	 * nu.setMaxNoiseFigure(5.899117f); nu.setMinNoiseFigure(3.5057163f);
	 */

	return nu;
    }
}
