public class Fraction
{	
	
	private int num, den;
	
	public Fraction(int n, int d)
	{
		num = n;
		den = d;
	}
	public Fraction()
	{
		num = 0;
		den = 1;
	}
	
	
	public int numerator()
	{
		return num;
	}
	
	public int denominator()
	{
		return den;
	}
	
	public void setNumerator(int n)
	{
		num = n;
	}
	
	public void setDenominator(int d)
	{
		den = d;
	}
	
	public Fraction add(Fraction other)
	{
		int n = num * other.den + other.num * den;
		int d = den * other.den;
		return new Fraction (n, d);
	}
	
	public Fraction sub(Fraction other)
	{
		int n = num * other.den - other.num * den;
		int d = den * other.den;
		return new Fraction (n, d);
	}
	
	public Fraction mul(Fraction other)
	{
		int n = num * other.num;
		int d = den * other.den;
		return new Fraction (n, d);
	}
	
	public Fraction div(Fraction other)
	{
		int n = num * other.den;
		int d = den * other.num;
		return new Fraction (n, d);
	}
	
	public String toString()
	{
		return num + "/" + den;
	}
}	