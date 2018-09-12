package br.upe.objfunctions.rn;

import java.util.ArrayList;
import java.util.HashMap;

import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.AmplifierVOA;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalChannel;
import br.upe.base.OpticalSignal;
import br.upe.mascara.OperatingPoint;
import br.upe.mascara.PowerMask;
import br.upe.mascara.PowerMaskFactory;
import br.upe.objfunctions.rn.base.MLP;
import br.upe.objfunctions.rn.base.SigmoidalFunction;
import br.upe.objfunctions.rn.util.NormalizationUtility;
import br.upe.objfunctions.rn.util.NormalizationUtilityFactory;
import br.upe.signal.factory.PowerMaskSignal;
import br.upe.util.DecibelConverter;


public class NNFunction extends ObjectiveFunction {

    private int[] layersSizes = { 3, 9, 2 };
    private NormalizationUtility nu;

    public NNFunction(NormalizationUtility nu) {
	this.nu = nu;
    }

    @Override
    public void defineNewOperationPoint(Amplifier amplifier, OpticalSignal signal) {
	MLP nn = getMLP(amplifier.getType());

	float gainSet = nu.normalizeGainSet(amplifier.getGain());
	float pIn = nu.normalizeInputPower(amplifier.getInputPower());

	double[] outputPower = new double[signal.getChannels().size()];
	double[] noiseFigure = new double[signal.getChannels().size()];
	double totalOutputPower = 0, totalInputPower = 0;
	HashMap<Double, Float> gainPerChannel = new HashMap<Double, Float>();
	HashMap<Double, Float> nfPerChannel = new HashMap<Double, Float>();

	for (int i = 0; i < signal.getChannels().size(); i++) {
	    OpticalChannel channel = signal.getChannels().get(i);
	    float frequency = nu.normalizeFrequency((float) channel.getFrequency());

	    double[] values = { gainSet, pIn, frequency };

	    double[] output = nn.calculateOutput(values, true);

	    // Gain of the channel
	    float gainChannel = nu.unNormalizeGainChannel((float) output[0]);
	    gainPerChannel.put(channel.getFrequency(), gainChannel);

	    double signalLin = DecibelConverter.toLinearScale(channel.getSignalPower());
	    outputPower[i] = signalLin * DecibelConverter.toLinearScale(gainChannel);

	    // Noise Figure of the channel
	    noiseFigure[i] = nu.unNormalizeNoiseFigure((float) output[1]);
	    nfPerChannel.put(channel.getFrequency(), (float) noiseFigure[i]);

	    totalInputPower += signalLin;
	    totalOutputPower += outputPower[i];

	}

	double totalGain = totalOutputPower / totalInputPower;

	// Gain Matching
	totalOutputPower = 0;
	double gainLin = DecibelConverter.toLinearScale(amplifier.getGain());
	for (int i = 0; i < outputPower.length; i++) {
	    outputPower[i] *= (gainLin / totalGain);
	    totalOutputPower += outputPower[i];
	}

	// Setting the features of the amplifier
	amplifier.setFlatness(calculateRipple(outputPower));
	amplifier.setNoiseFigure(calculateNFMax(noiseFigure));
	amplifier.setOutputPower((float) DecibelConverter.toDecibelScale(totalOutputPower));
	amplifier.setGainPerChannel(gainPerChannel);
	amplifier.setNoiseFigurePerChannel(nfPerChannel);
    }

    @Override
    public Amplifier[] getAmplifiersCandidate(Amplifier amplifier, OpticalSignal signal, boolean useInput) {
	PowerMask pm = PowerMaskFactory.getInstance().fabricatePowerMask(amplifier.getType());
	int maxGain = pm.getMaxGain();
	int minGain = pm.getMinGain();
	ArrayList<OperatingPoint> neighbors = new ArrayList<OperatingPoint>();

	if (useInput) {
	    // The Pin is fixed and the Gain is variable
	    for (int i = minGain; i <= maxGain; i++) {
		if ((pm.getMinTotalInputPower(i) - 0.5) <= signal.getTotalPower()
			&& (signal.getTotalPower()) <= (pm.getMaxTotalInputPower(i) + 0.5)) {
		    OperatingPoint op = new OperatingPoint();
		    op.setTotalInputPower(signal.getTotalPower());
		    op.setGainSet(i);

		    neighbors.add(op);
		}
	    }
	} else {
	    if (amplifier.getGain() < minGain)
		amplifier.setGain(minGain);
	    else if (amplifier.getGain() > maxGain)
		amplifier.setGain(maxGain);

	    float pin = pm.getMinTotalInputPower((int) amplifier.getGain());
	    float maxPin = pm.getMaxTotalOutputPower() - amplifier.getGain();

	    // The gain is fixed and the Pin is variable
	    while (pin <= maxPin) {
		OperatingPoint op = new OperatingPoint();
		op.setTotalInputPower(pin);
		op.setGainSet((int) amplifier.getGain());

		neighbors.add(op);

		pin += 1;
	    }
	}

	Amplifier[] amplifiers = new Amplifier[neighbors.size()];
	for (int i = 0; i < amplifiers.length; i++) {
	    amplifiers[i] = new Amplifier(neighbors.get(i), amplifier.getType());
	    if (useInput)
		this.defineNewOperationPoint(amplifiers[i], signal);
	    else {
		double factor = amplifiers[i].getInputPower() - signal.getTotalPower();
		OpticalSignal temp = signal.adjustByFactor(factor);
		this.defineNewOperationPoint(amplifiers[i], temp);
	    }
	}

	return amplifiers;
    }

    private MLP getMLP(AmplifierType type) {

	switch (type) {
	case EDFA_1_STG:
	    return new MLP(layersSizes, new SigmoidalFunction(), NNWeights.EDFA_1_STG, 1);
	case EDFA_2_STG:
	    return new MLP(layersSizes, new SigmoidalFunction(), NNWeights.EDFA_2_STG, 1);
	case EDFA_2_2_STG:
	    return new MLP(layersSizes, new SigmoidalFunction(), NNWeights.EDFA_2_2_STG, 1);
	case B21_L21:
	    break;
	case B21_L24:
	    break;
	case B24:
	    break;
	case L17_10CH:
	    break;
	case L17_20CH:
	    break;
	case L17_40CH:
	    break;
	case L17_80CH:
	    break;
	case L21_40CH:
	    break;
	case P14_L21:
	    break;
	default:
	    break;
	}

	return null;
    }

    public static void main(String[] args) {
	AmplifierType type = AmplifierType.EDFA_2_STG;
	NormalizationUtility nu = NormalizationUtilityFactory.getInstance().fabricate(type);

	float linkInputPower = DecibelConverter.calculateInputPower(39, -25.2f);

	PowerMaskSignal signal = new PowerMaskSignal(39, type, -25.2f, 30);
	OpticalSignal inputSignal = signal.createSignal();

	int ganho = 30;
	Amplifier amplifier = new AmplifierVOA(linkInputPower, ganho, (linkInputPower + ganho), 0.0f, 0.0f, 0.0f, type);

	long t = System.currentTimeMillis();
	NNFunction function = new NNFunction(nu);

	// Amplifier[] amps = function.getAmplifiersCandidate(amplifier,
	// inputSignal);

	function.defineNewOperationPoint(amplifier, inputSignal);
	System.out.println(System.currentTimeMillis() - t);
    }
}
