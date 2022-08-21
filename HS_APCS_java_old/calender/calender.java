import java.text.DecimalFormat;
import java.util.ArrayList;

public class calender
{
	
	private int days, first;
	ArrayList<String> nums = new ArrayList<String>();
	public calender(int d, int f)
	{
		days=d;
		first=f;
	}
	public calender()
	{
		days=30;
		first=1;
	}
	
	
	DecimalFormat out = new DecimalFormat("0000");
	
	private void generate(int da, int fi)
	{
		for(int i=0;i<(8-fi);i++)
			nums.add("    ");
		for(int i=0;i<da;i++)
			nums.add(out.format(i+1));
	}
	
	private String cal()
	{
		generate(days,first);
		String output="";
		for(int i=0;i<nums.size();i++)
		{
			output+=nums.get(i)+" ";
			if((i+1)%7==0)
				output+="\n";
		}
		output=output.replace("000","   ");
		output=output.replace("00","  ");
		return output;
	}
	
	public String toString()
	{
		String output="\n Sun  Mon  Tue  Wed  Thu  Fri  Sat \n";
		output+=cal()+"\n\n";
		return output;
	}
}
