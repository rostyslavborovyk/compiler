mov eax, 5
neg eax
push eax
mov eax, 6
push eax
mov eax, 1
push eax
mov eax, 4
push eax
mov eax, [ebp - 4]
push eax
mov eax, [ebp - 8]
push eax
pop eax
pop ebx
xor edx, edx
cdq
imul ebx
push eax
mov eax, [ebp - 16]
push eax
pop ebx
pop eax
idiv ebx