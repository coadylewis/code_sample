public class clFraction
{
	public static void main(String[] args)
	{
		Fraction fourSevenths = new Fraction(4, 7);
		Fraction oneHalf = new Fraction (1, 2);
		Fraction oneThird = new Fraction (1, 3);
		Fraction oneFourth = new Fraction (1, 4);
		Fraction twoThird = new Fraction (2, 3);
		
		Fraction test = oneThird.add(oneFourth);
		
		System.out.println(oneHalf.sub(twoThird));
		System.out.println(oneFourth.mul(oneHalf));
		System.out.println(oneThird.div(oneThird));
		System.out.println(fourSevenths.add(oneFourth));
		System.out.println((test));
		
		Fraction brian = new Fraction();
		
		brian.setNumerator(2);
		brian.setDenominator(9);
		
		System.out.println(brian.numerator());
		System.out.println(brian.denominator());
		
		System.out.println(brian);
		
	}
}