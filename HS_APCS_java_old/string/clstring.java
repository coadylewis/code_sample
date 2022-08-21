import java.util.Scanner;

public class clstring
{
	public static void main(String[] args)
	{
			Scanner input = new Scanner(System.in);
			
			
			System.out.println("Enter A String Of Exactly Four Words.");
			String fourword = input.nextLine();
			String asfourword= fourword.replace(' ','*');
			System.out.println(asfourword);
			String lastword = asfourword.substring(0, asfourword.lastIndexOf('*')+1) + "#!!@1234";
			System.out.println(lastword);
			String remove1stword = lastword.substring(lastword.indexOf('*')+1,lastword.length());
			System.out.println(remove1stword);
			String remove2ndword = remove1stword.substring(remove1stword.indexOf('*')+1,remove1stword.length());
			System.out.println(remove2ndword);
			String remove3rdword = remove2ndword.substring(remove2ndword.indexOf('*')+1,remove2ndword.length());
			System.out.println(remove3rdword);
			String name = remove3rdword+"CoadyLewis";
			System.out.println(name);
			int length = name.length();
			String reverse = "";
			for( int i = length - 1 ; i >= 0 ; i-- ) 
			{
				reverse=reverse + name.charAt(i);
			}
			System.out.println(reverse);
			int finallength=reverse.length();
			System.out.println(finallength);
			
	
	
	
	}
}