import java.util.ArrayList;

public class penny
{
	int[] boardindex = new int[25];
	String[] board = new String[25];
	boolean[] pennies = new boolean[25];
	public penny(){}
	
	
	public void assign()
	{
		for(int i=0;i<25;i++)
			boardindex[i]=0;
		for(int j=1;j<6;j++)
		{
			for(int i=0;i<3;i++)
			{
				int x=((int)(Math.random()*25));
				while(boardindex[x]!=0)
					x=((int)(Math.random()*25));
				boardindex[x]=j;
			}
		}
		for(int i=0;i<25;i++)
		{
			if(boardindex[i]==0)
				board[i]="|        |";
			if(boardindex[i]==1)
				board[i]="| PUZZLE |";
			if(boardindex[i]==2)
				board[i]="| POSTER |";
			if(boardindex[i]==3)
				board[i]="|  DOLL  |";
			if(boardindex[i]==4)
				board[i]="|  GAME  |";
			if(boardindex[i]==5)
				board[i]="|  BALL  |";
		}	
	}
	
	
	public String printboard()
	{
		String output="";
		for(int j=0;j<5;j++)
		{
			for(int i=0;i<5;i++)
				output+=board[j*5+i];
			output+="\n";
		}
		return output;
	}
	
	
	public void toss()
	{
		for(int i=0;i<25;i++)
			pennies[i]=false;
		for(int i=0;i<10;i++)
		{
			int x=((int)(Math.random()*25));
			while(pennies[x]==true)
				x=((int)(Math.random()*25));
			pennies[x]=true;
		}
		for(int i=0;i<25;i++)
		{
			if(pennies[i]==true)
				board[i]="|*PENNY**|";
		}
	}
	
	
	public String toString()
	{
		String output="YOUR PRIZES ARE:";
		int count1=0,count2=0,count3=0,count4=0,count5=0;
		for(int i=0;i<25;i++)
		{
			if(board[i].equals("| PUZZLE |"))
				count1++;
			if(board[i].equals("| POSTER |"))
				count2++;
			if(board[i].equals("|  DOLL  |"))
				count3++;
			if(board[i].equals("|  GAME  |"))
				count4++;
			if(board[i].equals("|  BALL  |"))
				count5++;
		}
		int count=count1+count2+count3+count4+count5;
		if(count1==0)
			output+=" PUZZLE ";
		if(count2==0)
			output+=" POSTER ";
		if(count3==0)
			output+=" DOLL ";
		if(count4==0)
			output+=" GAME ";
		if(count5==0)
			output+=" BALL ";
		if(count1!=0&&count2!=0&&count3!=0&&count4!=0&&count5!=0)
			output+=" ABSOLUTELY NOTHING, BETTER LUCK NEXT TIME!!! ";
		
		
		
		
		
		return output;
	}
	
	
	
	
	
	
	
	
}