mov eax, 12
push eax
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
mov eax, 6
push eax
pop eax
pop ebx
xor edx, edx
cdq
imul ebx
push eax
mov eax, [ebp - 8]
push eax
mov eax, 2
push eax
pop eax
pop ebx
add eax, ebx
push eax
mov eax, [ebp - 12]
push eax
mov eax, 2
push eax
pop ebx
pop eax
cdq
idiv ebx
push eax
jmp _post_cond_1
_else_1:
mov eax, 10
mov [ebp - 4], eax
mov eax, [ebp - 4]
push eax
mov eax, 2
push eax
pop ebx
pop eax
cdq
idiv ebx
mov [ebp - 16], eax
_post_cond_1:
mov eax, [ebp - 16]