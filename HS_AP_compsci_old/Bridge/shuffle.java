import java.util.ArrayList;

public class shuffle
{
	String[][] deck = {{"2C","3C","4C","5C","6C","7C","8C","9C","10C","JC","QC","KC","AC"},
	{"2D","3D","4D","5D","6D","7D","8D","9D","10D","JD","QD","KD","AD"},
	{"2H","3H","4H","5H","6H","7H","8H","9H","10H","JH","QH","KH","AH"},
	{"2S","3S","4S","5S","6S","7S","8S","9S","10S","JS","QS","KS","AS"}};
	String[][] shuffleddeck = new String[4][13];
	boolean[][] test = new boolean[4][13];
	String[] testdeck = new String[52];
	String[] first = new String[13];
	String[] second = new String[13];
	String[] third = new String[13];
	String[] fourth = new String[13];
	ArrayList<String> al1 = new ArrayList<String>();
	ArrayList<String> al2 = new ArrayList<String>();
	ArrayList<String> al3 = new ArrayList<String>();
	ArrayList<String> al4 = new ArrayList<String>();
	
	public shuffle(){}
	
	private void shuffle()
	{
		for(int i=0;i<4;i++)
		{
			for(int j=0;j<13;j++)
				test[i][j]=false;
		}
		
		for(int i=0;i<4;i++)
		{
			for(int j=0;j<13;j++)
			{
				int s=(int)(Math.random()*4);
				int c=(int)(Math.random()*13);
				while(test[s][c])
				{
					s=(int)(Math.random()*4);
					c=(int)(Math.random()*13);
				}
				test[s][c]=true;
				shuffleddeck[i][j]=deck[s][c];
			}
		}
	}
	
	private void testdeck()
	{
		for(int i=0;i<4;i++)
		{
			for(int j=0;j<13;j++)
				testdeck[13*i+j]=deck[i][j];
		}
	}
	
	private void hands()
	{
		for(int i=0;i<13;i++)
			first[i]=shuffleddeck[0][i];
		for(int i=0;i<13;i++)
			second[i]=shuffleddeck[1][i];
		for(int i=0;i<13;i++)
			third[i]=shuffleddeck[2][i];
		for(int i=0;i<13;i++)
			fourth[i]=shuffleddeck[3][i];
	}
	
	private void sort()
	{
		for(int i=0;i<52;i++)
		{
			for(int j=0;j<13;j++)
			{
				if(testdeck[i]==first[j])
					al1.add(first[j]);
			}
		}
		for(int i=0;i<52;i++)
		{
			for(int j=0;j<13;j++)
			{
				if(testdeck[i]==second[j])
					al2.add(second[j]);
			}
		}
		for(int i=0;i<52;i++)
		{
			for(int j=0;j<13;j++)
			{
				if(testdeck[i]==third[j])
					al3.add(third[j]);
			}
		}
		for(int i=0;i<52;i++)
		{
			for(int j=0;j<13;j++)
			{
				if(testdeck[i]==fourth[j])
					al4.add(fourth[j]);
			}
		}
	}
	
	public String toString()
	{
		String output="";
		shuffle();
		testdeck();
		hands();
		sort();
		output+="The First Hand Is "+al1+"\nThe Second Hand Is "+al2+
		"\nThe Third Hand Is "+al3+"\nThe Fourth Hand Is "+al4;
		return output;
	}	
}