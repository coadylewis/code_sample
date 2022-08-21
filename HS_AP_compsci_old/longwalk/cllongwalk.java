package kareltherobot;
 
class cllongwalk implements Directions
{	public static void main(String [] args)
	{	
		
		homefinder RIPbrian = new homefinder(2, 3, North, 0);
		
		
		RIPbrian.findHome();
		RIPbrian.turnOff();
		
		
			
	}
	
		static
	{
		World.setVisible(true);
		World.readWorld("D:/worlds/lw2.kwld");
		World.setDelay(2);
	}
}	