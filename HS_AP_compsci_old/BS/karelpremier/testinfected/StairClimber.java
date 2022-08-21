package kareltherobot;

public class StairClimber extends ur_Robot
{
    public StairClimber(int street, int avenue, Direction d, int beepers)
    {   super(street, avenue, d, beepers);
    }

	public void turnRight()
	{   //move();
		turnLeft();
		//move();
		turnLeft();
		//move();
		turnLeft();
		//move();
	}

	public void climbOneStair()
	{   turnLeft();
		move();
		turnRight();
		move();
	}

	public void climbStairs()
	{   climbOneStair();
		climbOneStair();
		climbOneStair();
	}

	public void getBeeper()
	{
		climbStairs();
		pickBeeper();
		turnOff();
	}

	public static void task()
	{   World.reset();
		World.readWorld("stairworld.kwld");
		World.setVisible(true);
		StairClimber karel = new StairClimber(1, 1, East, 0);
		karel.getBeeper();
	}

	public static void main(String [] args)
	{
		task();
	}
}