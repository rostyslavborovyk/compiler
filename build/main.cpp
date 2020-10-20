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
	"mov rax, 5;"
	"neg rax;"
	"push rax;"
	"mov rax, 6;"
	"push rax;"
	"mov rax, 1;"
	"push rax;"
	"mov rax, 4;"
	"push rax;"
	"mov rax, [rbp - 8];"
	"push rax;"
	"mov rax, [rbp - 16];"
	"push rax;"
	"pop rax;"
	"pop rbx;"
	"xor rdx, rdx;"
	"cdq;"
	"imul rbx;"
	"push rax;"
	"mov rax, [rbp - 32];"
	"push rax;"
	"pop rbx;"
	"pop rax;"
	"idiv rbx;"
	"mov rsp, rbp;"
	"pop rbp;"

  		 : "=r" ( b )
  		 );
	cout << b << endl;
	return 0;
}
