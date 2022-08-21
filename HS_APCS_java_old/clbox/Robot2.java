package kareltherobot;
//class Harvester extends Replanter


class Robot2 extends Robot
{
  public Robot2(int Street, int Avenue, Direction direction, int numberOfBeepers)
  {
    super(Street, Avenue, direction, numberOfBeepers);  
  }
  
  public void turnRight()
  {
    int i = 0;
    while(i<3)
    {
     turnLeft();
     i++; 
    }
    
    /*for(int i=0; i<3; i++)
    {
      turnLeft();
    }*/
    
    /*turnLeft();
    turnLeft();
    turnLeft();*/
     
  }
  
  public boolean rightIsClear()
  {
     turnRight();
     if (frontIsClear())
     {
        turnLeft();
        return true;
     }
     turnLeft();
     return false;  
  }
  
  public boolean leftIsClear()
  {
     turnLeft();
     if (frontIsClear())
     {
        turnRight();
        return true;
     }
     turnRight();
     return false;  
  }
    
}


