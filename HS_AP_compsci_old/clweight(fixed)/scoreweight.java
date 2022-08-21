public class scoreweight
{
	private int Test1, Test2, Test3;
	
	public final double WT1 = 0.3, WT2 = 0.25, WT3 = 0.45;
	
	public scoreweight(int T1, int T2, int T3)

	{
		Test1=T1;
		Test2=T2;
		Test3=T3;
	}
	
	
	public double weight1()
	{
		return Test1*WT1;
	}
	
	
	public double weight2()
	{
		return Test2*WT2;
	}
	
	
	public double weight3()
	{
		return Test3*WT3;
	}
	
	
	public double sum()
	{
		return weight1()+weight2()+weight3();
	}
	
}