import java.util.ArrayList;

public class perfect
{
	private static int number;
	public perfect(int n)
	{
		number=n;
	}
	
	
	public static ArrayList pnumber()
	{
		ArrayList<Integer> output = new ArrayList<Integer>();
		for(int i=2;i<number;i++)
		{
			factor pf=new factor(i);
			ArrayList<Integer> test = pf.allFactors();
			int sum=0;
			for(int j=0;j<test.size();j++)
			{
				sum+=test.get(j);
			}
			if(sum==i)
				output.add(i);
		}
		return output;
	}
	
	
	
	
}