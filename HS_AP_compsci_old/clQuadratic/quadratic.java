import java.text.DecimalFormat;

public class quadratic
{
	private double a, b, c;
	
	
	
	public quadratic(double ca, double cb, double cc)
	{
		a=ca;
		b=cb;
		c=cc;
	}
	public quadratic()
	{
		a=0;
		b=0;
		c=0;
	}
	
	DecimalFormat output = new DecimalFormat("0.000");
	
	
	public double dis()
	{
		return (b*b)-(4*a*c);
	}
	
	public boolean onesol()
	{
		if((dis())==0)
		return true;
		else
		return false;
	}
	
	public boolean twosol()
	{
		if((dis())>0)
		return true;
		else
		return false;
	}
	
	public boolean imag()
	{
		if((dis())<0)
		return true;
		else
		return false;
	}
	
	
	public String one()
	{
		String onesolution = output.format((-b)/(2*a));
		return onesolution;
	}
	
	public String two()
	{
		String twosolutions = output.format(((-b)+Math.sqrt(dis()))/(2*a))+" & "+output.format(((-b)-Math.sqrt(dis()))/(2*a));
		return twosolutions;
	}
	
	public String imaginary()
	{
		String imaginary = output.format((-b)/(2*a))+"+"+output.format(Math.sqrt(dis()*(-1))/(2*a))+"i"+" & "+output.format((-b)/(2*a))+"-"+output.format(Math.sqrt(dis()*(-1))/(2*a))+"i";
		return imaginary;
	}
	
	
	
	
}