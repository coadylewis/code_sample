import java.util.Scanner;
import java.text.DecimalFormat;

public class clChange
{
	public static void main(String[] args)
	{
			DecimalFormat output = new DecimalFormat("00");
			Scanner input = new Scanner(System.in);
		int dollars= (int)(Math.random()*100+1);
		int cents= (int)(Math.random()*100);
		double test=dollars+(((double)(cents))/100);
		String purchase=" "+dollars+"."+output.format(cents);
		System.out.println("The Purchase Price Is:"+purchase+
		"\n\nEnter The Cash Tendered");
			double cash=input.nextDouble();
		while(cash<test)
			{
				System.out.println("Error, Payment Must Be Greater Than Purchase Price");
				cash=input.nextDouble();
			}
		int dollarst=(int)(cash);
		int centst=(int)Math.round((cash-(int)cash)*100);
		
		changer roger=new changer(dollars,cents,dollarst,centst);
		System.out.println(roger);
	}
}