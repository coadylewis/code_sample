public class FrameArt
{
	private int Length, Width;
	
	public final double GLASS=0.02, WOOD=1.45;
	
	public FrameArt(int L, int W)

	{
		Length=L;
		Width=W;
	}
	
	
	public double Area()
	{
		return Length*Width;
	}
	
	public double GlassPrice()
	{
		return Area() *GLASS;
	}
	
	public double Perimeter()
	{
		return (2*Length) + (2*Width);
	}
	
	public double WoodPrice()
	{
		return Perimeter() / 12 *WOOD;
	}
	
	public double TotalPrice()
	{
		return GlassPrice() + WoodPrice();
	}
}