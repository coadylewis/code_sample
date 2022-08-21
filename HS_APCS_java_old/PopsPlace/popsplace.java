import java.text.DecimalFormat;


public class popsplace
{
	public double HW, HR;
	
	private String E;
	
	public final double OVERTIME=1.5, TAX=0.18;
	
	
	public popsplace(double hoursworked, double hourlyrate, String exempt)
	{
		HW=hoursworked;
		HR=hourlyrate;
		E=exempt;
	}
	
	
	DecimalFormat output = new DecimalFormat("$0.00");
	
	private double wages()
	{
		if(HW<=40.0)
		{
			return HW*HR;
		}
		else
		{
			return (HR*40.0+HR*HW*OVERTIME-HR*40.0*OVERTIME);
		}
	}
	
	private double income()
	{
		if(E.equals("Y")||E.equals("y"))
		{
			return wages();
		}
		else
		{
			return wages() * (1.0-TAX);
		}
	}
	
	public String toString()
	{
		String paycheck= "Wages Earned = " + output.format(income());
		String taxed= "\n" + "Taxes Deducted = " + output.format(wages() * (TAX));
		String exempt= "\n" + "NO TAXES DEDUCTED";
		if(E.equals("Y")||E.equals("y"))
		{
			return paycheck + exempt;
		}
		else
		{
			return paycheck + taxed;
		}
		
	}
}