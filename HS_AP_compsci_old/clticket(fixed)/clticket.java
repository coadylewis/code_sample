import java.util.Scanner;


public class clticket

{	public static void main(String [] args)
	{
		
	Scanner input = new Scanner(System.in);
	
	String Code;
	double Weight, PricePerPound;
	
	System.out.println("Enter The Weight");
		Weight = input.nextDouble();
	System.out.println("");
	
	
	System.out.println("Enter The PricePerPound");
		PricePerPound = input.nextDouble();
	System.out.println("");
	
	
	System.out.println("Enter The Code");
		Code = input.next();
	System.out.println("");
	System.out.println("");
	System.out.println("");
	
	
	Ticket brian = new Ticket(Weight, PricePerPound, Code);
	
	System.out.println(brian);
	
	
	
	
	}
}