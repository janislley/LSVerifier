#include <stdio.h>
#include <stdlib.h>

int sum(int *n1, int *n2) 
{
	return (*n1+*n2);
}

int call_sum(int *n1, int *n2)
{
	return sum(n1, n2);
}

int main(int argc, char *argv[])
{
	int *p1, *p2;
	int out = 0;

	p1 = malloc(sizeof(int));
	if(!p1)
		return 0;
		
	p2 = malloc(sizeof(int));
	if(!p2)
		return 0;

	*p1 = 1;
	*p2 = 2;

	out = sum(p1, p2);
	printf("%d\n", out);

	out = call_sum(p1, p2);
	printf("%d\n", out);

	free(p1);
	free(p2);

	return 0;
}
