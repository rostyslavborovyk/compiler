jmp _func_baz_end
_func_baz:
push ebp
mov ebp, esp
mov eax, [ebp + 8]
push eax
mov eax, 5
push eax
pop eax
pop ebx
add eax, ebx
push eax
mov eax, 2
push eax
pop eax
pop ebx
xor edx, edx
cdq
imul ebx
push eax
mov eax, [ebp - 4]
mov esp, ebp
pop ebp
ret 4
_func_baz_end:
jmp _func_foo_end
_func_foo:
push ebp
mov ebp, esp
mov eax, [ebp + 8]
push eax
mov eax, 10
push eax
pop eax
pop ebx
xor edx, edx
cdq
imul ebx
mov esp, ebp
pop ebp
ret 4
_func_foo_end:
jmp _func_main_end
_func_main:
push ebp
mov ebp, esp
push 12
call _func_baz
push eax
mov eax, [ebp - 4]
push eax
call _func_foo
push eax
mov eax, [ebp - 8]
push eax
mov eax, [ebp - 4]
push eax
pop ebx
pop eax
sub eax, ebx
mov esp, ebp
pop ebp
ret 
_func_main_end:
call _func_main