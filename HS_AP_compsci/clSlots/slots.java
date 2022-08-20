public class slots
{
	
	private String result="";
	int[] first=new int[]{1,1,1,2,2,3,4};
	int[] second=new int[]{1,1,2,2,2,3,4};
	int[] third=new int[]{1,1,2,2,3,3,4};
	int[] rescode=new int[3];
	public static int coins=5;
	public slots()
	{
	}
	
	private int roll()
	{
		int winnings=0;
		rescode[0]=first[(int)(Math.random()*7)];
		rescode[1]=second[(int)(Math.random()*7)];
		rescode[2]=third[(int)(Math.random()*7)];
		for(int i=0;i<3;i++)
		{
			if(rescode[i]==1)
				result+="|CHERRY|";
			if(rescode[i]==2)
				result+="|PLUM|";
			if(rescode[i]==3)
				result+="|BELL|";
			if(rescode[i]==4)
				result+="|BAR|";
		}
		if((rescode[0]==2)&&(rescode[1]!=2))
			winnings+=2;
		if((rescode[0]==2)&&(rescode[1]==2)&&(rescode[2]!=2))
			winnings+=4;
		if((rescode[0]==2)&&(rescode[1]==2)&&(rescode[2]==2))
			winnings+=20;
		if((rescode[0]==3)&&(rescode[1]!=3))
			winnings+=4;
		if((rescode[0]==3)&&(rescode[1]==3)&&(rescode[2]!=3))
			winnings+=8;
		if((rescode[0]==3)&&(rescode[1]==3)&&(rescode[2]==3))
			winnings+=100;
		if((rescode[0]==4)&&(rescode[1]!=4))
			winnings+=4;
		if((rescode[0]==4)&&(rescode[1]==4)&&(rescode[2]!=4))
			winnings+=8;
		if((rescode[0]==4)&&(rescode[1]==4)&&(rescode[2]==4))
			winnings+=200;
		coins=coins-1+winnings;
		return winnings;
	}
	
	
	public String toString()
	{
		String out="";
		out+="You've Won "+roll()+" Coins\n";
		out+=result+"\nYou Have "+coins+" Remaining";
		result=new String("");
		return out;
	}
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
}