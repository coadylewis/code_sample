import java.util.Scanner;


public class clnumber

{	public static void main(String [] args)
	{
		
	Scanner input = new Scanner(System.in);
	
	int number = (int)(Math.random() * 100 + 1);
	int guesses;
	int x;
	
	guesses=1;
	
	ngame game = new ngame(number);

	
	System.out.println("It's Game Day! Enter a Number Between 1 and 100\n");
	while(!game.checkNumber(x=input.nextInt()))
	{
		if(x>0&&x<101)
		{
			guesses=guesses+1;
			System.out.println(game.toString(x));
		}
		else
		{
			System.out.println("\nError, The Number Must Be Between 1 and 100.");
			break;
		}
	}
	if(x>0&&x<101)
		{
			System.out.println("\nCongratulations, you guessed correctly; it took you " + guesses + " guesses.");
		}
	}
}	