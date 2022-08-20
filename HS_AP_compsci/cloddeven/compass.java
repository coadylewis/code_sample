package kareltherobot;


class compass extends Robot2
{
	public compass(int Street, int Avenue, Direction direction, int numberOfBeepers)
  {
    super(Street, Avenue, direction, numberOfBeepers);  
  }
  
  
  public void findSafeStack()
  {
  	while(nextToABeeper())
  	{
  		Search();
  	}
  }
  
  
  
  public void Search()
  {
  		if(nextToABeeper())
  		{
  			pickBeeper();
  		}
  		
  		if(nextToABeeper())
  		{
  			isItEven();
  		}
  		else
  		{
  			isItOdd();
  		}
  }
  
  
  
  public void isItEven()
  {
  	pickBeeper();
	if(!nextToABeeper())
  	{
  		turnRight();
  		move();
  		collectPile();;
  	}
  }
  
  
  
  public void isItOdd()
  {
  	if(!nextToABeeper())
  	{
  		turnLeft();
  		move();
  		collectPile();
  	}
  }
  
  
  
  public void collectPile()
  {
  	while(nextToABeeper())
  	{
  		pickBeeper();
  	}
  }
  
  	
  	
  	
  
  
}