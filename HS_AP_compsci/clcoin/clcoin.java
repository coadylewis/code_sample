public class clcoin

{	public static void main(String [] args)
	{
		
	int Pennies, Nickels, Dimes, Quarters;
	
	
	
	
	Pennies = 3;
	
	Nickels = 4;
	
	Dimes = 5;
	
	Quarters = 6;
	
	
		
	cchanger brian = new cchanger(Pennies, Nickels, Dimes, Quarters);
	
	brian.setPennies(5);
	brian.setNickels(6);
	brian.setDimes(10);
	brian.setQuarters(3);
	
	System.out.println("");
	System.out.println(brian);
	
	}
}