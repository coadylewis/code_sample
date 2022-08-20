package kareltherobot;


class sdsteeple extends ssteeple
{
	public sdsteeple(int Street, int Avenue, Direction direction, int numberOfBeepers)
  {
    super(Street, Avenue, direction, numberOfBeepers);  
  } 
  
  public void overhurdle()
  {
  	turnRight();
  	move();
  	
  	while(!rightIsClear())
  	{
  		move();
  	}
  	
  	turnRight();
  }
 }