package kareltherobot;
 
class clbox implements Directions
{	public static void main(String [] args)
	{	
		
		bfinder RIPbrian = new bfinder(5, 5, West, 0);
		
		
		RIPbrian.findbeeper();
		
		RIPbrian.turnOff();
		
		
		
		
		
		
		
	}
	
		static
	{
		World.setVisible(true);
		World.readWorld("D:/worlds/bb1.kwld");
		World.setDelay(3);
	}
}	