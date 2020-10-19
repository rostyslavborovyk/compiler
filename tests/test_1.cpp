#include <iostream>
#include <string>
#include <stdint.h>
using namespace std;
int main()
{
	int b;
  	asm (

	"xor rdx, rdx;"
	"mov rax, 64;"
	"push rax;"
	"mov rax, 2;"
	"push rax;"
	"pop rbx;"
	"pop rax;"
	"idiv rbx;"
	"push rax;"
	"mov rax, 16;"
	"push rax;"
	"mov rax, 4;"
	"push rax;"
	"pop rbx;"
	"pop rax;"
	"idiv rbx;"
	"push rax;"
	"pop rbx;"
	"pop rax;"
	"mov rdx, 1;"
	"neg rdx;"
	"neg rax;"
	"idiv rbx;"
  		 : "=r" ( b )
  		 );
	cout << b << endl;
	return 0;
}
