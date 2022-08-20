public class ngame
{
	public int number;
	
	public ngame(int n)
	{
		number=n;
	}
	public ngame()
	{
		number=0;
	}
	
	public boolean checkNumber(int i)
	{
			if(number==i)
			{
				return true;
			}
			else
			{
				return false;
			}
		}
		
	
	public String toString(int i)
	{
		String less="The Number is less than "+i;
		String greater="The Number is greater than "+i;
		if(i>number)
		{
			return less;
		}
		else
		{
			return greater;
		}
	}	
}