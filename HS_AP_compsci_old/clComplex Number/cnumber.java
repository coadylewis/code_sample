
public class cnumber
{	
	
	private double real, imag;
	
	public cnumber(double r, double i)
	{
		real = r;
		imag = i;
	}
	public cnumber()
	{
		real = 1;
		imag = 1;
	}
	
	public String imaginary()
	{
		if(imag!=0)
		{
			
			if(imag>0)
			{
				return "+"+imag+"i";
			}
			else
			{
				return imag+"i";
			}
		}
		else
		{
			return "0";
		}
	}
	
	public String complexnumber()
	{
		if(imaginary().equals("0")&&real==0)
		{
			return "0";
		}
		else
		{
			return real+imaginary();
		}
	}
	
	public double getReal()
	{
		return real;
	}
	
	public double getImaginary()
	{
		return imag;
	}
	
	public double getConjugate(cnumber other)
	{
		return other.real*other.real+other.imag*other.imag;
	}
	
	public void setReal(double r)
	{
		real = r;
	}
	
	public void setImaginary(double i)
	{
		imag = i;
	}
	
	public cnumber add(cnumber other)
	{
		double r = real+other.real;
		double i = imag+other.imag;
		return new cnumber (r, i);
	}
	
	public cnumber sub(cnumber other)
	{
		double r = real-other.real;
		double i = imag-other.imag;
		return new cnumber (r, i);
	}
	
	public cnumber div(cnumber other)
	{
		double r = (double)(real*other.real+imag*other.imag)/(getConjugate(other));
		double i = (double)(other.real*imag-real*other.imag)/(getConjugate(other));
		return new cnumber (r, i);
	}
	
	public cnumber mul(cnumber other)
	{
		double r = imag*other.imag*(-1) + real*other.real;
		double i = real*other.imag + imag*other.real;
		return new cnumber (r, i);
	}
	
	public String toString()
	{
		return complexnumber();
	}
}