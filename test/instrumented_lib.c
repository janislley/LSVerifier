#include <stdio.h>
#include "lib.h"

int lib_div(int x, int y) {
__ESBMC_assume(y == 10);
__ESBMC_assume(y == 4);
#ifdef __FRAMAC__
	Frama_C_show_each_lib_div(y);
#endif
#ifdef __FRAMAC__
	Frama_C_show_each_lib_div(y);
#endif
	return(x/y);
}

int lib_if(int x, int y) {
	if( x > 0 && y > 0)
		return (lib_div(x,y));
	else
		return 0;
}
