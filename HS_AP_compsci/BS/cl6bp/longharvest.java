	package kareltherobot;
	
	class longharvest extends harvest
	{
		public longharvest(int Street, int Avenue, Direction direction, int numberofBeepers)
		{
			super (Street, Avenue, direction, numberofBeepers);
		}
		
		
		public void harvest1r()
		{
			super.harvest1r();
			harvest();
		}
	}