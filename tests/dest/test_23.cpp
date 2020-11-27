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
	"mov rax, 0b1010;"
	"push rax;"
	"mov rax, 0b10;"
	"push rax;"
	"pop rax;"
	"pop rbx;"
	"add rax, rbx;"
	"push rax;"
	"mov rax, 0b100;"
	"push rax;"
	"pop rbx;"
	"pop rax;"
	"cqo;"
	"idiv rbx;"
	"jmp _func_main_pre_end;"
	"_func_main_pre_end:;"
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
