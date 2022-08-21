import java.text.DecimalFormat;

public class changer
{
	private int dollars,cents,dollarst,centst;
	public changer(int d,int c,int dt,int ct)
	{
		dollars=d;
		cents=c;
		dollarst=dt;
		centst=ct;
	}
	
	DecimalFormat output = new DecimalFormat("00");
	int quarters,dimes,nickels,pennies,change,bills;
	
	
	public void coins()
	{
		bills=dollarst-dollars;
		if((centst-cents)<0)
		{
			change=centst-cents+100;
			bills=bills-1;
		}
		else
			change=centst-cents;
		int tester=change;
		quarters=tester/25;
		tester=tester%25;
		dimes=tester/10;
		tester=tester%10;
		nickels=tester/5;
		tester=tester%5;
		pennies=tester;
	}
	
	public String toString()
	{
		coins();
		String out="\n";
		out=out+"The Correct Change Is: $"+bills+"."+output.format(change)+
		"\n{\n\t";
		if(bills>0)
			if(bills>1)
				out=out+bills+" Whole Dollars\n\t";
			else
				out=out+bills+" Whole Dollar\n\t";
		if(quarters>0)
			if(quarters>1)
				out=out+quarters+" Quarters\n\t";
			else
				out=out+quarters+" Quarter\n\t";
		if(dimes>0)
			if(dimes>1)
				out=out+dimes+" Dimes\n\t";
			else
				out=out+dimes+" Dime\n\t";
		if(nickels>0)
			if(nickels>1)
				out=out+nickels+" Nickels\n";
			else
				out=out+nickels+" Nickel\n";
		if(pennies>0)
			if(pennies>1)
				out=out+"\t"+pennies+" Pennies\n";
			else
				out=out+"\t"+pennies+" Penny\n";
		out=out+"{\n";
		return out;
	}
}