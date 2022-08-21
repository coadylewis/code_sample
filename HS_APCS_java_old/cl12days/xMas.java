class xMas
{
	public xMas()
  {
    super();  
  }
  
  public void firstDay()
  {
  	System.out.println("	A Partridge In A Pear Tree");
  	System.out.println("");
  }
  
  public void secondDay()
  {
  	System.out.println("	2 Turtle Doves");
  	System.out.println("	And A Partridge In A Pear Tree");
  	System.out.println("");
  }
  
  public void thirdDay()
  {
  	System.out.println("	3 French Hens");
  	secondDay();
  }
  
  public void fourthDay()
  {
  	System.out.println("	4 Calling Birds");
  	thirdDay();
  }
  
  public void fifthDay()
  {
  	System.out.println("	5 Golden Rings");
  	fourthDay();
  }
  
  public void sixthDay()
  {
  	System.out.println("	6 Geese A Laying");
  	fifthDay();
  }
  
  public void seventhDay()
  {
  	System.out.println("	7 Swans A Swimming");
  	sixthDay();
  }
  
  public void eighthDay()
  {
  	System.out.println("	8 Maids A Milking");
  	seventhDay();
  }
  
  public void ninthDay()
  {
  	System.out.println("	9 Ladies Dancing");
  	eighthDay();
  }
  
  public void tenthDay()
  {
  	System.out.println("	10 Lords A Leaping");
  	ninthDay();
  }
  
  public void eleventhDay()
  {
  	System.out.println("	11 Pipers Piping");
  	tenthDay();
  }
  
  public void twelfthDay()
  {
  	System.out.println("	12 Drummers Drumming");
  	eleventhDay();
  }
  
  public void outro()
  {
  	System.out.println("On The 26th Day of September, Mr. Compton Gave To Me");
  	System.out.println("	A 100 On The Calculus BC Test");
  	intro();
  }
  
  public void intro()
  {
  	System.out.println("");
  	System.out.println("");
  }
}