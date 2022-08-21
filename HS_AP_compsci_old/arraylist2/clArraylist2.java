import java.util.Scanner;

public class clArraylist2
{
	public static void main(String[] args)
	{
			Scanner input = new Scanner(System.in);
			int choice=0;
			int number=0;
			while(choice!=9)
			{
				System.out.println("1) Generate New Arraylist\n2) Search The Base Arraylist\n3) Sort The Base Arraylist\n4) Reverse-Sort The Base Arraylist\n5) Find The Largest Number In The Base Arraylist\n6) Find The Smallest Number In The Base Arraylist\n7) Copy The Base Arraylist\n8) Display The Sum Of The Base Arraylist");
				System.out.println("Enter Your Choice, To Exit The Program Enter 9");
					choice=input.nextInt();
				if(choice==2)
				{
					System.out.println("Enter The Number To Search For");
					number=input.nextInt();
				}
				arraylist2 brad=new arraylist2(number,choice);
				System.out.println(brad);
			}
	}
}