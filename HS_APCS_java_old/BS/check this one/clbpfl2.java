package kareltherobot;



class clbpfl2 implements Directions
{	public static void main(String [] args)
	{	
		
		harvest2 karel = new harvest2(2, 3, East, 30);
		
		for(int i=1; i<=3; i++)
		{
			karel.harvest2r();
		}
		
		karel.turnOff();
		
		
		

	
	}

	static
	{	World.setDelay(5);
		World.setVisible(true);
		World.readWorld("D:/worlds/beep2.kwld");
	}
}