package kareltherobot;

import junit.framework.*;

public class UnitTest extends KJRTest
{
	public UnitTest(String name)
	{ super(name);
	}

	private ur_Robot karel;

	public void setUp()
	{   World.reset();
		World.setVisible(true);
		karel = new ur_Robot(1, 1, North, 1);
	}

	public void testActions()
	{   assertFrontIsClear(karel);
		karel.move();
		karel.turnLeft();
		assertFrontIsBlocked(karel);
		assertOnStreet(karel, 2);
		assertOnAvenue(karel, 1);
		assertHasNoNeighbor(karel);
		assertFacingWest(karel);
		assertNotAt(karel, 1, 1);
		assertBeepersInBeeperBag(karel);
		assertNotNextToABeeper(karel);
		karel.putBeeper();
		assertNoBeepersInBeeperBag(karel);
		assertNextToABeeper(karel);
	}

	public void testTurnoff()
	{	assertRunning(karel);
		karel.turnOff();
		assertNotRunning(karel);
	}

	public void testErrorTurnoff()
	{	assertRunning(karel);
		assertFrontIsClear(karel);
		karel.turnLeft();
		assertFrontIsBlocked(karel);
		karel.move();
		assertNotRunning(karel);
	}

    public static void main(String[] args)
    {   junit.swingui.TestRunner.run(UnitTest.class);
    }
}