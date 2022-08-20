import java.util.Scanner;

public class clwa

{	public static void main(String [] args)
	{
		
	Scanner input = new Scanner(System.in);
		
	int Test1, Test2, Test3;
	
	System.out.println("Enter 1st Score");
	
	Test1 = input.nextInt();
	
	System.out.println("Enter 2nd Score");
	
	Test2 = input.nextInt();
	
	System.out.println("Enter 3rd Score");
	
	Test3 = input.nextInt();
	
	
	scoreweight travis = new scoreweight(Test1, Test2, Test3);
	
	
	System.out.println("Weighted Value of 1st Score is " + travis.weight1());
	System.out.println("Weighted Value of 2nd Score is " + travis.weight2());
	System.out.println("Weighted Value of 3rd Score is " + travis.weight3());
	System.out.println("Weighted Average is " + travis.sum());
	}
}