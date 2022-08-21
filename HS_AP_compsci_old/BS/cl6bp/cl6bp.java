package kareltherobot;


class cl6bp implements Directions
{	public static void main(String [] args)
	{	
		
		longharvest karel = new longharvest(2, 3, East, 0);
		
		for(int i=1; i<=3; i++)
		{
			karel.harvest2r();
		}
		
		karel.turnOff();
		
		
		

	
	}

	static
	{	World.setDelay(15);
		World.setVisible(true);
		World.readWorld("D:/worlds/beepfld2.kwld");
	}
}