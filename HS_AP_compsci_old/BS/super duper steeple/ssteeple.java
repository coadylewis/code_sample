package kareltherobot;


class ssteeple extends steeple
{
	public ssteeple(int Street, int Avenue, Direction direction, int numberOfBeepers)
  {
    super(Street, Avenue, direction, numberOfBeepers);  
  } 
    
    
    public void uphurdle()
    {
    	while(!rightIsClear())
    		move();
    }
    
    
    
    public void downhurdle()
    {
    	while(frontIsClear())
    		move();
    }
  }