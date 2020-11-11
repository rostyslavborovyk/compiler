jmp _func_main_end
_func_main:
push ebp
mov ebp, esp
mov eax, 0
cmp eax, 0
je _there_2
jmp _end1_2
_there_2:
mov eax, 0
cmp eax, 0
je _end0_2
jmp _end1_2
_end1_2:
mov eax, 1
jmp _end_2
_end0_2:
xor eax, eax
jmp _end_2
_end_2:
cmp eax, 0
je _else_1
mov eax, 10
push eax
jmp _post_cond_1
_else_1:
mov eax, 6
mov [ebp - 4], eax
_post_cond_1:
mov eax, [ebp - 4]
mov esp, ebp
pop ebp
ret 
_func_main_end:
call _func_main