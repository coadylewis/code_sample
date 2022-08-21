import java.util.ArrayList;
import java.util.Collections;

public class pleasework
{
	public final int NUMBER=200;
	ArrayList<Integer> nums = new ArrayList<Integer>();
	public pleasework(){}
	
	public int generate(int x)
	{
		nums.add(x);
		do
		{
			next();	
		}
		while(test());	
		return nums.size()-1;
	}
	
	public boolean test()
	{
		if((nums.get(nums.size()-1))==1&&(nums.contains(2))&&(nums.contains(4)))
			return false;
		else
			return true;
	}
	
	public void next()
	{
		if((nums.get(nums.size()-1)%2)==0)
			nums.add((nums.get(nums.size()-1))/2);
		else
			nums.add((nums.get(nums.size()-1)*3)+1);
	}	
	
	public String toString()
	{
		String output="";
		ArrayList<Integer> mx = new ArrayList<Integer>();
		for(int i=1;i<NUMBER;i++)
		{
			output=output+"\n"+i+": "+generate(i)+" cycles";
			nums.clear();
			mx.add(generate(i));
			nums.clear();
		}
		int y=Collections.max(mx);
		generate((mx.indexOf(y)+1));
		output=output+"\n\n\n"+"Number Requiring Maximum Cycles Is "
		+(mx.indexOf(y)+1)+" With "+y+" Cycles Required\n\n\nThe Sequence For "+(mx.indexOf(y)+1)+" Is:\n\n"
		+nums+"\n\n";
		nums.clear();
		mx.clear();
		y=0;
		return output;
	}
}