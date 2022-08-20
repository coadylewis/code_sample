import java.util.Scanner;

 
public class cleaster

{	public static void main(String [] args)
	{
		Scanner reader = new Scanner(System.in);
		
		int A, B, C, D, E, F, Year;
		
		System.out.println("Enter The Year");
		
		Year = reader.nextInt();
		A = Year % 19;
		B = Year % 4;
		C = Year % 7;
		D = (19 * A + 24) % 30;
		E = (2 * B + 4 * C + 6 * D + 5) % 7;
		F = (22 + D + E);
		
		
		if((Year == 1954) || (Year == 1981) || (Year == 2049) || (Year == 2076))
		{
			F=F-7;
		}
		
		if(F<31)
		{
			System.out.println("Easter Sunday is March " + F + ", in " + Year);
		}
		else
		{
			System.out.println("Easter Sunday is April " + (F-31) + ", in " + Year);
		}
	}
}
		