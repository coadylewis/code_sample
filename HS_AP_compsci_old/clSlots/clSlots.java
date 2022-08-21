import java.util.Scanner;

public class clSlots
{
	public static void main(String[] args)
	{
			Scanner input = new Scanner(System.in);
			int C=1;
			
			slots tillmankareldean = new slots();
			while(C!=0)
			{
				if(tillmankareldean.coins==0)
					break;
				System.out.println("\n\nPress [ENTER] To Play(0 to Exit)");
				String enter=new String(input.nextLine());
				if(enter.equals("0"))
					break;
				System.out.println("\n\n"+tillmankareldean);	
			}
	}
}