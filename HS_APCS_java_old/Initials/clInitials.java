import TurtleGraphics.*;

public class clInitials
{
	public static void main(String[] args)
	{
		SketchPadWindow butt = new SketchPadWindow(600,400);
		Pen turtle = new StandardPen(butt);
		
		turtle.home();
		turtle.up();
		turtle.turn(90);
		turtle.move(110);
		turtle.turn(-90);
		turtle.move(145);
		turtle.turn(45);
		turtle.down();
		turtle.move(20*Math.sqrt(2));
		turtle.turn(45);
		turtle.move(130);
		turtle.turn(45);
		turtle.move(20*Math.sqrt(2));
		turtle.turn(45);
		turtle.move(290);
		turtle.turn(45);
		turtle.move(20*Math.sqrt(2));
		turtle.turn(45);
		turtle.move(130);
		turtle.turn(45);
		turtle.move(20*Math.sqrt(2));
		turtle.up();
		turtle.home();
		turtle.turn(90);
		turtle.move(90);
		turtle.turn(-90);
		turtle.move(165);
		turtle.turn(180);
		turtle.down();
		turtle.move(330);
		turtle.turn(180);
		turtle.move(165);
		turtle.turn((-1)*Math.toDegrees(Math.atan(180.0/165)));
		turtle.move(Math.sqrt(165*165+180*180));
		turtle.turn(180);
		turtle.move(Math.sqrt(165*165+180*180));
		turtle.turn((2)*Math.toDegrees(Math.atan(180.0/165)));
		turtle.move(Math.sqrt(165*165+180*180));
		turtle.up();
		turtle.home();
		turtle.turn(-90);
		turtle.move(110);
		turtle.turn(90);
		turtle.move(165);
		turtle.turn(180);
		turtle.down();
		turtle.move(330);
		turtle.turn(90);
		turtle.move(170);
		turtle.up();
		turtle.home();
	}
}