import java.text.DecimalFormat;
import java.util.ArrayList;

public class riemann
{
	private int function,n;
	private double a,b,c,lower,upper;
	ArrayList<Double> y = new ArrayList<Double>();
	public riemann(int f,double aa,double bb,double cc,double l,double u,int nn)
	{
		function=f;
		a=aa;
		b=bb;
		c=cc;
		lower=l;
		upper=u;
		n=nn;
	}
	
	DecimalFormat output = new DecimalFormat("0.000");
	
	private void generate()
	{
		if(function==1)
			for(double i=lower;i<=upper;i+=((lower+upper)/n))
				y.add(1.0*a*(i+b)+c);
		if(function==2)
			for(double i=lower;i<=upper;i+=((lower+upper)/n))
				y.add(1.0*a*(i+b)*(i+b)+c);
		if(function==3)
			for(double i=lower;i<=upper;i+=((lower+upper)/n))
				y.add(1.0*a*(i+b)*(i+b)*(i+b)+c);
		if(function==4)
			for(double i=lower;i<=upper;i+=((lower+upper)/n))
				y.add(a*(Math.sin(1.0*(i+b)))+c);
		if(function==5)
			for(double i=lower;i<=upper;i+=((lower+upper)/n))
				y.add(a*(Math.sin(1.0*(i*b)))+c);
	}
	
	public String toString()
	{
		generate();
		String out="\n\nThe RRAM Is ";
		double rsum=0.0;double lsum=0.0;double tsum=0.0;
		for(int i=1;i<y.size();i++)
			rsum+=(y.get(i))*((lower+upper)/n);
		for(int i=0;i<(y.size()-1);i++)
			lsum+=(y.get(i))*((lower+upper)/n);
		tsum=(rsum+lsum)/2;
		out+=output.format(rsum)+"\nThe LRAM Is "+output.format(lsum)+"\n"+
		"The Trapezoidal Sum Is "+output.format((double)(Math.round(tsum*1000))/1000);
		return out;	
	}
}