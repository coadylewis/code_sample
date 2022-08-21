package kareltherobot;


class bfinder extends Robot2
{
	public bfinder(int Street, int Avenue, Direction direction, int numberOfBeepers)
  {
    super(Street, Avenue, direction, numberOfBeepers);  
  }
  
  
  	
  	public void findbeeper()
  	{
  		findcorner();
  		
  		if(!nextToABeeper())
  		{
  			filter();
  		}
  		
  		if(nextToABeeper())
  		{
  			pickBeeper();
  		}
  	}
  	
  	
  	
  	public void findcorner()
  	{
  		while(frontIsClear())
  		{
  			move();
  		}
  		
  		while(!frontIsClear())
  		{
  			turnRight();
  		}
  		
  		while(frontIsClear())
  		{
  			move();
  		}
  		
  		while(!frontIsClear())
  		{
  			turnRight();
  		}
  	}
  	
  	
  	
  	public void filter()
  	{
  		while(!anyBeepersInBeeperBag())
  			{	
  				
  				while(frontIsClear())
  					{
  						if(!nextToABeeper())
  						{
  							move();
  						}
  						if(nextToABeeper())
  						{
  							pickBeeper();
  						}
  						
  					}
  				
  				if(!nextToABeeper())
  					{
  						turnRight();
  						if(frontIsClear())
  						{
  							move();
  						}
  						turnRight();
  					}
  					
  				if(nextToABeeper())
  					{
  						pickBeeper();
  					}
  				
  				while(frontIsClear())
  					{
  						if(!nextToABeeper())
  						{
  							move();
  						}
  						if(nextToABeeper())
  						{
  							pickBeeper();
  						}
  						
  					}
  					
  				if(!nextToABeeper())
  					{
  						turnLeft();
  						if(frontIsClear())
  						{
  							move();
  						}
  						turnLeft();	
  					}
  					
  				if(nextToABeeper())
  					{
  						pickBeeper();
  					}	
  			}
  	}
  
  
}