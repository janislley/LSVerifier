#include <stdio.h>
#include <stdlib.h>
#include "lib.h"

int sum(int x, int y)
{
	return (x+y);
}

int div0(int x, int y)
{
	return (x/y);
}

int psum(int *x, int *y)
{
	return (*x+*y);
}

int test_lib(int x, int y)
{
	x++;
	y--;

	return (lib_div(x, y));
}

int main()
{
	int *p1 = NULL;
	int *p2 = NULL;
	int res;
	
	p1 = malloc(sizeof(p1));
	p2 = malloc(sizeof(p2));

	if(p1 && p2){
		*p1 = 1;
		*p2 = 2;
	}
	else
		return 0;

	res = div0(4,2);
	res = div0(12,3);
	res = lib_div(80,10);
	res = test_lib(30,5);

	printf("%d\n", sum(*p1, *p2));
  printf("%d\n", psum(p1, p2));

	free(p1);
	free(p2);
	return 0;
}
