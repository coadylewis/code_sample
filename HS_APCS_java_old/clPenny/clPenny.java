import java.util.Scanner;

public class clPenny
{
	public static void main(String[] args)
	{
		Scanner input = new Scanner(System.in);
		int holder=0;
		while(holder==0)
		{
			System.out.println("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
			System.out.println("This Program Simulates Tossing Ten Pennies At A Board");
			System.out.println("The Current Board Is:\n\n");
			penny test = new penny();
			test.assign();
			System.out.println(test.printboard()+"\n\nPress [ENTER] To Toss Ten Pennies");
			input.nextLine();
			test.toss();
			System.out.println("The New Board Is:\n\n"+test.printboard()+"\n\n");
			System.out.println("Press [ENTER] To See Your Results");
			input.nextLine();
			System.out.println(test+"\n\nPress [ENTER] To Play Again (CTRL+C To Exit)");
			input.nextLine();
			System.out.println("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
		}
	}
}





