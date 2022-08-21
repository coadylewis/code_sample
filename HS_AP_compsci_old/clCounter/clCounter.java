import java.util.Scanner;

public class clCounter
{
	public static void main(String[] args)
	{
			Scanner input = new Scanner(System.in);
			String C="Y";
			int nmbr;
		while(C.equals("Y")||C.equals("y"))
		{
			System.out.println("How Many Numbers Do You Want To Generate\n");
				nmbr=input.nextInt();
			while(nmbr<=0)
			{
				System.out.println("Error, Enter a Number Greater than 0");
				nmbr=input.nextInt();
			}
			counter bladezofglory = new counter(nmbr);
			System.out.println("\n"+bladezofglory+"\nWould You Like To Test Again?(Y/N)\n");
				C=input.next();
			while(!(C.equals("Y")||C.equals("y")||C.equals("N")||C.equals("n")))
			{
				System.out.println("Error, Enter Y or N");
				C=input.next();
			}
		}
	}
}