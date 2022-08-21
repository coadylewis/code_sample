public class rps
{
	private int player,computer=1;
	public rps(int o)
	{
		player=o;

	}
	
	private void generate()
	{
		computer=(int)(Math.random()*3+1);
	}
	
	public String toString()
	{
		String output="";
		generate();
		if(player==computer)
		{
			output+="You Tied With The Computer";
		}
		if(player==1&&computer==2)
		{
			output+="You Lost, The Computer Played Paper";
		}
		if(player==1&&computer==3)
		{
			output+="You Won, The Computer Played Scissors";
		}
		if(player==2&&computer==1)
		{
			output+="You Won, The Computer Played Rock";
		}
		if(player==2&&computer==3)
		{
			output+="You Lost, The Computer Played Scissors";
		}
		if(player==3&&computer==1)
		{
			output+="You Lost, The Computer Played Rock";
		}
		if(player==3&&computer==2)
		{
			output+="You Won, The Computer Played Paper";
		}
		return output;
	}
	
}