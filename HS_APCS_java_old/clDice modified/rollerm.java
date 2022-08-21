import java.text.DecimalFormat;

public class rollerm
{
	private int rolls;
	
	public rollerm(int r)
	{
		rolls=r;
	}
	public rollerm()
	{
		rolls=0;
	}
	
	DecimalFormat output = new DecimalFormat("0.000");
	
	int event=0, fre2=0, fre3=0, fre4=0, fre5=0, fre6=0,
		fre7=0, fre8=0, fre9=0, fre10=0, fre11=0, fre12=0;
	
	public String AleaIactaEst()
	{
		String dice=event+ "	";
		event=(int)(Math.random() * 6 + 1) + (int)(Math.random() * 6 + 1);
		
		if(event==2)
		fre2++;
		if(event==3)
		fre3++;
		if(event==4)
		fre4++;
		if(event==5)
		fre5++;
		if(event==6)
		fre6++;
		if(event==7)
		fre7++;
		if(event==8)
		fre8++;
		if(event==9)
		fre9++;
		if(event==10)
		fre10++;
		if(event==11)
		fre11++;
		if(event==12)
		fre12++;
		return dice;		
	}
	
	public int totalRolls()
	{
		return fre2+fre3+fre4+fre5+fre6+fre7+fre8+fre9+fre10+fre11+fre12;
	}
	
	public String toString()
	{
		String label = "EVENT          # OF TIMES          PERCENTAGE\n";
		String e2="    2          "+fre2+"                  "+output.format((double)(fre2)/totalRolls()*100)+"%\n";
		String e3="    3          "+fre3+"                  "+output.format((double)(fre3)/totalRolls()*100)+"%\n";
		String e4="    4          "+fre4+"                  "+output.format((double)(fre4)/totalRolls()*100)+"%\n";
		String e5="    5          "+fre5+"                  "+output.format((double)(fre5)/totalRolls()*100)+"%\n";
		String e6="    6          "+fre6+"                  "+output.format((double)(fre6)/totalRolls()*100)+"%\n";
		String e7="    7          "+fre7+"                  "+output.format((double)(fre7)/totalRolls()*100)+"%\n";
		String e8="    8          "+fre8+"                  "+output.format((double)(fre8)/totalRolls()*100)+"%\n";
		String e9="    9          "+fre9+"                  "+output.format((double)(fre9)/totalRolls()*100)+"%\n";
		String e10="   10          "+fre10+"                  "+output.format((double)(fre10)/totalRolls()*100)+"%\n";
		String e11="   11          "+fre11+"                  "+output.format((double)(fre11)/totalRolls()*100)+"%\n";
		String e12="   12          "+fre12+"                  "+output.format((double)(fre12)/totalRolls()*100)+"%\n";
		return label+e2+e3+e4+e5+e6+e7+e8+e9+e10+e11+e12;
	}
}