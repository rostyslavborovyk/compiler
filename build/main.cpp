#include <iostream>
#include <string>
#include <stdint.h>
using namespace std;
int main()
{
	int b;
  	asm (

	"jmp _func_foo_end;"
	"_func_foo:;"
	"push rbp;"
	"mov rbp, esp;"
	"mov rax, 2;"
	"push rax;"
	"mov rax, [rbp + 16];"
	"push rax;"
	"pop rax;"
	"pop rbx;"
	"xor rdx, rdx;"
	"cqo;"
	"imul rbx;"
	"push rax;"
	"mov rax, 1;"
	"push rax;"
	"pop rax;"
	"pop rbx;"
	"add rax, rbx;"
	"mov esp, rbp;"
	"pop rbp;"
	"ret 4;"
	"_func_foo_end:;"
	"jmp _func_main_end;"
	"_func_main:;"
	"push rbp;"
	"mov rbp, esp;"
	"push 2;"
	"call _func_foo;"
	"push rax;"
	"mov rax, [rbp - 8];"
	"mov esp, rbp;"
	"pop rbp;"
	"ret ;"
	"_func_main_end:;"
	"call _func_main;"
	"mov b, eax;"

  		 : "=r" ( b )
  		 );
	cout << b << endl;
	return 0;
}
