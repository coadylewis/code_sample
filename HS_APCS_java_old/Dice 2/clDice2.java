import java.util.Scanner;

public class clDice2
{
	public static void main(String[] args)
	{
			Scanner input = new Scanner(System.in);
			String C="Y";
		while(C.equals("Y")||C.equals("y"))
		{
			int rolls;
			System.out.println("\nEnter The Number Of Rolls");
				rolls=input.nextInt();
			while(rolls<=0)
			{
				System.out.println("Error, Enter a Number Greater than 0");
				rolls=input.nextInt();
			}
			rollerm karel = new rollerm(rolls);
			for(int i=0;i<rolls;i++)
			System.out.print(karel.AleaIactaEst());
			System.out.println("\n"+karel+"\nWould You Like To Roll Again?(Y/N)\n");
				C=input.next();
			while(!(C.equals("Y")||C.equals("y")||C.equals("N")||C.equals("n")))
			{
				System.out.println("Error, Enter Y or N");
				C=input.next();
			}
		}
	}
}