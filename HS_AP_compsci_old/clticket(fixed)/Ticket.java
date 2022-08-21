import java.text.DecimalFormat;


public class Ticket
{
	private double Weight, PricePerPound;
	
	private String Code;
	
	public Ticket(double W, double PPP, String C)
	{
		Weight=W;
		PricePerPound=PPP;
		Code=C;
	}
	
	
	DecimalFormat output = new DecimalFormat("$0.00");
	
	public double finalcost()
	{
		return Weight * PricePerPound;
	}
	
	
	public String toString()
	{
		String Border ="%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" + "\n" + "\n";
		String Title ="          Brad's Big Red Supermarket Produce Department       " + "\n" + "\n" 
		+ "        Item" + "      Weight" + "     PricePerPound" + "     Final Price" + "\n";
		String Body ="        " + Code + "        " + Weight + " lbs.        " + output.format(PricePerPound) 
		+ "/lb        " + output.format(finalcost()) + "\n" + "\n";
		
		return Border + Title + Body + Border;
	}
	
	
}