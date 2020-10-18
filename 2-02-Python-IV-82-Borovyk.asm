mov eax, 5
cmp eax, 0
je _there_1
jmp _end1_1
_there_1:
mov eax, 0
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

