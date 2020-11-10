#include <iostream>
#include <string>
#include <stdint.h>
using namespace std;
int main()
{
	int b;
  	asm (

	"push rbp;"
	"mov rbp, rsp;"
	"jmp _func_baz_end;"
	"_func_baz:;"
	"push rbp;"
	"mov rbp, esp;"
	"mov rax, [rbp + 8];"
	"push rax;"
	"mov rax, 2;"
	"push rax;"
	"pop rax;"
	"pop rbx;"
	"add rax, rbx;"
	"push rax;"
	"mov rax, [rbp - 8];"
	"mov esp, rbp;"
	"pop rbp;"
	"ret 4;"
	"_func_baz_end:;"
	"jmp _func_foo_end;"
	"_func_foo:;"
	"push rbp;"
	"mov rbp, esp;"
	"mov rax, [rbp + 12];"
	"push rax;"
	"mov rax, [rbp + 8];"
	"push rax;"
	"pop rax;"
	"pop rbx;"
	"add rax, rbx;"
	"push rax;"
	"mov rax, 10000;"
	"push rax;"
	"mov rax, [rbp - 8];"
	"mov esp, rbp;"
	"pop rbp;"
	"ret 8;"
	"_func_foo_end:;"
	"jmp _func_main_end;"
	"_func_main:;"
	"push rbp;"
	"mov rbp, esp;"
	"push 12;"
	"call _func_baz;"
	"push rax;"
	"push 3;"
	"mov rax, [rbp - 8];"
	"push rax;"
	"call _func_foo;"
	"push rax;"
	"mov rax, [rbp - 16];"
	"push rax;"
	"mov rax, [rbp - 8];"
	"push rax;"
	"pop rax;"
	"pop rbx;"
	"add rax, rbx;"
	"mov esp, rbp;"
	"pop rbp;"
	"ret ;"
	"_func_main_end:;"
	"call _func_main;"
	"mov rsp, rbp;"
	"pop rbp;"

  		 : "=r" ( b )
  		 );
	cout << b << endl;
	return 0;
}
