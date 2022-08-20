import java.text.DecimalFormat;

public class NES
{
	private double kwh;
	private final double RESF75=.03907;
	private final double RESN150=.02757;
	private final double RESN275=.01537;
	private final double RESO500=.01177;
	private final double RESMIN=1.25;
	private final double COMF100=.03929;
	private final double COMN400=.02729;
	private final double COMU50ADD=.01729;
	private final double COMF15K=.01129;
	private final double COMN25K=.00929;
	private final double COMN60K=.00699;
	private final double COMN400K=.00589;
	private final double COMO50ADD=.00569;
	private final double COMDEM=2.01;
	public NES(double k)
	{
		kwh=k;
	}
	
	DecimalFormat output = new DecimalFormat("$0.00");
	
	public String Commercial(double kw)
	{
		String out="";
		double total=0;
		if(kw<50)
		{
			if(kwh>500)
				total+=(kwh-500)*COMU50ADD+100*COMF100+400*COMN400;
			if((kwh>100)&&(kwh<=500))
				total+=100*COMF100+(kwh-100)*COMN400;
			if(kwh<=100)
				total+=kwh*COMF100;
			out+="The Total Bill Is "+output.format(total);
		}
		else
		{
			total+=kw*COMDEM;
			if(kwh>500000)
				total+=(kwh-500000)*COMO50ADD+400000*COMN400K+60000*COMN60K+25000*COMN25K+15000*COMF15K;
			if((kwh>100000)&&(kwh<=500000))
				total+=(kwh-100000)*COMN400K+60000*COMN60K+25000*COMN25K+15000*COMF15K;
			if((kwh>40000)&&(kwh<=100000))
				total+=(kwh-40000)*COMN60K+25000*COMN25K+15000*COMF15K;
			if((kwh>15000)&&(kwh<=40000))
				total+=(kwh-15000)*COMN25K+15000*COMF15K;
			if(kwh<=15000)
				total+=kwh*COMF15K;
			out+="The Total Bill Is "+output.format(total);
		}
		return out;
	}
	
	public String Residential()
	{
		String out="";
		double total=0;
		if(kwh>500)
			total+=(kwh-500)*RESO500+275*RESN275+150*RESN150+75*RESF75;
		if((kwh>225)&&(kwh<=500))
			total+=(kwh-225)*RESN275+150*RESN150+75*RESF75;
		if((kwh>75)&&(kwh<=225))
			total+=(kwh-75)*RESN150+75*RESF75;
		if(kwh<=75)
			total+=kwh*RESF75;
		if(total<RESMIN)
			total=RESMIN;
		out+="The Total Bill Is "+output.format(total);
		return out;
	}
	
	
	
	
	
	
	
}