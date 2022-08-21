import java.util.Scanner;


public class clpp

{	public static void main(String [] args)
	{
		
	Scanner input = new Scanner(System.in);
	
	double HW, HR;
	String E;
	
	System.out.println("Enter The Hours Worked");
		HW = input.nextDouble();
	System.out.println("");
	
	
	System.out.println("Enter The Hourly Rate");
		HR = input.nextDouble();
	System.out.println("");
	
	
	System.out.println("Exempt (Y/N)?");
		E = input.next();
	System.out.println("");
	System.out.println("");
	System.out.println("");
	
	
	popsplace brian = new popsplace(HW, HR, E);
	
	System.out.println(brian);
	}
}