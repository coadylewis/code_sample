import java.text.DecimalFormat;

public class dup
{
	private int iterations;
	
	public dup(int it)
	{
		iterations=it;
	}
	public dup()
	{
		iterations=0;
	}
	
	DecimalFormat output = new DecimalFormat("0.00");
	
	int acc=0;
	
	
	public boolean test()
	{
		int num1[] = new int[10];
		int num2[] = new int[10];
		for(int i=0;i<10;i++)
		{	
			num1[i]=(int)(Math.random() * 100 + 1);
			num2[i]=(int)(Math.random() * 100 + 1);
		}
		for(int i=0;i<10;i++)
		{
			for(int k=0;k<10;k++)
			{
				if(num1[i]==num2[k])
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
		String percentage="In "+iterations+" Iterations, A Match Occured "+output.format((double)acc/iterations*100)+"% Of The Time.";
		int acc=0;
		return percentage;
	}
	
	
}