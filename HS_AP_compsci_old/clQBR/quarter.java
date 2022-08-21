import java.text.DecimalFormat;

public class quarter
{
	private double att,com,yg,tdp,nint;
	private String name;
	
	public quarter(String n,double a,double c,double y,double t,double i)
	{
		name=n;
		att=a;
		com=c;
		yg=y;
		tdp=t;
		nint=i;
	}
	public quarter()
	{
		name="Vince Young";
		att=1;
		com=1;
		yg=1;
		tdp=1;
		nint=1;
	}
	
	DecimalFormat output = new DecimalFormat("0.0");
	
	private double one()
	{
		return (((com/att*100)-30)*0.05);
	}
	
	private double two()
	{
		return (((yg/att)-3)*0.25);
	}
	
	private double three()
	{
		return ((tdp/att*100)*0.20);
	}
	
	private double four()
	{
		return (2.375-((nint/att*100)*0.25));
	}
	
	private double five()
	{
		return ((one()+two()+three()+four())/6*100);
	}
	
	public String toString()
	{
		String rating="Name: "+name+"\nAtt: "+Math.round(att)+"\nComp: "+
		Math.round(com)+"\nYG: "+Math.round(yg)+"\nTD: "+Math.round(tdp)+
		"\nInt: "+Math.round(nint)+"\nQBR: "+output.format(five())+"\n";
		return rating;
	}	
}