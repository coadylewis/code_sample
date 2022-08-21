import java.util.Scanner;

public class clBirthday
{
	public static void main(String[] args)
	{
			Scanner input = new Scanner(System.in);
			String C="Y";
		while(C.equals("Y")||C.equals("y"))
		{
			int iterations;
			int people;
			System.out.println("\nEnter The Number Of Tests");
				iterations=input.nextInt();
			while(iterations<=0)
			{
				System.out.println("Error, Enter an Integer Greater than 0");
				iterations=input.nextInt();
			}
			System.out.println("\nEnter The Number of People in the Room");
				people=input.nextInt();
			while(people<=0)
			{
				System.out.println("Error, Enter an Integer Greater than 0");
				people=input.nextInt();
			}
			birthday karel = new birthday(iterations, people);
			for(int i=0;i<iterations;i++)
			{
				karel.acc();
			}
			System.out.println("\n"+karel+"\n\nWould You Like To Test Again?(Y/N)\n");
				C=input.next();
			while(!(C.equals("Y")||C.equals("y")||C.equals("N")||C.equals("n")))
			{
				System.out.println("Error, Enter Y or N");
				C=input.next();
			}
		}
	}
}