import java.util.Scanner;

public class clqbr
{
	public static void main(String[] args)
	{
			Scanner input = new Scanner(System.in);
			String C="Y",name;
			double att,com,yg,tdp,nint;
		while(C.equals("Y")||C.equals("y"))
		{
			System.out.println("\nEnter the Name of the Quarterback\n");
				name=input.nextLine();
			System.out.println("\nEnter the Number of Pass Attempts\n");
				att=input.nextDouble();
			while(att<0)
			{
				System.out.println("Error, Enter a Number Greater than or Equal to 0");
				att=input.nextDouble();
			}
			System.out.println("\nEnter the Number of Pass Completions\n");
				com=input.nextDouble();
			while(com<0)
			{
				System.out.println("Error, Enter a Number Greater than or Equal to 0");
				com=input.nextDouble();
			}
			System.out.println("\nEnter the Number of Yards Gained\n");
				yg=input.nextDouble();
			while(yg<0)
			{
				System.out.println("Error, Enter a Number Greater than or Equal to 0");
				yg=input.nextDouble();
			}
			System.out.println("\nEnter the Number of Touchdown Passes\n");
				tdp=input.nextDouble();
			while(tdp<0)
			{
				System.out.println("Error, Enter a Number Greater than or Equal to 0");
				tdp=input.nextDouble();
			}
			System.out.println("\nEnter the Number of Interceptions\n");
				nint=input.nextDouble();
			while(nint<0)
			{
				System.out.println("Error, Enter a Number Greater than or Equal to 0");
				nint=input.nextDouble();
			}
			quarter tombradyforthewin=new quarter(name,att,com,yg,tdp,nint);
			System.out.println("\n"+tombradyforthewin+"\nWould You Like To Test Again?(Y/N)\n");
				C=input.next();
			while(!(C.equals("Y")||C.equals("y")||C.equals("N")||C.equals("n")))
			{
				System.out.println("Error, Enter Y or N");
				C=input.nextLine();
			}
		}
	}
}