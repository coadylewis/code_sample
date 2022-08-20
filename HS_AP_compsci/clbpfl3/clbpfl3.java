package kareltherobot;


class clbpfl3 implements Directions
{	public static void main(String [] args)
	{	
		
		harvest karel = new harvest(2, 3, East, 0);
		harvest brian = new harvest(4, 3, East, 0);
		harvest tarquine = new harvest(6, 3, East, 0);
		
		
		
			karel.harvest2r();
			karel.turnOff();
		
		
		
			brian.harvest2r();
			brian.turnOff();
			
		
		
			tarquine.harvest2r();
			tarquine.turnOff();
		
		
			
			
		
			
		
			
			
			
		
			
			
			
		
		
		

	
	}

	static
	{	World.setDelay(15);
		World.setVisible(true);
		World.readWorld("D:/worlds/beepfld.kwld");
	}
}