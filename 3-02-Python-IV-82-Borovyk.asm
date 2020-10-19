mov eax, 5
push eax
mov eax, 6
neg eax
push eax
mov eax, [ebp - 4]
push eax
mov eax, [ebp - 8]
push eax
pop eax
pop ebx
cdq
imul ebx