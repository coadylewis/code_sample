public class counter
{
	private int nmbr;
	
	public counter(int n)
	{
		nmbr=n;
	}
	public counter()
	{
		nmbr=1;
	}
	
	public void generate(int[] n)
	{
		for(int i=0;i<n.length;i++)
			n[i]=((int)(Math.random()*51));
	}
	
	public int freq(int x,int[] n)
	{
		int count=0;
		for(int j=0;j<(n.length);j++)
		{
			if(x==n[j])
				count++;
		}
		return count;
	}
	
	public String toString()
	{
		int nums[] = new int[nmbr];
		generate(nums);
		String list="\n";
		String dist="";
		for(int i=0;i<nums.length;i++)
		{
			list=list+nums[i]+ "     ";
		}
		
		for(int i=0;i<51;i++)
		{
			if(i==51)
				break;
			if(freq(i,nums)!=0)
				dist=dist+i+ "	"+freq(i,nums)+" times\n";
		}
		String total=list+"\n\n"+dist;
		return total;		
	}
}