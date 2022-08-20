package kareltherobot;


class homefinder extends Robot2
{
	public homefinder(int Street, int Avenue, Direction direction, int numberOfBeepers)
  {
    super(Street, Avenue, direction, numberOfBeepers);  
  }
  
  
  	public void turnAround()
  	{
  		for(int i=0;i<2;i++)
  		{
  			turnLeft();
  		}
  	}
  	
  	
  	public void checkForBeeper()
  	{
  		move();
  		if(nextToABeeper())
  		{
  			pickBeeper();
  			
  		}
  		else
  		{
  			turnAround();
  			move();
  			turnAround();
  			checkLeft();
  		}
  	}
  	
  	
  	public void checkLeft()
  	{
  		turnLeft();
  		move();
  		if(nextToABeeper())
  		{
  			pickBeeper();
  			
  		}
  		else
  		{
  			turnAround();
  			move();
  			turnLeft();
  			pickRight();
  		}
  	}
  	
  	
  	public void pickRight()
  	{
  		turnRight();
  		move();
  		pickBeeper();
  	}
  	
  	
  	
  	
  	
  	public void findHome()
  	{
  		while(frontIsClear())
  		{
  			checkForBeeper();
  			if(nextToABeeper())
  			{
  				return;
  			}
  			
  			
  			
  		}
  	}
  	
  	
  	
  	
  
  
}