#include <iostream>
#include <string>
#include <stdint.h>
using namespace std;
int main()
{
	int b;
  	asm (

	"xor rdx, rdx;"
	"push rbp;"
	"mov rbp, rsp;"
	"mov rax, 100;"
	"mov rsp, rbp;"
	"pop rbp;"
  		 : "=r" ( b )
  		 );
	cout << b << endl;
	return 0;
}
