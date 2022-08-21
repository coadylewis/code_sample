import java.text.DecimalFormat;
import java.util.Scanner;

public class foodorder
{	
	private final double H=0.80, C=0.95, F=0.75, SD=0.70, LD=0.90, TAX=0.0925;
	public int hburger,cburger,fries,sdrink,ldrink;

	
	public foodorder(int h,int c,int f,int s,int l)
	{
		hburger=h;
		cburger=c;
		fries=f;
		sdrink=s;
		ldrink=l;
	}
	public foodorder()
	{
		hburger=0;
		cburger=0;
		fries=0;
		sdrink=0;
		ldrink=0;
	}
	
	Scanner input = new Scanner(System.in);
	
	public void takeOrder()
	{
			System.out.println("");
			System.out.println("Select An Option");
			System.out.println("");
			System.out.println("	1. Hamburger       (" + H + " cents)");
			System.out.println("	2. Cheeseburger    (" + C + " cents)");
			System.out.println("	3. French Fries    (" + F + " cents)");
			System.out.println("	4. Small Drink     (" + SD + " cents)");
			System.out.println("	5. Large Drink     (" + LD + " cents)");
			System.out.println("	6. Order Completed");
			System.out.println("");
			System.out.println("");
	}
	
	private double hburger()
	{
		return hburger*H;
	}
	
	private double cburger()
	{
		return cburger*C;
	}
	
	private double fries()
	{
		return fries*F;
	}
	
	private double sdrink()
	{
		return sdrink*SD;
	}
	
	private double ldrink()
	{
		return ldrink*LD;
	}
	
	DecimalFormat output = new DecimalFormat("$0.00");
	
	public String toString()
	{
		String finalbill= "Your Total Is "+output.format((hburger()+cburger()+fries()
		+sdrink()+ldrink())*(1+TAX));
		
		return finalbill;
	}	
}