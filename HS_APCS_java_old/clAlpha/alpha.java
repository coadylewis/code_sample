public class alpha
{
	private String enter="";
	private int a,b,c,d,e,f,g,h,it,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z;
	public alpha(String s)
	{
		enter=s;
	}
	
	public void search()
	{
		for(int i=0;i<enter.length();i++)
		{
			if((enter.substring(i,(i+1)).equals("A"))||(enter.substring(i,(i+1)).equals("a")))
				a++;
			if((enter.substring(i,(i+1)).equals("B"))||(enter.substring(i,(i+1)).equals("b")))
				b++;
			if((enter.substring(i,(i+1)).equals("C"))||(enter.substring(i,(i+1)).equals("c")))
				c++;
			if((enter.substring(i,(i+1)).equals("D"))||(enter.substring(i,(i+1)).equals("d")))
				d++;
			if((enter.substring(i,(i+1)).equals("E"))||(enter.substring(i,(i+1)).equals("e")))
				e++;
			if((enter.substring(i,(i+1)).equals("F"))||(enter.substring(i,(i+1)).equals("f")))
				f++;
			if((enter.substring(i,(i+1)).equals("G"))||(enter.substring(i,(i+1)).equals("g")))
				g++;
			if((enter.substring(i,(i+1)).equals("H"))||(enter.substring(i,(i+1)).equals("h")))
				h++;
			if((enter.substring(i,(i+1)).equals("I"))||(enter.substring(i,(i+1)).equals("i")))
				it++;
			if((enter.substring(i,(i+1)).equals("J"))||(enter.substring(i,(i+1)).equals("j")))
				j++;
			if((enter.substring(i,(i+1)).equals("K"))||(enter.substring(i,(i+1)).equals("k")))
				k++;
			if((enter.substring(i,(i+1)).equals("L"))||(enter.substring(i,(i+1)).equals("l")))
				l++;
			if((enter.substring(i,(i+1)).equals("M"))||(enter.substring(i,(i+1)).equals("m")))
				m++;
			if((enter.substring(i,(i+1)).equals("N"))||(enter.substring(i,(i+1)).equals("n")))
				n++;
			if((enter.substring(i,(i+1)).equals("O"))||(enter.substring(i,(i+1)).equals("o")))
				o++;
			if((enter.substring(i,(i+1)).equals("P"))||(enter.substring(i,(i+1)).equals("p")))
				p++;
			if((enter.substring(i,(i+1)).equals("Q"))||(enter.substring(i,(i+1)).equals("q")))
				q++;
			if((enter.substring(i,(i+1)).equals("R"))||(enter.substring(i,(i+1)).equals("r")))
				r++;
			if((enter.substring(i,(i+1)).equals("S"))||(enter.substring(i,(i+1)).equals("s")))
				s++;
			if((enter.substring(i,(i+1)).equals("T"))||(enter.substring(i,(i+1)).equals("t")))
				t++;
			if((enter.substring(i,(i+1)).equals("U"))||(enter.substring(i,(i+1)).equals("u")))
				u++;
			if((enter.substring(i,(i+1)).equals("V"))||(enter.substring(i,(i+1)).equals("v")))
				v++;
			if((enter.substring(i,(i+1)).equals("W"))||(enter.substring(i,(i+1)).equals("w")))
				w++;
			if((enter.substring(i,(i+1)).equals("X"))||(enter.substring(i,(i+1)).equals("x")))
				x++;
			if((enter.substring(i,(i+1)).equals("Y"))||(enter.substring(i,(i+1)).equals("y")))
				y++;
			if((enter.substring(i,(i+1)).equals("Z"))||(enter.substring(i,(i+1)).equals("z")))
				z++;
		}
	}
	
	
	public String toString()
	{
		search();
		String out="The Frequency Of Each Letter Is:\n";
		if(a!=0)
			out+="A="+a+"\n";
		if(b!=0)
			out+="B="+b+"\n";
		if(c!=0)
			out+="C="+c+"\n";
		if(d!=0)
			out+="D="+d+"\n";
		if(e!=0)
			out+="E="+e+"\n";
		if(f!=0)
			out+="F="+f+"\n";
		if(g!=0)
			out+="G="+g+"\n";
		if(h!=0)
			out+="H="+h+"\n";
		if(it!=0)
			out+="I="+it+"\n";
		if(j!=0)
			out+="J="+j+"\n";
		if(k!=0)
			out+="K="+k+"\n";
		if(l!=0)
			out+="L="+l+"\n";
		if(m!=0)
			out+="M="+m+"\n";
		if(n!=0)
			out+="N="+n+"\n";
		if(o!=0)
			out+="O="+o+"\n";
		if(p!=0)
			out+="P="+p+"\n";
		if(q!=0)
			out+="Q="+q+"\n";
		if(r!=0)
			out+="R="+r+"\n";
		if(s!=0)
			out+="S="+s+"\n";
		if(t!=0)
			out+="T="+t+"\n";
		if(u!=0)
			out+="U="+u+"\n";
		if(v!=0)
			out+="V="+v+"\n";
		if(w!=0)
			out+="W="+w+"\n";
		if(x!=0)
			out+="X="+x+"\n";
		if(y!=0)
			out+="Y="+y+"\n";
		if(z!=0)
			out+="Z="+z+"\n";
		return out;
	}
}