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
	"mov rax, 0;"
	"push rax;"
	"mov rax, 1;"
	"cmp rax, 0;"
	"je _there_2;"
	"jmp _end1_2;"
	"_there_2:;"
	"mov rax, 0;"
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
	"mov [rbp - 4], rax;"
	"jmp _post_cond_1;"
	"_else_1:;"
	"mov rax, 6;"
	"mov [rbp - 4], rax;"
	"_post_cond_1:;"
	"mov rax, [rbp - 8];"
	"mov rsp, rbp;"
	"pop rbp;"

  		 : "=r" ( b )
  		 );
	cout << b << endl;
	return 0;
}
