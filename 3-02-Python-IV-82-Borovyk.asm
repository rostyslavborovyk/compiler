mov eax, 0
push eax


mov eax, 20
neg eax
push eax
mov eax, 5
push eax
pop ebx
pop eax
cdq
idiv ebx
push eax
mov eax, 100
cmp eax, 0
je _there_1
jmp _end1_1
_there_1:
mov eax, [ebp - 4]
cmp eax, 0
je _end0_1
jmp _end1_1
_end1_1:
mov eax, 1
jmp _end_1
_end0_1:
xor eax, eax
jmp _end_1
_end_1:
push eax
pop eax
pop ebx
cdq
imul ebx
push eax


mov eax, 20
push eax
mov eax, 2
push eax
pop ebx
pop eax
cdq
idiv ebx
push eax
mov eax, [ebp - 8]
push eax
mov eax, 2
push eax
pop ebx
pop eax
cdq
idiv ebx
push eax
pop eax
pop ebx
cdq
imul ebx

