import java.text.DecimalFormat;

public class cchanger
{
	private int Pennies, Nickels, Dimes, Quarters;
	
	public cchanger(int Pn, int Nck, int Dm, int Qrt)
	{
		Pennies=Pn;
		Nickels=Nck;
		Dimes=Dm;
		Quarters=Qrt;
	}
	public cchanger()
	{
		Pennies=0;
		Nickels=0;
		Dimes=0;
		Quarters=0;
	}
	
	
	public void setPennies(int P)
	{
		Pennies=P;
	}
	
	public void setNickels(int N)
	{
		Nickels=N;
	}
	
	public void setDimes(int D)
	{
		Dimes=D;
	}
	
	public void setQuarters(int Q)
	{
		Quarters=Q;
	}
	
	
	public int findCents()
	{
		return Pennies + 5 * Nickels + 10 * Dimes + 25 * Quarters;
	}
	
	public int findDollars()
	{
		return findCents() / 100;
	}
	
	public int findChange()
	{
		return findCents() % 100;
	}
	
	public int getPennies()
	{
		return Pennies;
	}
	
	public int getNickels()
	{
		return Nickels;
	}
	
	public int getDimes()
	{
		return Dimes;
	}
	
	public int getQuarters()
	{
		return Quarters;
	}
	
	
	DecimalFormat output = new DecimalFormat("00");
	
	
	public String toString()
	{
		return "You have,\n" + getPennies() + " pennies\n" + getNickels() + " nickels\n" + getDimes() +
		" dimes\n" + getQuarters() + " quarters" + "\n" + findCents() + " cents" + "\n" + findDollars() + " whole dollars" + "\n\nTotal Amount = $" +
		findDollars() + "." + output.format(findChange()) + "\n";
	}
}