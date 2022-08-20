import java.text.DecimalFormat;

public class birthday
{
	private int iterations;
	private int people;
	
	public birthday(int it, int p)
	{
		iterations=it;
		people=p;
	}
	public birthday()
	{
		iterations=1;
		people=1;
	}
	
	DecimalFormat output = new DecimalFormat("0.00");
	
	int acc=0;
	
	
	public boolean test()
	{
		int num[] = new int[people];
		for(int i=0;i<people;i++)
		{	
			num[i]=(int)(Math.random() * 365 + 1);
		}
		for(int i=0;i<people;i++)
		{
			for(int k=0;k<people;k++)
			{
				if((i==k)&&(k==(people-1)))
				{
					return false;
				}
				if(i==k)
				{
					k++;
				}
				if(num[i]==num[k])
				{
					return true;
				}
			}
		}
		return false;		
	}
	
	public void acc()
	{
		
		if(test())
		acc++;
	}
	
	public String toString()
	{
		String percentage="In "+iterations+" Tests of a Room with "+people+
		" People, Two People Had the Same Birthday "+output.format((double)acc/iterations*100)+"% Of The Time.";
		int acc=0;
		return percentage;
	}
	
	
}