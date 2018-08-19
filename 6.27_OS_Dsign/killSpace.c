#include <stdio.h>

int main(void)
{
	int c,n=0,max=2;
	while((c=getchar())!=EOF)
	{
		if(c=='\n')
			n++;
		else
			n=0;
		if(n<max)
			putchar(c);
	}
}
