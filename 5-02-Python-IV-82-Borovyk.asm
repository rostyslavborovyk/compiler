jmp _func_foo_end
_func_foo:
push ebp
mov ebp, esp
mov eax, 2
push eax
mov eax, [ebp + 8]
push eax
pop eax
pop ebx
xor edx, edx
cdq
imul ebx
push eax
mov eax, 1
push eax
pop eax
pop ebx
add eax, ebx
mov esp, ebp
pop ebp
ret 4
_func_foo_end:
jmp _func_main_end
_func_main:
push ebp
mov ebp, esp
push 2
call _func_foo
push eax
mov eax, [ebp - 4]
mov esp, ebp
pop ebp
ret 
_func_main_end:
call _func_main