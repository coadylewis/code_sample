import java.util.Scanner;

public class clAlpha
{
	public static void main(String[] args)
	{
			Scanner input = new Scanner(System.in);
			int C=1;
			while(C!=0)
			{
				System.out.println("\n\nEnter A String Of Letters(0 to Exit)");
				String enter=new String(input.nextLine());
				if(enter.equals("0"))
					break;
				alpha karel = new alpha(enter);
				System.out.println("\n\n"+karel);
			}
	}
}