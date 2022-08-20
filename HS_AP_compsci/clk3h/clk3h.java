package kareltherobot;

class clk3h implements Directions
{	public static void main(String [] args)
	{	
		
		hurdler karel = new hurdler(1, 1, East, 0);
		
		karel.move();
		karel.move3();
		karel.turnLeft();
		karel.move3();
		karel.turnRight();
		karel.move();
		karel.turnRight();
		karel.move3();
		karel.turnLeft();
		karel.move3();
		karel.turnLeft();
		karel.move3();
		karel.turnRight();
		karel.move();
		karel.turnRight();
		karel.move3();
		karel.turnLeft();
		karel.move3();
		karel.turnLeft();
		karel.move3();
		karel.turnRight();
		karel.move();
		karel.turnRight();
		karel.move3();
		karel.turnLeft();
		karel.move3();
		karel.celebrate();
		karel.turnOff();
		
		

	
	}

	static
	{	World.setDelay(15);
		World.setVisible(true);
		World.readWorld("D:/worlds/k3h.kwld");
	}
}