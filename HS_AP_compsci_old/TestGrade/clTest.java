import java.util.Scanner;

public class clTest
{
	public static void main(String[] args)
	{
		
	Scanner input = new Scanner(System.in);
		
	double Test1, Test2, Test3;
	String C = "Y";
	
	while(C.equals("Y")||C.equals("y"))
	{
		System.out.println("");
		System.out.println("Enter Points Earned On The 1st Test");
	
		Test1 = input.nextDouble();
	
		System.out.println("Enter Points Earned On The 2nd Test");
	
		Test2 = input.nextDouble();
	
		System.out.println("Enter Points Earned On The 3rd Test");
	
		Test3 = input.nextDouble();
	
		grader mrCompton = new grader(Test1,Test2,Test3);
	
		System.out.println("");	
		System.out.println(mrCompton);
		
		System.out.println("\nWould You Like To Determine Another Grade(Y/N)?");
		C = input.next();
	}
	}
}