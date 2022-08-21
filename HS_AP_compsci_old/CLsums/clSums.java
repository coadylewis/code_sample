import java.util.Scanner;

public class clSums
{
	public static void main(String[] args)
	{
		Scanner input = new Scanner(System.in);
		System.out.println("Enter A Function Format\n1) Y=A(X+B)+C\t2) Y=A((X"+
		"+B)^2)+C\t3) Y=A((X+B)^3)+C\t4) Y=A(sin(X+B))+C\t5) Y=A(sin(BX))+C");
			int function=input.nextInt();
		System.out.println("Enter Numbers For A B And C");
			double a=input.nextDouble();
			double b=input.nextDouble();
			double c=input.nextDouble();
		System.out.println("Enter A Lower And Upper Bound For The Sum");
			double lower=input.nextDouble();
			double upper=input.nextDouble();
		System.out.println("Enter An Integer For The Number Of Subintervals");
			int n=input.nextInt();
		
		riemann rap = new riemann(function,a,b,c,lower,upper,n);
		System.out.println(rap);	
	}
}