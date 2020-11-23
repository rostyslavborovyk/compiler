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
	"mov rax, 0;"
	"push rax;"
	"mov rax, [rbp - 8];"
	"cmp rax, 0;"
	"je _there_1;"
	"jmp _end1_1;"
	"_there_1:;"
	"mov rax, [rbp - 16];"
	"cmp rax, 0;"
	"je _end0_1;"
	"jmp _end1_1;"
	"_end1_1:;"
	"mov rax, 1;"
	"jmp _end_1;"
	"_end0_1:;"
	"xor rax, rax;"
	"jmp _end_1;"
	"_end_1:;"
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
