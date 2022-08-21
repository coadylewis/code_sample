import javax.swing.JOptionPane;

public class clpi
{
public static void main(String [] args)
{
	String inputStr = JOptionPane.showInputDialog("Enter the Number of Iterations", "0");
	if(inputStr == null)
		return;
	int n = Integer.parseInt(inputStr);
	
		double sum=1.0;
	
	if(n<0)
		JOptionPane.showMessageDialog(null,"Error: Number of Iterations must be >0");
	else
	{
		
				
				for(int i=2; i<=n; i++)
				{
					if(i%2 == 0)
					{
						sum= sum - (1.0/(2*i-1));
					}
					else
					{
						sum = sum + (1.0/(2*i-1));
					}	
				}
	}
	double pi=sum*4;
	JOptionPane.showMessageDialog(null, "Pi is " + pi);
	
	
}
}
