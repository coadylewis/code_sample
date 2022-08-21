package kareltherobot;
 
class clsstp implements Directions
{	public static void main(String [] args)
	{	
		
		ssteeple karel = new ssteeple(1, 1, East, 0);
		
		
		while(!karel.nextToABeeper())
		{
			if(karel.frontIsClear())
			karel.move();
			else
			karel.clearhurdle();
		}
		
		karel.pickBeeper();
		karel.turnOff();
	}
	
		static
	{	World.setVisible(true);
		World.readWorld("D:/worlds/ss1.kwld");
		World.setDelay(5);
	}
}		