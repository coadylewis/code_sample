import java.util.Scanner;
import java.text.DecimalFormat;

public class clfa

{	public static void main(String [] args)
	{
		
	Scanner input = new Scanner(System.in);
	
	int Length, Width;


	System.out.println("Enter The Length");
		Length = input.nextInt();
	System.out.println("");
	
	
	System.out.println("Enter The Width");
		Width = input.nextInt();
	System.out.println("");
	
	DecimalFormat output = new DecimalFormat("$0.00");
	
	FrameArt brian = new FrameArt(Length, Width);
	
	
	System.out.println("The Price Of The Glass Is " + output.format(brian.GlassPrice()));
		System.out.println("");
	System.out.println("The Price Of The Wood Is " + output.format(brian.WoodPrice()));
		System.out.println("");
	System.out.println("The Total Price To Frame The Artwork Is " + output.format(brian.TotalPrice()));
	
	}
}