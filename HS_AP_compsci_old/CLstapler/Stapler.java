/** @student.info
 *<BR> Name:
 *<BR> Date:				
 *<BR> Period:				
 *<BR> Description:			 Stapler Driver
 */

public class Stapler
{


	//********Instance Variables********


	//DO NOT ADD, DO NOT CHANGE
	private int myStaples;		//how many staples in stapler
	private int myCapacity;		//how many staples it can hold
	private boolean myClosed;	//is stapler closed?


	//********Constructors********


	//Default constructor.
	//Set to: zero staples, capacity 250, closed.
	public Stapler()
	{
		myStaples=0;
		myCapacity=250;
		myClosed=true;
	}

	//Regular constructor.  Initialize instance variables with
	//provided values.  Assume user will use valid values for all.
	public Stapler(int staples, int capacity, boolean closed)
	{
		myStaples=staples;
		myCapacity=capacity;
		myClosed=closed;
	}

	//Copy constructor.  Initializes stapler with values provided
	//from another stapler.  Assume "temp" stapler has valid values.
	public Stapler(Stapler temp)
	{
		myStaples=temp.myStaples;
		myCapacity=temp.myCapacity;
		myClosed=temp.myClosed;
	}


	//********Mutator Methods (change values) ********


	//Close the stapler
	public void closeStapler()
	{
		myClosed=true;
	}

	//Open the stapler
	public void openStapler()
	{
		myClosed=false;
	}

	//Subtract a single staple.  The stapler can
	//staple only when already closed AND when it HAS STAPLES.
	//**Both** conditions **must** be true to staple.
	//HINT:  Requires one or more IF statements.
	public void staple()
	{
		if((myClosed==true)&&(myStaples>=1))
		{
			myStaples--;
		}
	}

	//Increase staples up to the maximum capacity.
	//The stapler must already be OPEN to add staples.
	//HINT: Requires IF statement(s) to make sure stapler is already open
	//and to make sure you fill it up to, BUT NOT BEYOND capacity.
	public void addStaples(int moreStaples)
	{
		if(myClosed==false)
		{
			for(int i=0;i<moreStaples;i++)
			{
				if(myStaples<myCapacity)
				{
					myStaples++;
				}
			}
		}
	}


	//********Accessor Methods (return values) ********

	//returns number of staples
	public int numStaples()
	{
		return myStaples;
	}

	//returns capacity of stapler
	public int getCapacity()
	{
		return myCapacity;
	}

	//returns open/closed status of stapler
	public boolean isClosed()
	{
		return myClosed;
	}
}