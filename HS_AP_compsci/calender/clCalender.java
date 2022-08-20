import java.util.Scanner;

public class clCalender
{
	public static void main(String[] args)
	{
			Scanner input = new Scanner(System.in);
			int days,first;
			System.out.println("Enter The Number Of Days");
				days=input.nextInt();
			System.out.println("Enter The Date Of The First Sunday");
				first=input.nextInt();
				
			calender brad = new calender(days,first);
			System.out.println(brad);		
	}
}