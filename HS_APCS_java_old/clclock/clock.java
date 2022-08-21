public class clock
{
	private int hour,cmin,min;
	private boolean am;
	
	public clock(int h,int cm,int m,boolean a)
	{
		hour=h;
		cmin=cm;
		min=m;
		am=a;
	}
	
	public clock()
	{
		hour=0;
		cmin=0;
		min=0;
		am=true;
	}
	
	int ctmin=0;
	int nhour=0;
	int nmin=0;
	
	public void calcmin()
	{
		if(am==true)
		{
			if(hour==12)
				ctmin=cmin;
			else
				ctmin=60*hour+cmin;
		}
		else
		{
			if(hour==12)
				ctmin=12*60+cmin;
			else
				ctmin=(hour+12)*60+cmin;
		}
	}
	
	public void findhour(int m)
	{
		if(m>1440)
			nhour=(m%1440)/60;
		if(m==1440)
			nhour=0;
		if(m<1440)
			nhour=m/60;	
	}
	
	public void findmin(int m)
	{
		if(m>1440)
			nmin=(m%1440)%60;
		if(m==1440)
			nmin=0;
		if(m<1440)
			nmin=m%60;
	}
	
	public int finalMin()
	{
		findmin(ctmin+min);
		return nmin;
	}
	
	public int finalHour()
	{
		findhour(ctmin+min);
		if(nhour<12)
		{
			am=true;
			if(nhour==0)
				return 12;
			else
				return nhour;
		}
		else
		{
			am=false;
			if(nhour==12)
				return nhour;
			else
				return nhour-12;
		}
	}
	
	public String toString()
	{
		calcmin();
		String ct="The Current Time Is "+finalHour()+":";
		
		if(finalMin()<10)
			ct=ct+"0"+finalMin();
		else
			ct=ct+finalMin();
		if(am==true)
			ct=ct+" AM";
		else
			ct=ct+" PM";
			
		ctmin=0;
		nhour=0;
		nmin=0;
		return ct;
	}	
}