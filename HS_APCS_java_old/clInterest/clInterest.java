import java.util.Scanner;

public class clInterest
{
	public static void main(String[] args)
	{
			Scanner input = new Scanner(System.in);
			String C="Y";
			while(C.equals("Y")||C.equals("y"))
			{
				System.out.println("\nEnter 'A' to Find Monthly Mortgage Payment;Enter 'B' to Display Amortization Schedule");
				String enter=input.next();
				while(!(enter.equals("A")||enter.equals("a")||enter.equals("B")||enter.equals("b")))
				{
					System.out.println("Enter 'A' or 'B'");
					enter=input.nextLine();
				}
				double principal,interest,x;
				System.out.println("Enter The Principal");
				principal=input.nextDouble();
				System.out.println("Enter The Yearly Interest Rate in Percent");
				interest=input.nextDouble();
				if(enter.equals("A")||enter.equals("a"))
					System.out.println("Enter The Number of Years for the Loan");
				else
					System.out.println("Enter The Monthly Payment");
				x=input.nextDouble();
				interest karel = new interest(principal,interest,x);
				if(enter.equals("A")||enter.equals("a"))
					System.out.println("\nThe Monthly Payment Is: "+karel.monthly()+"\n");
				else
					System.out.println("\n\n"+karel+"\n");
				System.out.println("\n\nWould You Like To Run The Program Again?(Y/N)\n\n");
				C=input.next();
				while(!(C.equals("Y")||C.equals("y")||C.equals("N")||C.equals("n")))
				{
					System.out.println("Error, Enter Y or N");
					C=input.next();
				}
			}
	}
}