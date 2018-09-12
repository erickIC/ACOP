package br.upe.objfunctions.rn.base;

import java.util.ArrayList;
import java.util.Random;

public class MLP{

	public Layer[] layers;
	private ArrayList<Double> errorTraining = new ArrayList<Double>();
	private double[] errorValidation;


	/**
	 * Used in the case which the user had already trained the network
	 * @param layerSizeValues
	 * @param definedWeights The weights found
	 */
	public MLP(int[] layerSizeValues, Function function, double[] definedWeights, int biasValue)
	{
		this.layers = new Layer[layerSizeValues.length];
		int weightsIndex = 0;
		for (int i = 0; i < this.layers.length; i++)
		{
			double maxNeuronIndex;
			Neuron[] newNeurons;

			if(i<layerSizeValues.length-1){
				newNeurons = new Neuron[layerSizeValues[i]+1];
				maxNeuronIndex = newNeurons.length-1; 
				//Last layer, without bias
			}else{
				newNeurons = new Neuron[layerSizeValues[i]];
				maxNeuronIndex = newNeurons.length;
			}

			for (int j = 0; j < maxNeuronIndex; j++)
			{
				double[] weights;
				//first layer
				if(i==0){
					weights = new double[1];
					weights[0] = 1;
				}else{
					weights = new double[layerSizeValues[i-1]+1];

					for(int k=0;k<weights.length;k++)
					{
						weights[k] = definedWeights[weightsIndex++];
					}
				}

				if (i == 0)
				{
					newNeurons[j] = new Neuron(new IdentityFunction(), weights, false);
				}
				else
				{
					newNeurons[j] = new Neuron(function, weights, false);
				}
			}

			//Inserting the bias neuron
			if (i < layerSizeValues.length - 1)
			{
				double[] weights = new double[0];
				newNeurons[newNeurons.length - 1] = new Neuron(new IdentityFunction(), weights, true);
				newNeurons[newNeurons.length - 1].storedValue = biasValue;
			}

			this.layers[i] = new Layer(newNeurons);
		}
	}

	//receives a list with the layers size values. Ex.: [3,5,4,2] => input = 3, 2 hidden layers (5 e 4), and output = 2
	public MLP(int[] layerSizeValues,Function function,int biasValue)
	{
		Random randNum = new Random(System.currentTimeMillis());
		this.layers = new Layer[layerSizeValues.length];
		for (int i = 0; i < this.layers.length; i++)
		{
			double maxNeuronIndex;
			Neuron[] newNeurons;

			if(i<layerSizeValues.length-1){
				newNeurons = new Neuron[layerSizeValues[i]+1];
				maxNeuronIndex = newNeurons.length-1; 
			}else{
				newNeurons = new Neuron[layerSizeValues[i]];
				maxNeuronIndex = newNeurons.length;
			}
			for (int j = 0; j < maxNeuronIndex; j++)
			{
				double[] weights;
				if(i==0){
					weights = new double[1];
					weights[0] = 1;
				}else{
					weights = new double[layerSizeValues[i-1]+1];
					int neg = randNum.nextInt(1);
					if(neg==0)
					{
						for(int k=0;k<weights.length;k++)
						{
							weights[k] = -1*randNum.nextDouble();
						}
					}else{
						for(int k=0;k<weights.length;k++)
						{
							weights[k] = randNum.nextDouble();
						}
					}                        
				}

				if (i == 0)
				{
					newNeurons[j] = new Neuron(new IdentityFunction(), weights, false);
				}
				else
				{
					newNeurons[j] = new Neuron(function, weights, false);
				}
			}
			//Inserting the bias neuron
			if (i < layerSizeValues.length - 1)
			{
				double[] weights = new double[0];
				newNeurons[newNeurons.length - 1] = new Neuron(new IdentityFunction(), weights, true);
				newNeurons[newNeurons.length - 1].storedValue = biasValue;
			}
			this.layers[i] = new Layer(newNeurons);
		}
	}

	public double[] calculateOutput(double[] input,boolean validation){

		if (input.length != this.layers[0].neurons.length - 1){
			throw new RuntimeException("O tamanho da entrada fornecida não bate com o tamanho requerido.");
		}
		else
		{
			for (int i = 0; i < this.layers[0].neurons.length; i++)
			{
				if (!this.layers[0].neurons[i].isBias)
				{
					this.layers[0].neurons[i].storedValue = input[i];
				}
			}
			for (int i = 0; i < this.layers.length - 1; i++)
			{
				for (int j = 0; j < this.layers[i].neurons.length; j++)
				{
					double functionOutput;
					if (!this.layers[i].neurons[j].isBias)
					{
						functionOutput = this.layers[i].neurons[j].functionCall();
					}
					else
					{
						functionOutput = 1;
					}

					for (Neuron neuron2 : this.layers[i + 1].neurons)
					{
						if (!neuron2.isBias)
						{
							neuron2.storedValue += neuron2.inputWeights[j] * functionOutput;
						}
					}
				}
			}
			double[] ret = new double[this.layers[this.layers.length - 1].neurons.length];
			int b = 0;
			for (Neuron neuron : this.layers[this.layers.length - 1].neurons)
			{
				ret[b] = neuron.functionCall();
				b++;            
			}

			if(validation){
				resetNeuronsStoredValues();
			}

			return ret;
		}
	}

	private double[] forwardStage(double[] input, double[] desiredOutput)
	{
		double[] actualOutput = this.calculateOutput(input, false);
		double[] ret = new double[desiredOutput.length];
		for (int i = 0; i < desiredOutput.length; i++)
		{
			// Absolute Error (AE)
			ret[i] = (desiredOutput[i] - actualOutput[i]);
		}
		return ret;
	}

	private double backpropagation(double[] input,double[] desiredOutput,double learningRate,double momentumAlpha){
		double[] errors = this.forwardStage(input, desiredOutput);
		ArrayList<Double>[] sensibilities = new ArrayList[this.layers.length];
		for (int i = 0; i < sensibilities.length; i++)
		{
			sensibilities[i] = new ArrayList<Double>();
		}
		//Calculando sensibilidade dos neurônios de saída
		int j = this.layers.length - 1;
		while (j >= 0)
		{
			if (j == this.layers.length - 1)
			{
				for (int i = 0; i < this.layers[j].neurons.length; i++)
				{
					double derivativeOutput = this.layers[j].neurons[i].derivativeFunctionCall();
					sensibilities[j].add(derivativeOutput * errors[i]);
				}
			}
			else
			{
				for (int i = 0; i < this.layers[j].neurons.length; i++)
				{
					double derivativeOutput = this.layers[j].neurons[i].derivativeFunctionCall();
					if (!this.layers[j].neurons[i].isBias)
					{
						double sum = 0;
						for (int k = 0; k < this.layers[j + 1].neurons.length; k++)
						{
							if (!this.layers[j + 1].neurons[k].isBias)
							{
								sum += this.layers[j + 1].neurons[k].inputWeights[i] * (double)sensibilities[j + 1].get(k);
							}
						}
						sensibilities[j].add(sum * derivativeOutput);
					}
				}
			}
			j -= 1;
		}
		for (int _i = 0; _i < this.layers.length - 1; _i++)
		{
			int i=this.layers.length-1-_i;
			for (j = 0; j < this.layers[i].neurons.length; j++)
			{
				if (!this.layers[i].neurons[j].isBias)
				{
					for (int k = 0; k < this.layers[i].neurons[j].inputWeights.length; k++)
					{
						double oldValue = this.layers[i].neurons[j].inputWeights[k];
						this.layers[i].neurons[j].inputWeights[k] += learningRate * (double)sensibilities[i].get(j) * this.layers[i - 1].neurons[k].functionCall() + momentumAlpha * (double)this.layers[i].neurons[j].oldWeightChanges.get(k);
						this.layers[i].neurons[j].oldWeightChanges.set(k, this.layers[i].neurons[j].inputWeights[k] - oldValue);
					}
				}
			}
		}
		this.resetNeuronsStoredValues();
		return errorCalc(errors);
	}

	private double errorCalc(double[] errors)
	{
		double _sum = 0;
		for (double error : errors)
		{
			_sum += error * error;
		}
		return _sum / errors.length;
	}

	private void resetNeuronsStoredValues()
	{
		for (Layer layer : this.layers)
		{
			for (Neuron neuron : layer.neurons)
			{
				if (!neuron.isBias)
				{
					neuron.storedValue = 0;
				}
			}
		}
	}

	public double validateNetwork(double[][] validationData, double[][] validationOutput, double OmaX, double Omin)
	{
		double sumsum = 0;
		for (int j = 0; j < validationData.length; j++)
		{
			double[] nnOutput = this.calculateOutput(validationData[j], true);
			this.resetNeuronsStoredValues();
			double _sum = 0;
			for (int i = 0; i < validationOutput[j].length; i++)
			{
				_sum += (validationOutput[j][i] - nnOutput[i]) * (validationOutput[j][i] - nnOutput[i]);
			}

			sumsum += _sum/validationOutput[j].length;
		}

		return sumsum/validationData.length;
	}

	public double[] getErrorValidation(){
		return errorValidation;
	}

	public void onlineTraining(double[][] samples, double[][] desiredOutputs, boolean shuffleData, double learningRate, double maximumAcceptableError, int maxIterations, double momentumAlpha, double Omax, double Omin)
	{
		double averageError = maximumAcceptableError + 1;
		int count = 0;
		errorTraining = new ArrayList<Double>();

		while (averageError > maximumAcceptableError && count < maxIterations)
		{

			double errorSum = 0;
			for (int i = 0; i < samples.length; i++)
			{
				errorSum += this.backpropagation(samples[i], desiredOutputs[i], learningRate, momentumAlpha);
			}
			averageError = errorSum / samples.length;
			errorTraining.add(averageError);

			count++;
		}

	}
	
	private void shuffleData(double[][] data, double[][] data2) {
		Random random = new Random();

		for (int i = 0; i < (data.length - 1); i++) {
			// sorteia um índice
			int j = random.nextInt(data.length);

			// troca o conteúdo dos índices i e j do vetor 1
			double[] temp = data[i];
			data[i] = data[j];
			data[j] = temp;

			// troca o conteúdo dos índices i e j do vetor 2
			temp = data2[i];
			data2[i] = data2[j];
			data2[j] = temp;
		}
	}

	public void onlineTraining(double[][] samples, double[][] desiredOutputs, 
			boolean shuffleData, double learningRate, double maximumAcceptableError, 
			int maxIterations, double momentumAlpha, double Omax, double Omin, 
			double[][] validationInput, double[][] validationOutputs)
	{
		double averageError = maximumAcceptableError + 1;
		int count = 0;
		errorTraining = new ArrayList<Double>();
		errorValidation = new double[maxIterations];

		while (averageError > maximumAcceptableError && count < maxIterations)
		{

			if (shuffleData)
				shuffleData(samples, desiredOutputs);

			double errorSum = 0;
			for (int i = 0; i < samples.length; i++)
			{
				errorSum += this.backpropagation(samples[i], desiredOutputs[i], learningRate, momentumAlpha);
			}
			averageError = errorSum / samples.length;
			errorTraining.add(averageError);

			if(validationInput != null){
				if (shuffleData)
					shuffleData(validationInput, validationOutputs);

				errorValidation[count] = this.validateNetwork(validationInput, validationOutputs, Omax, Omin);
			}

			count++;
		}

	}

	public double[][] getErrorData(int step) {
		double[][] retorno = new double[2][51];

		for (int i = 0; i < errorTraining.size(); i += step) {
			retorno[0][i / step] = errorTraining.get(i);
			retorno[1][i / step] = errorValidation[i];
		}

		retorno[0][retorno[0].length - 1] = errorTraining.get(errorTraining.size() - 1);
		retorno[1][retorno[1].length - 1] = errorValidation[errorValidation.length - 1];

		return retorno;
	}

	public ArrayList<Double> getWeights(){
		ArrayList<Double> weights = new ArrayList<Double>();
		//Para cada camada, comecando da escondida
		for (int i = 1; i < layers.length; i++) {
			//Para cada neuronio no qual o valor vai entrar
			for(int j=0; j<layers[i].neurons.length; j++){
				if(!layers[i].neurons[j].isBias){
					//Para cada neuronio que o valor veio
					for(int k=0; k<layers[i-1].neurons.length; k++){
						weights.add(this.layers[i].neurons[j].inputWeights[k]); //recebe do bias
					}
				}
			}
		}

		return weights;
	}

}
