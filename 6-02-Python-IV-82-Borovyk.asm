jmp _func_main_end
_func_main:
push ebp
mov ebp, esp
mov eax, 0b1010
push eax
mov eax, 0b10
push eax
pop eax
pop ebx
add eax, ebx
push eax
mov eax, 0b100
push eax
pop ebx
pop eax
cdq
idiv ebx
jmp _func_main_pre_end
_func_main_pre_end:
mov esp, ebp
pop ebp
ret 
_func_main_end:
call _func_main