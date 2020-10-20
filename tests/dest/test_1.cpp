#include <iostream>
#include <string>
#include <stdint.h>
using namespace std;
int main()
{
	int b;
  	asm (

	"xor rdx, rdx;"
	"push rbp;"
	"mov rbp, rsp;"
	"mov rax, 4;"
	"push rax;"
	"mov rax, 2;"
	"push rax;"
	"mov rax, [rbp - 8];"
	"push rax;"
	"mov rax, [rbp - 16];"
	"push rax;"
	"pop rax;"
	"pop rbx;"
	"cdq;"
	"imul rbx;"
	"mov rsp, rbp;"
	"pop rbp;"
  		 : "=r" ( b )
  		 );
	cout << b << endl;
	return 0;
}
