import java.util.*;


public class arraylist
{
	private ArrayList<Integer> x = new ArrayList<Integer>();
	private ArrayList<Integer> y = new ArrayList<Integer>();
	private ArrayList<Integer> z = new ArrayList<Integer>();
	

	public void generatex()
	{
		for(int i=0;i<30;i++)
		{
			x.add((int)(Math.random()*100+1));
		}
	}

	
	public void generatey()
	{
		for(int i=0;i<30;i++)
		{
			y.add((int)(Math.random()*100+1));
		}
	}




	public void generatez()
	{
		for(int i=0;i<30;i++)
		{
			z.add((x.get(i))*(y.get(i)));
		}
	}


	public int sum()
	{
		int zsum=0;
		for(int i=0;i<30;i++)
		{
			zsum=zsum+z.get(i);
		}
		return zsum;
	}


	public String toString()
	{
		generatex();
		generatey();
		generatez();
		String label="This Program Generates Two 30 Element ArrayLists, X And Y, With Each Element Being A Random Number From 1 To 100.\nA Third ArrayList, Z, Has 30 Elements That Are The Product Of The Corresponding X And Y Elements.\n\nX,      Y,      Z\n";
		String columns="";
		for(int i=0;i<30;i++)
		columns=columns+x.get(i)+"      "+y.get(i)+"      "+z.get(i)+"\n";
		String output="The Sum Of All Of Z's Elements Is "+sum()+"\nThe Square Root Of That Sum Is "+Math.sqrt(sum());
		return label+columns+output;
	}
//}
}