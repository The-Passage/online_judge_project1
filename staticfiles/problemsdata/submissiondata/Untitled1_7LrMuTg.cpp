#include <stdio.h>

int main(){
	int a, b, c, s = 0;
	for(a = 0; a<10; a++)
	 for(b = 0; b<10; b++)
	  for(c = 0; c<10; c++) if(a+b+c==9) s++;
	printf("%d\n",s);
}
