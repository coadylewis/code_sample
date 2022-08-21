import java.util.Scanner;

public class clClock
{
	public static void main(String[] args)
	{
			Scanner input = new Scanner(System.in);
			String C="Y";
			int hour,cmin;
			int min=0;
			String test;
			boolean am=true;
		while(C.equals("Y")||C.equals("y"))
		{
			min=0;
			System.out.println("\nEnter the Current Hour\n");
				hour=input.nextInt();
			while(hour<=0)
			{
				System.out.println("\nError, Enter a Number Greater than 0\n");
				hour=input.nextInt();
			}
			System.out.println("\nEnter the Current Minute\n");
				cmin=input.nextInt();
			while(cmin<0)
			{
				System.out.println("\nError, Enter a Number Greater than or Equal to 0\n");
				cmin=input.nextInt();
			}
			System.out.println("\nEnter A for AM or P for PM\n");
				test=input.next();
			while((!(test.equals("A")||test.equals("a")))&&
			(!(test.equals("P")||test.equals("p"))))
			{
				System.out.println("\nError, Enter A for AM or P for PM\n");
				test=input.next();
			}
			if(test.equals("A")||test.equals("a"))
			{
				am=true;
			}
			if(test.equals("P")||test.equals("p"))
			{
				am=false;
			}
			
			clock bladezofglory = new clock(hour,cmin,min,am);
			
			System.out.println("\n"+bladezofglory+"\n");
			System.out.println("\nEnter the Minutes You Would Like to Advance the Clock\n");
				min=input.nextInt();
			while(min<0)
			{
				System.out.println("\nError, Enter a Number Greater than or Equal to 0\n");
				min=input.nextInt();
			}
			
			clock thefinalcountdown = new clock(hour,cmin,min,am);;
			
			System.out.println("\n"+thefinalcountdown+
			"\n\nWould You Like To Run The Program Again?(Y/N)\n");
			
				C=input.next();
			while(!(C.equals("Y")||C.equals("y")||C.equals("N")||C.equals("n")))
			{
				System.out.println("\nError, Enter Y or N\n");
				C=input.next();
			}
		}
	}
}