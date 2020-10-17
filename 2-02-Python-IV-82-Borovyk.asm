mov eax, 6
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
je _there_1
jmp _end1_1
_there_1:
mov eax, 0
cmp eax, 0
je _there_3
jmp _end1_3
_there_3:
mov eax, 0
cmp eax, 0
je _end0_3
jmp _end1_3
_end1_3:
mov eax, 1
jmp _end_3
_end0_3:
xor eax, eax
jmp _end_3
_end_3:
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


mov eax, [ebp - 4]
push eax
mov eax, 3
push eax
pop eax
pop ebx
cdq
imul ebx

