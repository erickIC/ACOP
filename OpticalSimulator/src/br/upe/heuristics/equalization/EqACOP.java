package br.upe.heuristics.equalization;

import java.util.ArrayList;
import java.util.List;

import br.upe.base.ACOPHeuristic;
import br.upe.base.Amplifier;
import br.upe.base.AmplifierType;
import br.upe.base.EqualizationHeuristic;
import br.upe.base.IOpticalDevice;
import br.upe.base.ObjectiveFunction;
import br.upe.base.OpticalSignal;
import br.upe.base.ROADM;
import br.upe.heuristics.maxGain.MaxGain;
import br.upe.initializations.UniformInitialization;
import br.upe.metrics.BeckerNoiseFigureMetric;
import br.upe.objfunctions.rn.NNFunction;
import br.upe.objfunctions.rn.util.NormalizationUtility;
import br.upe.objfunctions.rn.util.NormalizationUtilityFactory;
import br.upe.selection.MaxGainSelection;
import br.upe.signal.factory.PowerMaskSignal;
import br.upe.signal.tracker.AmplifierSignalMonitor;
import br.upe.simulations.simsetups.SimSetAMPVOA;
import br.upe.simulations.simsetups.SimulationSetup;

public class EqACOP {
    private ACOPHeuristic acop;
    private EqualizationHeuristic equalization;
    private List<IOpticalDevice> systemDevices;
    private List<AmplifierSignalMonitor> monitors;

    public EqACOP(ACOPHeuristic acop, EqualizationHeuristic equalization, List<IOpticalDevice> systemDevices) {
	super();
	this.acop = acop;
	this.equalization = equalization;
	this.systemDevices = systemDevices;
	this.monitors = new ArrayList<AmplifierSignalMonitor>();
    }
    
    public ACOPHeuristic getAcop() {
	return acop;
    }

    public void setAcop(ACOPHeuristic acop) {
	this.acop = acop;
    }

    public EqualizationHeuristic getEqualization() {
	return equalization;
    }

    public void setEqualization(EqualizationHeuristic equalization) {
	this.equalization = equalization;
    }

    public void execute(OpticalSignal inputSignal) {
	//Create first monitor
	AmplifierSignalMonitor monitor = new AmplifierSignalMonitor();
	monitor.setInputSignal(inputSignal);

	//Create list of monitors and add the first monitor
	monitors.add(monitor);

	// Auxiliary variables to tackle the ACOP result
	boolean isFirstAmplifier = false;
	int indexFirstAmp = 0;
	Amplifier[] amps = null;
	AmplifierSignalMonitor[] monitorsTemp = null;

	for(int i=0; i<systemDevices.size(); i++){
	    IOpticalDevice device = systemDevices.get(i);
	    AmplifierSignalMonitor currentMonitor = monitors.get(i);
	    if(device instanceof ROADM){
		//Equalize the signal and store the result
		currentMonitor
			.setOutputSignal(equalization.equalizeSignal((ROADM) device, currentMonitor.getInputSignal()));
		//Update the input signal for the next monitor
		monitors.add(new AmplifierSignalMonitor());
		monitors.get(i+1).setInputSignal(currentMonitor.getOutputSignal());
		//Signalizes that the next amplifier is the first
		isFirstAmplifier = true;
	    } else if (device instanceof Amplifier) {
		if (isFirstAmplifier) {
		    // Define the correct input power if the first amplifier
		    acop.setLinkInputPower(monitors.get(i).getInputSignal().getTotalPower());
		    acop.getMonitors()[0].setInputSignal(monitors.get(i).getInputSignal());

		    // Execute ACOP and saves amplifiers and monitors
		    amps = acop.execute();
		    monitorsTemp = acop.getMonitors();

		    indexFirstAmp = i;
		}
		// Updates the current amplifier to the one returned
		device = amps[i];
		monitors.get(i).setOutputSignal(monitorsTemp[i - indexFirstAmp].getOutputSignal());
	    }
	}
    }
    
    public static void main(String[] args) {
	// **** ACOP *** //
	AmplifierType type = AmplifierType.EDFA_1_STG;

	NormalizationUtility nu = NormalizationUtilityFactory.getInstance().fabricate(type);
	ObjectiveFunction function = new NNFunction(nu); // LinearInterpolationFunction();

	System.out.println("-- LinearInterpolationFunction --");

	int numberCh = 39;
	SimulationSetup simSet = new SimSetAMPVOA(numberCh, -21f, 9f);
	float[] linLosses = simSet.getLINK_LOSSES();
	int numberAmplifiers = simSet.getNumberOfAmplifiers();

	BeckerNoiseFigureMetric nfMetric = new BeckerNoiseFigureMetric(linLosses);

	// Definindo ganho máximo
	float maxPout = simSet.getMaxOutputPower();
	System.out.println(maxPout);

	//Creating Signal
	PowerMaskSignal signal = new PowerMaskSignal(numberCh, type, simSet.getCHANNEL_POWER(), 30);
	OpticalSignal inputSignal = signal.createSignal();
	
	ACOPHeuristic acop = new MaxGain(numberAmplifiers, linLosses, inputSignal, function);
	acop.setInitialization(new UniformInitialization(type));
	acop.setSelectionOp(new MaxGainSelection());
	acop.setVoaMaxAttenuation(simSet.getVOA_MAX_ATT());
	acop.setRoadmAttenuation(simSet.getROADM_ATT());
	acop.setMaxOutputPower(maxPout);
	
	// **** EQUALIZATION *** //
	EqualizationHeuristic equalization = new StandardEqualization();

	// **** DEVICES *** //
	ROADM roadm = new ROADM(simSet.getROADM_ATT(), simSet.getVOA_MAX_ATT());

	EqACOP heuristic = new EqACOP(acop, equalization, systemDevices);
    }

}
