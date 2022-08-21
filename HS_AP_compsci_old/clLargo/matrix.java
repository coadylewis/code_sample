import java.text.DecimalFormat;

public class matrix
{
	//SET THE NUMBER OF ROWS & COLUMNS GREATER THAN 0
	private final int ROWS=10;
	private final int COLUMNS=10;
	//SET THE UPPER BOUND OF NUMBERS IN THE MATRIX LESS THAN 1000
	private final int LIMIT=200;
	
	public matrix(){}
	
	DecimalFormat output = new DecimalFormat("000");
	
	int[][] brad = new int[ROWS][COLUMNS];
	
	private void generate()
	{
		for(int i=0;i<ROWS;i++)
		{
			for(int j=0;j<COLUMNS;j++)
				brad[i][j]=(int)(Math.random() * LIMIT + 1);
		}
	}
	
	public String toString()
	{
		generate();
		String largo="";
		for(int x=0;x<(COLUMNS*4+1);x++)
			largo=largo+"_";
		largo=largo+"\n|";
		for(int i=0;i<ROWS;i++)
		{
			for(int j=0;j<COLUMNS;j++)
				largo=largo+output.format(brad[i][j])+"|";
			largo=largo+"\n|";
			
			for(int x=0;x<(COLUMNS);x++)
				largo=largo+"___|";
			largo=largo+"\n|";
		}
		largo=largo.substring(0,largo.length()-1);
		largo=largo.replace("|00","|  ");
		largo=largo.replace("|0","| ");
		String analysis="";
		int rowmax=0;
		int colmax=0;
		int rowmin=0;
		int colmin=0;
		int maxValue=0;
		int minValue=LIMIT;
		for(int i=0;i<ROWS;i++)
    		for(int j=0;j<COLUMNS;j++)
    			if(brad[i][j]>maxValue)
    			{
    				maxValue = brad[i][j];
    				rowmax=i;
    				colmax=j;
    			}
    	for(int i=0;i<ROWS;i++)
    		for(int j=0;j<COLUMNS;j++)
    			if(brad[i][j]<minValue)
    			{
    				minValue = brad[i][j];
    				rowmin=i;
    				colmin=j;
    			}			
        int sum=0;
        for(int i=0;i<ROWS;i++)
		{
			for(int j=0;j<COLUMNS;j++)
				sum=sum+brad[i][j];
		}
        
		return largo+"\n\n"+"The Sum Of All Of The Numbers Is: "+sum+"\n\n"+
		"The Largest Number Is "+maxValue+
		" In Row: "+(rowmax+1)+", Column: "+(colmax+1)+"\n"+
		"The Smallest Number Is "+minValue+
		" In Row: "+(rowmin+1)+", Column: "+(colmin+1)+"\n";
	}
}