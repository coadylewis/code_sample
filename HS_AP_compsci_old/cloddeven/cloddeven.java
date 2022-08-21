package kareltherobot;
 
class cloddeven implements Directions
{	public static void main(String [] args)
	{	
		
		compass SYIsAMeme = new compass(5, 5, North, 0);
		
		
		SYIsAMeme.findSafeStack();
		SYIsAMeme.turnOff();
		
		
			
	}
	
		static
	{
		World.setVisible(true);
		World.readWorld("D:/worlds/oe1.kwld");
		World.setDelay(5);
		
		
	}
}	