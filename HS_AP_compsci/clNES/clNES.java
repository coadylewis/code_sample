import java.util.Scanner;

public class clNES
{
	public static void main(String[] args)
	{
			Scanner input = new Scanner(System.in);
			String C="Y";
			while(C.equals("Y")||C.equals("y"))
			{
				System.out.println("\nEnter 'A' For Residential; Enter 'B' For Commercial");
				String enter=input.next();
				while(!(enter.equals("A")||enter.equals("a")||enter.equals("B")||enter.equals("b")))
				{
					System.out.println("Enter 'A' or 'B'");
					enter=input.nextLine();
				}
				System.out.println("Enter The Kilowatt Hours of Usage");
				double kwh=input.nextDouble();
				while(kwh<=0)
				{
					System.out.println("Enter A Value Greater Than Zero");
					kwh=input.nextDouble();
				}
				
				NES brad = new NES(kwh);
				if(enter.equals("A")||enter.equals("a"))
					System.out.println(brad.Residential());
				else
				{
					System.out.println("Enter The Kilowatts Demanded");
					double kw=input.nextDouble();
					while(kw<=0)
					{
						System.out.println("Enter A Value Greater Than Zero");
						kw=input.nextDouble();
					}
					System.out.println(brad.Commercial(kw));
				}
				System.out.println("\nWould You Like To Run The Program Again?(Y/N)\n");
				C=input.next();
				while(!(C.equals("Y")||C.equals("y")||C.equals("N")||C.equals("n")))
				{
					System.out.println("Error, Enter Y or N");
					C=input.next();
				}
			}
	}
}