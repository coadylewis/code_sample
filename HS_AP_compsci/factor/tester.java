public class tester
{
	int number;
	public tester(int n)
	{
		number=n;
	}

private boolean prime(int n)
{
	for(int i=2;i<=Math.sqrt(n);i++)
	{
		if(n%i==0)
			return false;
	}
	return true;
}

public String toString()
{
	String factors="";
	int test=number;
	if(prime(number))
	{
		factors+="The Number Is Prime\n\n";
	}
	else
	{
		factors+="The Number's Prime Factors Are:  ";
	}
	while(!prime(number))
	{
		for(int i=number;i>1;i--)
		{
			if(prime(i)&&(number%i==0))
			{
				factors+=i+",  ";
				number=number/i;
				break;
			}
		}
	}
	if(!(number==test))
		factors+="And "+number+"\n\n";
	String error="";
	if(test<=1)
	{
		error+="Only Positive Integers Greater Than One Have Prime Factors\n\n";
		return error;
	}
	return factors;
}
}