import java.util.Scanner;

public class clFFMenu
{
	public static void main(String[] args)
	{
		
		Scanner input = new Scanner(System.in);
		
		foodorder karel = new foodorder();
		
		int hburger,cburger,fries,sdrink,ldrink;
		hburger=0;
		cburger=0;
		fries=0;
		sdrink=0;
		ldrink=0;
		String ham = "Y";
		String cheese = "Y";
		String fri = "Y";
		String sdr = "Y";
		String ldr = "Y";
		String C = "Y";
		
	
		while(C.equals("Y")||C.equals("y"))
		{
			karel.takeOrder();
			System.out.println("Would you like any Hamburgers?");
			ham = input.next();
			if(ham.equals("Y")||ham.equals("y"))
			{
			System.out.println("Enter the # of Hamburgers");
			hburger=input.nextInt();
			}
			System.out.println("Would you like any Cheeseburgers?");
			cheese = input.next();
			if(cheese.equals("Y")||cheese.equals("y"))
			{
			System.out.println("Enter the # of Cheeseburgers");
			cburger=input.nextInt();
			}
			System.out.println("Would you like any Fries?");
			fri = input.next();
			if(fri.equals("Y")||fri.equals("y"))
			{
			System.out.println("Enter the # of Fries");
			fries=input.nextInt();
			}
			System.out.println("Would you like any Small Drinks?");
			sdr = input.next();
			if(sdr.equals("Y")||sdr.equals("y"))
			{
			System.out.println("Enter the # of Small Drinks");
			sdrink=input.nextInt();
			}
			System.out.println("Would you like any Large Drinks?");
			ldr = input.next();
			if(ldr.equals("Y")||ldr.equals("y"))
			{
			System.out.println("Enter the # of Large Drinks");
			ldrink=input.nextInt();
			}
			foodorder haynes = new foodorder(hburger,cburger,fries,sdrink,ldrink);
			System.out.println("");
			System.out.println(haynes);
			System.out.println("Would You Like to Take Another Order? (Y/N)");
			C = input.next();
			System.out.println("\n\n");
		}
	}
}
		