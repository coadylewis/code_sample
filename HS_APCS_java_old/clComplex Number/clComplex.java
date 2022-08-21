import java.util.Scanner;
import java.text.DecimalFormat;

public class clComplex
{
	public static void main(String[] args)
	{
		
		Scanner input = new Scanner(System.in);
		DecimalFormat output = new DecimalFormat("0.000");
		cnumber brian = new cnumber();
		
		
		System.out.println("The default complex number is ");
		System.out.println(brian);
		
		cnumber karel = new cnumber();
		karel.setReal(3);
		karel.setImaginary(2);
		
		System.out.println("You have set complex number A as");
		System.out.println(karel);
		
		
		double real, imag;
		String C = "Y";
	
		while(C.equals("Y")||C.equals("y"))
		{
			System.out.println("");
			System.out.println("Now Input Complex Number B");
			System.out.println("Enter the real part");
				real = input.nextDouble();
			System.out.println("Enter the imaginary part");
				imag = input.nextDouble();
			cnumber compton = new cnumber(real, imag);
			System.out.println("You have input " +compton);
			System.out.println("");
			System.out.println("A+B= " +karel.add(compton));
			System.out.println("");
			System.out.println("A-B= " +karel.sub(compton));
			System.out.println("");
			System.out.println("A*B= " +karel.mul(compton));
			System.out.println("");
			System.out.println("A/B= " +karel.div(compton));
			System.out.println("");
			System.out.println("The product of B and its conjugate is " + compton.getConjugate(compton));
			System.out.println("");
			System.out.println("The Angle of Complex Number B is " + output.format(Math.atan((imag/real))) + " radians");
			System.out.println("");
			
			System.out.println("Would you like to enter a different value of B?");
			C = input.next();
			System.out.println("");
			System.out.println("");
			System.out.println("");
		}
		
		
		
		
		
	}
}