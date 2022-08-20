package kareltherobot;


class steeple extends Robot2
{
	public steeple(int Street, int Avenue, Direction direction, int numberOfBeepers)
  {
    super(Street, Avenue, direction, numberOfBeepers);  
  }
  
  
  
  public void uphurdle()
  {
  	for(int i=1; i<=3; i++)
  	{
  		if(!rightIsClear())
  		move();
  	}
  }
  
  
  public void overhurdle()
  {
  	turnRight();
  	move();
  	turnRight();
  }
  
  
  public void downhurdle()
  {
  	for(int i=1; i<=3; i++)
  	{
  		if(frontIsClear())
  		move();
  	}
  }
  
  
  public void clearhurdle()
  {
  	turnLeft();
  	uphurdle();
  	overhurdle();
  	downhurdle();
  	turnLeft();
  }
  
  

}
