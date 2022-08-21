import java.util.ArrayList;

public class beads
{
	private int first,second;
	ArrayList<Integer> nums = new ArrayList<Integer>();
	public beads(int f, int s)
	{
		first=f;
		second=s;
	}
	public beads()
	{
		first=1;
		second=1;
	}
	
	private void generate()
	{
		nums.add(first);
		nums.add(second);
		do
		{
			next();	
		}
		while(test());
	}
	
	private boolean test()
	{
		if(((nums.get(nums.size()-1))==second)&&((nums.get(nums.size()-2))==first))
			return false;
		else
			return true;
	}
	
	private void next()
	{
		nums.add((nums.get(nums.size()-1)+nums.get(nums.size()-2))%10);
	}
	
	public String toString()
	{
		generate();
		String output="\n"+nums.get(0);
		int cycles=1;
		for(int i=1;i<nums.size();i++)
		{
			output=output+", "+nums.get(i);
			cycles++;
		}
		cycles=cycles-2;
		output=output+"\n\nIt Took "+cycles+" Cycles To Return To The Original Numbers";
		nums.clear();
		return output;	
	}
}