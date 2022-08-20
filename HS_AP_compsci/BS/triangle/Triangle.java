import TurtleGraphics.*;

public class Triangle
{
	private double x1,y1,x2,y2,x3,y3,distance1,distance2,distance3,side,shiftx,shifty;
	
	public Triangle(double X1,double Y1,double X2, double Y2,double X3,double Y3)
	{
		x1=X1;
		y1=Y1;
		x2=X2;
		y2=Y2;
		x3=X3;
		y3=Y3;
	}
	public Triangle()
	{
		x1=0;
		y1=0;
		x2=0;
		y2=0;
		x3=0;
		y3=0;
	}
	
	public void distance()
	{
		distance1 = Math.sqrt(((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)));
		distance2 = Math.sqrt(((x1-x3)*(x1-x3) + (y1-y3)*(y1-y3)));
		distance3 = Math.sqrt(((x2-x3)*(x2-x3) + (y2-y3)*(y2-y3)));
	}
	
	public double area()
	{
		return 0.5*Math.abs(x1*y2-x2*y1+x2*y3-x3*y2+x3*y1-x1*y3);
	}
	
	public void draw(Pen p)
	{
		p.up();
		p.move(x1, y1);
		p.down();
		p.move(x2, y2);
		p.move(x3, y3);
		p.move(x1, y1);
	}
	
	public void stretchBy(double factor)
	{
		x1=x1*factor;
		y1=y1*factor;
		x2=x2*factor;
		y2=y2*factor;
		x3=x3*factor;
		y3=y3*factor;
	}
	
	public void move(double xLoc, double yLoc)
	{
		shiftx=xLoc-x1;
		shifty=yLoc-y1;
		x1=xLoc;
		y1=yLoc;
		
		x2=x2+shiftx;
		y2=y2+shifty;
		x3=x3+shiftx;
		y3=y3+shifty;
	}
	
	public double getXPos()
	{
		return x1;
	}
	
	public double getYPos()
	{
		return y1;
	}
	
	public String toString()
	{
		return("side 1 = " + distance1 + "\nside 2 = " + distance2 + "\nside 3 = " + distance3 + 
		"\nposition1 = " + x1 + ", " + y1 + "\nposition2 = " + x2 + ", " + y2 + "\nposition3 = " + x3 + ", " + y3
		+ "\nArea = " + area() + "\n");
	}
	
	
}