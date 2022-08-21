import java.util.ArrayList;
import java.text.DecimalFormat;

public class interest
{
	private double principal,interest,x;
	public interest(double p,double i,double y)
	{
		principal=p;
		interest=i;
		x=y;
	}
	
	DecimalFormat output = new DecimalFormat("$0.00");
	
	public String monthly()
	{
		double out;
		double r=(interest/100)/12;
		double n=x*12;
		out=(((r)*Math.pow((1+r),n))/(Math.pow((1+r),n)-1))*principal;
		String s1=output.format(out);
		return s1;
	}
	
	public String toString()
	{
		String s1="";
		double r=(interest/100)/12;
		double n=x*12;
		double monthly=x;
		double ipay=r*principal;
		double isum=0;
		double ppay=monthly-ipay;
		double pbalance=principal;
		
		ArrayList<String> amort = new ArrayList<String>();
		amort.add("{MONTH} {MONTHLY PAYMENT} {INTEREST PAYMENT} {PRINCIPAL PAYMENT} {TOTAL INTEREST} {PRINCIPAL BALANCE}\n");
		int i=1;
		while(pbalance>0)
		{
			ipay=r*pbalance;
			
			ppay=monthly-ipay;
			if(ppay>pbalance)
			{
				monthly=pbalance+ipay;
				ppay=pbalance;
				isum+=ipay;
				amort.add(i+"          "+output.format(monthly)+"          "+output.format(ipay)+"          "+output.format(ppay)+"          "+output.format(isum)+"          $0.00");
				break;
			}
			isum+=ipay;
			pbalance=pbalance-ppay;
			
			amort.add(i+"          "+output.format(monthly)+"          "+output.format(ipay)+"          "+output.format(ppay)+"          "+output.format(isum)+"          "+output.format(pbalance)+"\n");
			i++;
		}
		amort.add("\n{MONTH} {MONTHLY PAYMENT} {INTEREST PAYMENT} {PRINCIPAL PAYMENT} {TOTAL INTEREST} {PRINCIPAL BALANCE}\n");
		String out="";
		for(int j=0;j<amort.size();j++)
			out+=amort.get(j);
		return out;
	}
}