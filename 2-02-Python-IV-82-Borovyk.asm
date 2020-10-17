mov eax, 6
cmp eax, 0
je _there_5
jmp _end1_6
_there_5:
mov eax, 0
cmp eax, 0
je _end0_7
jmp _end1_6
_end1_6:
mov eax, 1
jmp _end_8
_end0_7:
xor eax, eax
jmp _end_8
_end_8:
cmp eax, 0
je _there_1
jmp _end1_2
_there_1:
mov eax, 0
cmp eax, 0
je _there_9
jmp _end1_10
_there_9:
mov eax, 0
cmp eax, 0
je _end0_11
jmp _end1_10
_end1_10:
mov eax, 1
jmp _end_12
_end0_11:
xor eax, eax
jmp _end_12
_end_12:
cmp eax, 0
je _end0_3
jmp _end1_2
_end1_2:
mov eax, 1
jmp _end_4
_end0_3:
xor eax, eax
jmp _end_4
_end_4:
push eax


mov eax, [ebp - 4]
push eax
mov eax, 3
push eax
pop eax
pop ebx
cdq
imul ebx

