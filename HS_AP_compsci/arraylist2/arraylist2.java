import java.util.ArrayList;

public class arraylist2
{
	private int number,choice;
	ArrayList<Integer> nums = new ArrayList<Integer>();
	public arraylist2(int n,int c)
	{
		number=n;
		choice=c;
	}
	public arraylist2()
	{
		number=0;
		choice=9;
	}
	
	private ArrayList generate(ArrayList<Integer> n)
	{
		for(int i=0;i<1000;i++)
			n.add((int)(Math.random()*90+10));
		return n;
	}
	
	private String display(ArrayList<Integer> n)
	{
		String output="";
		int s=0;
		int e=20;
		for(int i=0;i<50;i++)
		{
			for(int j=s;j<e;j++)
			{
				output+=n.get(j)+"   ";
			}
			s+=20;
			e+=20;
			output+="\n";
		}
		return output;
	}
	
	private String search(int x,ArrayList<Integer> n)
	{
		String output="";
		int count=0;
		ArrayList<String> index = new ArrayList<String>();
		for(int i=0;i<1000;i++)
		{
			if(n.get(i)==x)
			{
				count++;
				index.add(""+i);
			}
		}
		if(count==0)
			output+=x+" Does Not Appear In The List";
		else
			output+=x+" Appears "+count+" Times, The Indexes Are "+index;
		return output;
	}
	
	private ArrayList sort(ArrayList<Integer> x)
	{
		int lowest=100;
		int n=1000;
		ArrayList<Integer> s = new ArrayList<Integer>();
		for(int i=0;i<1000;i++)
		{
			int index=-1;
			for(int j=0;j<n;j++)
			{
				if(x.get(j)<lowest)
				{
					lowest=x.get(j);
					index=j;
				}
			}
			s.add(lowest);
			x.remove(index);
			n--;
			lowest=100;
		}
		return s;
	}
	
	private ArrayList rsort(ArrayList<Integer> x)
	{
		int largest=0;
		int n=1000;
		ArrayList<Integer> s = new ArrayList<Integer>();
		for(int i=0;i<1000;i++)
		{
			int index=-1;
			for(int j=0;j<n;j++)
			{
				if(x.get(j)>largest)
				{
					largest=x.get(j);
					index=j;
				}
			}
			s.add(largest);
			x.remove(index);
			n--;
			largest=0;
		}
		return s;
	}
	
	private String largest()
	{
		String output="The Largest Value Is ";
		int largest=0;
		int index=0;
		int count=0;
		for(int j=0;j<1000;j++)
		{
			if(nums.get(j)>largest)
			{
				largest=nums.get(j);
				index=j;
			}
		}
		output+=nums.get(index);
		for(int i=0;i<1000;i++)
		{
			if(nums.get(index)==nums.get(i))
				count++;
		}
		output+=", It Appears "+count+" Times";
		return output;
	}
	
	private String smallest()
	{
		String output="The Smallest Value Is ";
		int lowest=100;
		int index=0;
		int count=0;
		for(int j=0;j<1000;j++)
		{
			if(nums.get(j)<lowest)
			{
				lowest=nums.get(j);
				index=j;
			}
		}
		output+=nums.get(index);
		for(int i=0;i<1000;i++)
		{
			if(nums.get(index)==nums.get(i))
				count++;
		}
		output+=", It Appears "+count+" Times";
		return output;
	}
	
	private ArrayList copy(ArrayList<Integer> n)
	{
		ArrayList<Integer> o = new ArrayList<Integer>();
		for(int i=0;i<1000;i++)
			o.add(n.get(i));
		return o;
	}
	
	private int sum(ArrayList<Integer> n)
	{
		int sum=0;
		for(int i=0;i<1000;i++)
			sum+=n.get(i);
		return sum;
	}
	
	public String toString()
	{
		generate(nums);
		String output="";
		if(choice!=9)
		{
			output+="\n\nYour Base Arraylist is\n"+display(nums)+"\n\n";
		}
		if(choice==1)
		{
			nums.clear();
			generate(nums);
			output+="Your New Arraylist Is\n"+display(nums)+"\n\n";
		}
		if(choice==2)
		{
			output+="\n\n"+search(number,nums)+"\n\n";
		}
		if(choice==3)
		{
			output+="The Sorted Arraylist Is\n"+display(sort(nums))+"\n\n";
		}
		if(choice==4)
		{
			output+="The Reverse-Sorted Arraylist Is\n"+display(rsort(nums))+"\n\n";
		}
		if(choice==5)
		{
			output+=largest()+"\n\n";
		}
		if(choice==6)
		{
			output+=smallest()+"\n\n";
		}
		if(choice==7)
		{
			output+="The Copied Arraylist Is\n"+display(copy(nums))+"\n\n";
		}
		if(choice==8)
		{
			output+="The Sum Of The Elements In The Arraylist Is "+sum(nums);
		}
		nums.clear();
		return output;
	}	
}
	