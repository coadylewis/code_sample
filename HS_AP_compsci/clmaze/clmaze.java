package kareltherobot;
 
class clmaze implements Directions
{	public static void main(String [] args)
	{	
		
		navigator photoshopbrian = new navigator(13, 13, East, 0);
		
		
		photoshopbrian.navigateMaze();
		photoshopbrian.turnOff();
		
		
			
	}
	
		static
	{
		World.setVisible(true);
		World.readWorld("D:/worlds/maze1.kwld");
		World.setDelay(2);
		
		
	}
}	