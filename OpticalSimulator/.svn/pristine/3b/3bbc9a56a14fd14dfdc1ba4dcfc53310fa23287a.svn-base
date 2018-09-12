package br.upe.objfunctions.rn.base;

public class SigmoidalFunction implements Function {

	@Override
	public double call(double value) {
		 if (value <= -700)
             return 0;
         else
             return 1.0 / (1 + Math.exp(-1 * value));
	}

	@Override
	public double derivativeCall(double value) {
		
		return this.call(value)*(1 - this.call(value));
	}

}
