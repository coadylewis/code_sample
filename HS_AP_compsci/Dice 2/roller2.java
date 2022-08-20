import java.text.DecimalFormat;
import java.util.Arrays;

public class roller2
{
	private int rolls;
	
	public roller2(int r)
	{
		rolls=r;
	}
	public roller2()
	{
		rolls=0;
	}
	
	DecimalFormat output = new DecimalFormat("0.000");
	
	int event=0;
	int freArray[] = new int[]{0,0,0,0,0,0,0,0,0,0,0};
	
	public String AleaIactaEst()
	{
		
		String dice="";		
		event=(int)(Math.random() * 6 + 1) + (int)(Math.random() * 6 + 1);
		freArray[event]++;
		dice=dice+"   "+event;
		return dice;		
	}
	
	public String toString()
	{
		String[] e = new String[11];
		String label = "EVENT          # OF TIMES          PERCENTAGE\n";
		for(int i=0;i<=10;i++)
		{	
			
			e[i]="    "+(i+2)+"          "+freArray[i]+"                  "+output.format((double)(freArray[i])/rolls*100)+"%\n";
		}
		return label + Arrays.toString(e);
	}
}