mov eax, 10
push eax
mov eax, 2
push eax
pop ebx
pop eax
cdq
idiv ebx
push eax
mov eax, 3
push eax
pop eax
pop ebx
cdq
imul ebx
push eax
mov eax, 0
push eax
pop eax
pop ebx
cdq
imul ebx
cmp eax, 0
je _there
jmp _end1
_there:
mov eax, 0
cmp eax, 0
je _end0
jmp _end1
_end1:
mov eax, 1
jmp _end
_end0:
xor eax, eax
jmp _end
_end:
push eax


mov eax, [ebp - 4]
push eax
mov eax, 10
push eax
pop eax
pop ebx
cdq
imul ebx

