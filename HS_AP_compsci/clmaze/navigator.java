package kareltherobot;


class navigator extends Robot2
{
	public navigator(int Street, int Avenue, Direction direction, int numberOfBeepers)
  {
    super(Street, Avenue, direction, numberOfBeepers);  
  }
  
  
  public void navigateMaze()
  {
  	while(!nextToABeeper())
  	{
  		navigate();
  		if(nextToABeeper())
  		{
  			return;
  		}
  	}
  }
  
  
  public void navigate()
  {
  	if(!rightIsClear())
  	{
  		if(frontIsClear())
  		{
  			move();
  		}
  		else
  		{
  			turnLeft();
  		}
  	}
  	goRight();
  	
  }
  	
  	
  public void goRight()
  {
  	if(rightIsClear())
  	{
  		turnRight();
  		move();
  	}
  }
  	
  	
  	
  
  
}