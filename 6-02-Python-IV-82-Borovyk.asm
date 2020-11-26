jmp _func_is_prime_end
_func_is_prime:
push ebp
mov ebp, esp
mov eax, 2
push eax
_start_cycle_1:
mov eax, [ebp - 4]
push eax
mov eax, [ebp + 8]
push eax
pop ebx
pop eax
cmp eax, ebx
setl al
cmp eax, 0
je _end_cycle_1
mov eax, [ebp + 8]
push eax
mov eax, [ebp - 4]
push eax
pop ebx
pop eax
cdq
idiv ebx
mov eax, edx
push eax
mov eax, 0
push eax
pop ebx
pop eax
cmp eax, ebx
sete al
cmp eax, 0
je _else_2
mov eax, 0
jmp _func_is_prime_pre_end
jmp _post_cond_2
_else_2:
mov eax, [ebp - 4]
push eax
mov eax, 1
push eax
pop eax
pop ebx
add eax, ebx
mov [ebp - 4], eax
_post_cond_2:
jmp _start_cycle_1
_end_cycle_1:
mov eax, 1
jmp _func_is_prime_pre_end
_func_is_prime_pre_end:
mov esp, ebp
pop ebp
ret 4
_func_is_prime_end:
jmp _func_main_end
_func_main:
push ebp
mov ebp, esp
mov eax, 0
push eax
mov eax, [ebp + 8]
push eax
_start_cycle_3:
mov eax, [ebp - 8]
push eax
mov eax, [ebp + 12]
push eax
pop ebx
pop eax
cmp eax, ebx
setle al
cmp eax, 0
je _end_cycle_3
mov eax, [ebp - 8]
push eax
call _func_is_prime
cmp eax, 0
je _else_4
mov eax, [ebp - 4]
push eax
mov eax, [ebp - 8]
push eax
pop eax
pop ebx
add eax, ebx
mov [ebp - 4], eax
mov eax, [ebp - 8]
push eax
mov eax, 1
push eax
pop eax
pop ebx
add eax, ebx
mov [ebp - 8], eax
jmp _post_cond_4
_else_4:
mov eax, [ebp - 8]
push eax
mov eax, 1
push eax
pop eax
pop ebx
add eax, ebx
mov [ebp - 8], eax
_post_cond_4:
jmp _start_cycle_3
_end_cycle_3:
mov eax, [ebp - 4]
jmp _func_main_pre_end
_func_main_pre_end:
mov esp, ebp
pop ebp
ret 8
_func_main_end:
push 100
push 2
call _func_main