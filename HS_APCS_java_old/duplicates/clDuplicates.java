import java.util.Scanner;

public class clDuplicates
{
	public static void main(String[] args)
	{
			Scanner input = new Scanner(System.in);
			String C="Y";
		while(C.equals("Y")||C.equals("y"))
		{
			int iterations;
			System.out.println("\nEnter The Number Of Iterations");
				iterations=input.nextInt();
			while(iterations<=0)
			{
				System.out.println("Error, Enter a Number Greater than 0");
				iterations=input.nextInt();
			}
			dup karel = new dup(iterations);
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