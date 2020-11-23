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
	"mov rax, 12;"
	"push rax;"
	"mov rax, 1;"
	"cmp rax, 0;"
	"je _there_2;"
	"jmp _end1_2;"
	"_there_2:;"
	"mov rax, 20;"
	"neg rax;"
	"cmp rax, 0;"
	"je _end0_2;"
	"jmp _end1_2;"
	"_end1_2:;"
	"mov rax, 1;"
	"jmp _end_2;"
	"_end0_2:;"
	"xor rax, rax;"
	"jmp _end_2;"
	"_end_2:;"
	"cmp rax, 0;"
	"je _else_1;"
	"mov rax, 10;"
	"push rax;"
	"jmp _post_cond_1;"
	"_else_1:;"
	"mov rax, 6;"
	"mov [rbp - 16], rax;"
	"_post_cond_1:;"
	"mov rax, [rbp - 16];"
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
