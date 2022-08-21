package kareltherobot; // Essential, I think. Not everything is public

import java.awt.*;
import java.applet.*;
import java.awt.event.*;
import java.util.*;
//import kareltherobot.*;
import kareltherobot.Directions;
import kareltherobot.World;
import kareltherobot.WorldBuilderInterface;
import kareltherobot.MiniBuilder;
import kareltherobot.ur_Robot;
import kareltherobot.Robot;
import kareltherobot.WorldBuilder;


public class KarelApplet extends Applet implements  Directions // Directions OR RobotTester is essential.
{	
	public void init()
	{	setSize(400, 400);
		add(worldCommands); // Just a flow layout. Could change, of course. 
		//add(canvas); // Use this for canvas in the same frame. 
		add(showWorld); //Use this for a separate frame.
		add(tasker);
		add(wantBuilder);
		add(fromText);
		add(reset);
		add(toText);
		add(speed);
		
		tasker.addActionListener 
		(	new ActionListener ()	
			{	public void actionPerformed(ActionEvent e)
				{	new Thread() // This thread is essential or the world won't update in an applet
					{	public void run()
						{ task();
						}	
					}.start();
				}
			}
		); // Wow -- double nested anonymous inner class. 
		
		wantBuilder.addActionListener
		(	new ActionListener()
			{	public void actionPerformed(ActionEvent e)
				{	if (builder == null) 
					{	builder = new MiniBuilder(true);
					}
					else ((MiniBuilder)builder).setVisible(true);
				}
			}
		); 
		
		fromText.addActionListener
		(	new ActionListener()
			{	public void actionPerformed(ActionEvent e)
				{	World.getWorld(worldCommands.getText()); //String -> World
					World.repaint();	
				}
			}
		);

		reset.addActionListener
		(	new ActionListener()
			{	public void actionPerformed(ActionEvent e)
				{	World.reset();
					World.repaint();	
				}
			}
		);
		
		toText.addActionListener
		(	new ActionListener()
			{	public void actionPerformed(ActionEvent e)
				{	String text = World.asText("\n"); // World -> String
					worldCommands.append(text);	
				}
			}
		);
		
		speed.addActionListener
		(	new ActionListener()
			{	public void actionPerformed(ActionEvent e)
				{	World.showSpeedControl(true);
				}
			}
		);
		
		showWorld.addActionListener
		(	new ActionListener()
			{	public void actionPerformed(ActionEvent e)
				{	World.setVisible(true);
					//World.showSpeedControl(true);	
				}
			}
		);

		World.replaceCloser(null);
		setVisible(true);
				
	}
	
	private Button tasker = new Button ("Perform Task");
	private TextArea worldCommands = new TextArea(20, 40); // A bit smaller is ok too.
	private Canvas canvas = World.worldCanvas(); // force the World class to load.
	private Button wantBuilder = new Button("World Builder");
	private WorldBuilderInterface builder = null;
	private Button reset = new Button("Clear World");
	private Button showWorld = new Button("Show World");
	private Button fromText = new Button("Text -> World");
	private Button toText = new Button("World -> Text");
	private Button speed = new Button ("Show Speed Control");
	
/// Everything above is scaffolding
/// Everything below is what the user writes and includes

/// The class is needed but doesn't need to be inner to the applet. 
/// Being able to write classes is essential to the concept

	class RightTurner extends ur_Robot
	{	public RightTurner(int street, int avenue, Direction dir, int beepers)
		{	super(street, avenue, dir, beepers);
		}
			
		public void turnRight()
		{	turnLeft();
			turnLeft();
			turnLeft();
		}
	}

	public void task() // Naming this "task" isn't essential, though desirable if visible.
	{	//World.showSpeedControl(true);	
		RightTurner karel = new RightTurner(3, 3, East, infinity);
				
		karel.turnRight();
		karel.move();
		karel.turnRight();
		karel.move();
		karel.turnRight();
		karel.move();
		karel.turnOff();	
	}

}


