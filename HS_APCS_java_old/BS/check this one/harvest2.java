	package kareltherobot;
	
	
	class harvest2 extends Robot
	{
		public harvest2(int Street, int Avenue, Direction direction, int numberofBeepers)
		{
			super (Street, Avenue, direction, numberofBeepers);
		}
		
		
		
		public void move3()
		{
			for(int i=1; i<=3; i++)
			{
				move();
			}
		}
		
		public void turnRight()
		{
			for(int i=1; i<=3; i++)
			{
				turnLeft();
			}
		}
		
		public void reposRight()
		{
			move();
			turnLeft();
			move();
			turnLeft();
		}
		
		public void reposLeft()
		{
			move();
			turnRight();
			move();
			turnRight();
		}
		
		public void harvest()
		{
			move();
			replant();
			
			
		}
		
		public void harvest1r()
		{
			for(int i=1; i<=5; i++)
			{
				harvest();
			}
		}
		
		public void harvest2r()
		{
			harvest1r();
			reposRight();
			harvest1r();
			reposLeft();
		}
		
		public void replant()
		{
			for(int i=1;i<=2;i++)
				{
					if(nextToABeeper())
					{
						pickBeeper();
					}
				}
			
			putBeeper();
		}
	}
		