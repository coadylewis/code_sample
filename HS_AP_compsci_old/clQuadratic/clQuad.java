import java.util.Scanner;

public class clQuad
{
	public static void main(String[] args)
	{
			Scanner input = new Scanner(System.in);
			String C="Y";
			double a,b,c;
			
		System.out.println("This Program Solves Quadratic Equations of the Form A(X^2)+B(X)+C=0\n");
		while(C.equals("Y")||C.equals("y"))
		{
			System.out.println("\nEnter A");
			a=input.nextDouble();
			System.out.println("Enter B");
			b=input.nextDouble();
			System.out.println("Enter C");
			c=input.nextDouble();
			quadratic karel = new quadratic(a,b,c);
			if(karel.onesol())
			System.out.println("\nx = "+karel.one());
			if(karel.twosol())
			System.out.println("\nx = "+karel.two());
			if(karel.imag())
			System.out.println("\nx = "+karel.imaginary());
			System.out.println("Would you like to solve another equation?(Y/N)");
			C=input.next();
			while(!(C.equals("Y")||C.equals("y")||C.equals("N")||C.equals("n")))
			{
				System.out.println("Error, Enter Y or N");
				C=input.next();
			}
		}
	}
}