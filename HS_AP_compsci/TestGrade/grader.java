public class grader
{
	
	private double Test1, Test2, Test3;
	
	public grader(double T1, double T2, double T3)
	{
		Test1=T1;
		Test2=T2;
		Test3=T3;
	}
	public grader()
	{
		Test1=0;
		Test2=0;
		Test3=0;
	}
	
	public double oneOrTwo()
	{
		if(Test1>Test2)
		{
			return Test1;
		}
		else
		{
			return Test2;
		}
	}
	
	public double totalGrade()
	{
		return oneOrTwo() + Test3;
	}
	
	public String letterGrade()
	{
		String grade = "grade";
		
		if(totalGrade()>=90)
		{
			grade = "A";
		}
		if(totalGrade()>=80&&totalGrade()<90)
		{
			grade = "B";
		}
		if(totalGrade()>=70&&totalGrade()<80)
		{
			grade = "C";
		}
		if(totalGrade()>=60&&totalGrade()<70)
		{
			grade = "D";
		}
		if(totalGrade()<60)
		{
			grade = "F";
		}
		return grade;
	}
	
	public String toString()
	{
		String GradeAn = "Your Grade is an " + letterGrade();
		String GradeA = "Your Grade is a " + letterGrade();
		String Encouragement = "Congratulations, ";
		String Discouragement = "You've taken a MASSIVE L, ";
		if(letterGrade().equals("A")||letterGrade().equals("F"))
		{
			if(letterGrade().equals("A"))
			{
				return Encouragement + GradeAn;
			}
			else
			{
				return Discouragement + GradeAn;
			}
		}
		else
		{
			return GradeA;
		}
		
	}
}