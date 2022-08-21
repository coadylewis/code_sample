import java.util.Scanner;

public class clNecklace
{
	public static void main(String[] args)
	{
		Scanner input = new Scanner(System.in);
		String C="Y";
		while(C.equals("Y")||C.equals("y"))
		{
				int first=1;
				int second=1;
			System.out.println("\nEnter The First Number\n");
				first=input.nextInt();
				
			while(Math.abs(first)>10)
			{
				System.out.println("Error, Enter An Integer With A Magnitude Less Than 10");
				first=input.nextInt();
			}	
			System.out.println("\nEnter The Second Number\n");
				second=input.nextInt();
			
			while(Math.abs(second)>10)
			{
				System.out.println("Error, Enter An Integer With A Magnitude Less Than 10");
				second=input.nextInt();
			}
			beads brad = new beads(first,second);
				System.out.println(brad);
			System.out.println("\nWould You Like To Test Again?(Y/N)\n");
				C=input.next();
			while(!(C.equals("Y")||C.equals("y")||C.equals("N")||C.equals("n")))
			{
				System.out.println("Error, Enter Y or N");
				C=input.nextLine();
			}
		}
	}
}