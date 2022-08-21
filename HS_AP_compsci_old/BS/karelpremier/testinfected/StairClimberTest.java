package kareltherobot;

public class StairClimberTest extends KJRTest implements Directions
{

    public StairClimberTest(String name)
    {   super(name);
    }

	private StairClimber karel;

	public void setUp()
	{   World.reset();
		World.readWorld("stairworld.kwld");
		World.setVisible(true);
		karel = new StairClimber(1, 1, East, 0);
	}

	public void testRightTurn()
	{   assertFacingEast(karel);
		assertRunning(karel);
		karel.turnRight();
		assertFacingSouth(karel);
		assertRunning(karel);
		karel.turnRight();
		assertFacingWest(karel);
		assertRunning(karel);
		karel.turnRight();
		assertFacingNorth(karel);
		assertRunning(karel);
		karel.turnRight();
		assertFacingEast(karel);
		assertRunning(karel);
	}

	public void testClimbOneStair()
	{   assertFacingEast(karel);
		assertRunning(karel);
		assertFrontIsBlocked(karel);
		assertAt(karel, 1, 1);
		karel.climbOneStair();
		assertFacingEast(karel);
		assertRunning(karel);
		assertAt(karel, 2, 2);
	}

	public void testClimbStairs()
	{   //World.readWorld("stairworld.kwld");
		assertFacingEast(karel);
		assertRunning(karel);
		assertFrontIsBlocked(karel);
		karel.climbStairs();
		assertNextToABeeper(karel);
		assertRunning(karel);
	}

	public void testGetBeeper()
	{	assertFacingEast(karel);
		assertRunning(karel);
		assertFrontIsBlocked(karel);
		assertNoBeepersInBeeperBag(karel);
		karel.getBeeper();
		assertNotRunning(karel);
		assertBeepersInBeeperBag(karel);
		assertNotNextToABeeper(karel);
	}

    public static void main(String[] args)
    {
        junit.swingui.TestRunner.run(StairClimberTest.class);
    }
}