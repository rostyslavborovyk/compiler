#include <iostream>
#include <string>
#include <stdint.h>
using namespace std;
int main()
{
	int b;
  	asm (

	"jmp _func_main_end;"
	"_func_main:;"
	"push rbp;"
	"mov rbp, rsp;"
	"mov rax, 100;"
	"mov rsp, rbp;"
	"pop rbp;"
	"ret ;"
	"_func_main_end:;"
	"call _func_main;"

  		 : "=r" ( b )
  		 );
	cout << b << endl;
	return 0;
}
