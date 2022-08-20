import java.util.Scanner;

public class clPrime
{
	public static void main(String[] args)
	{
		Scanner input = new Scanner(System.in);
		int number=1;
		while(number!=0)
		{
			System.out.print("Enter A Number To Find Its Prime ");
			System.out.print("Factors (0 To Exit)\n");
			number=input.nextInt();
			if(number==0)
				break;
			tester brad = new tester(number);
			System.out.println(brad);
		}
	}
}