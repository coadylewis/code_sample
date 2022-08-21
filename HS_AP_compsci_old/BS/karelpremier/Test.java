package kareltherobot;

class Test	implements  RobotTester
{
	public void task() 
	{
		World.readWorld("test.kwld");
		ur_Robot karel = new ur_Robot(1, 1, East, 0);
		
		karel.move();
		karel.move();
		karel.move();
		karel.turnLeft();
		karel.move();
		karel.move();
		karel.pickBeeper();
		karel.turnLeft();
		karel.move();
		karel.turnLeft();
		karel.move();
		karel.turnLeft();
		karel.move();
		karel.turnOff();	
	}

}

