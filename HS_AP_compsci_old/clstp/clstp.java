package kareltherobot;
 
class clstp implements Directions
{	public static void main(String [] args)
	{	
		
		steeple karel = new steeple(1, 1, East, 0);
		
		
		for(int i=1; i<=8; i++)
		{
			if(frontIsClear())
			karel.move();
			else
			karel.clearhurdle();
		}
		
		karel.turnOff();
	}
	
		static
	{	World.setVisible(true);
		World.readWorld("D:/worlds.sc1.kwld");
		World.setDelay(15);
	}
}		