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
	"mov rax, 2;"
	"push rax;"
	"mov rax, [rbp - 8];"
	"push rax;"
	"mov rax, 4;"
	"push rax;"
	"pop rax;"
	"pop rbx;"
	"add rax, rbx;"
	"mov [rbp - 8], rax;"
	"mov rax, [rbp - 8];"
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
