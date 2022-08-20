import java.util.Scanner;

public class clPerfectNumber
{
	public static void main(String[] args)
	{
		Scanner input = new Scanner(System.in);
		System.out.println("This Program Finds All Perfect Numbers Less Than An Integer");
		System.out.println("Enter The Integer");
			int number=input.nextInt();
			while((number<=6))
			{
				System.out.println("Enter An Integer Greater Than Six");
				number=input.nextInt();
			}
		perfect out = new perfect(number);
		System.out.println(perfect.pnumber());
	}
}