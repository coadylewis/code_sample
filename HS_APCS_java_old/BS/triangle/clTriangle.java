import TurtleGraphics.*;
import java.util.Scanner;
import java.awt.Color;

public class clTriangle
{
	public static void main(String[] args)
	{
		SketchPadWindow win = new SketchPadWindow(600, 400);
		
		Scanner input = new Scanner(System.in);
		
		Pen pen;
		pen = new StandardPen(win);
		double x1,y1,x2,y2,x3,y3;
	
	System.out.println("Enter The X Coordinate Of The First Vertex");
	x1=input.nextDouble();
	System.out.println("Enter The Y Coordinate Of The First Vertex");
	y1=input.nextDouble();
	System.out.println("Enter The X Coordinate Of The Second Vertex");
	x2=input.nextDouble();
	System.out.println("Enter The Y Coordinate Of The Second Vertex");
	y2=input.nextDouble();
	System.out.println("Enter The X Coordinate Of The Third Vertex");
	x3=input.nextDouble();
	System.out.println("Enter The Y Coordinate Of The Third Vertex");
	y3=input.nextDouble();
	
		Triangle tri = new Triangle(x1,y1,x2,y2,x3,y3);
		
		tri.draw(pen);
		tri.distance();
		System.out.println(tri);
		
		System.out.println("Press <Enter> to Continue");
		input.nextLine();
		input.nextLine();
		pen.setColor(Color.white);
		tri.draw(pen);
		pen.setColor(Color.red);
		
		tri.stretchBy(2);
		tri.draw(pen);
		tri.distance();
		System.out.println(tri);
		
		System.out.println("Press <Enter> to Continue");
		input.nextLine();
		pen.setColor(Color.white);
		tri.draw(pen);
		pen.setColor(Color.green);
		
		tri.move(50,50);
		tri.draw(pen);
		tri.distance();
		System.out.println(tri);
	}
}
		
		
	