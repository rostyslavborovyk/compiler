jmp _func_main_end
_func_main:
push ebp
mov ebp, esp
mov eax, 1
push eax
mov eax, 3
push eax
_start_cycle_1:
mov eax, [ebp - 8]
cmp eax, 0
je _end_cycle_1
mov eax, [ebp - 4]
push eax
mov eax, 2
push eax
pop eax
pop ebx
xor edx, edx
cdq
imul ebx
mov [ebp - 4], eax
mov eax, [ebp - 8]
push eax
mov eax, 1
push eax
pop ebx
pop eax
sub eax, ebx
mov [ebp - 8], eax
jmp _start_cycle_1
_end_cycle_1:
mov eax, [ebp - 4]
mov esp, ebp
pop ebp
ret 
_func_main_end:
call _func_main