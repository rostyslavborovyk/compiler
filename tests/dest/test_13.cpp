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
	"mov rax, 16;"
	"push rax;"
	"mov rax, 2;"
	"push rax;"
	"mov rax, 12;"
	"push rax;"
	"mov rax, 3;"
	"push rax;"
	"pop rbx;"
	"pop rax;"
	"cqo;"
	"idiv rbx;"
	"push rax;"
	"pop rax;"
	"pop rbx;"
	"xor rdx, rdx;"
	"cqo;"
	"imul rbx;"
	"push rax;"
	"mov rax, 4;"
	"push rax;"
	"pop rbx;"
	"pop rax;"
	"cqo;"
	"idiv rbx;"
	"push rax;"
	"pop rax;"
	"pop rbx;"
	"add rax, rbx;"
	"push rax;"
	"mov rax, 2;"
	"push rax;"
	"mov rax, [rbp - 16];"
	"push rax;"
	"mov rax, [rbp - 8];"
	"push rax;"
	"mov rax, [rbp - 16];"
	"push rax;"
	"pop rax;"
	"pop rbx;"
	"add rax, rbx;"
	"push rax;"
	"pop rax;"
	"pop rbx;"
	"xor rdx, rdx;"
	"cqo;"
	"imul rbx;"
	"mov [rbp - 16], rax;"
	"mov rax, [rbp - 16];"
	"mov rsp, rbp;"
	"pop rbp;"

  		 : "=r" ( b )
  		 );
	cout << b << endl;
	return 0;
}
