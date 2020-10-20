#include <iostream>
#include <string>
#include <stdint.h>
using namespace std;
int main()
{
	int b;
  	asm (

	CODE
  		 : "=r" ( b )
  		 );
	cout << b << endl;
	return 0;
}
