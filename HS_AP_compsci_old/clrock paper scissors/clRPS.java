import java.util.Scanner;

public class clRPS
{
	public static void main(String[] args)
	{
		Scanner input = new Scanner(System.in);
		String C="Y";
		int player=0;int wins=0;int ties=0;int losses=0; 
		while(C.equals("Y")||C.equals("y"))
		{
			System.out.println("\n\nEnter R for Rock, P for Paper, or S for Scissors");
				String option=input.nextLine();
			if(option.equals("R")||option.equals("r"))
				player=1;
			if(option.equals("P")||option.equals("p"))
				player=2;
			if(option.equals("S")||option.equals("s"))
				player=3;
			rps doge = new rps(player);
			String test=""+doge;
			System.out.println(test);
			if(test.contains("You Won"))
				wins++;
			if(test.contains("You Tied"))
				ties++;
			if(test.contains("You Lost"))
				losses++;
			test.replace(""+doge,"");
			System.out.println("\n\nWins: "+wins+"\nTies: "+ties+
			"\nLosses: "+losses+"\n\n");
			System.out.println("\n\nWould You Like To Play Again?(Y/N)\n");
				C=input.nextLine();
			while(!(C.equals("Y")||C.equals("y")||C.equals("N")||C.equals("n")))
			{
				System.out.println("Error, Enter Y or N");
				C=input.nextLine();
			}
			
		}
	}
}