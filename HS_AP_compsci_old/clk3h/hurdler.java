package kareltherobot;
	
class hurdler extends ur_Robot
{
	public hurdler (int Street, int Avenue, Direction direction, int numberofBeepers)
	{
		super (Street, Avenue, direction, numberofBeepers);
	}
		
		
		
	public void turnRight()
	{
			turnLeft();
			turnLeft();
			turnLeft();
	}
		
	public void move3()
	{
		move();
		move();
		move();
	}
		
	public void celebrate()
	{
		turnLeft();
		turnLeft();
		turnLeft();
		turnLeft();
		turnLeft();
		turnLeft();
	}
}

