package kareltherobot;

public class Test2	implements  RobotTester
{
	public void task() 
	{
		ur_Robot karel = new ur_Robot(3, 3, East, infinity);
		
		karel.turnLeft();
		karel.move();
		karel.turnLeft();
		karel.move();
		karel.turnLeft();
		karel.move();
		karel.turnOff();	
	}

}
