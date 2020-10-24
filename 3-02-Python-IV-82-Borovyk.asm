mov eax, 12
push eax
mov eax, 5
push eax
pop eax
pop ebx
add eax, ebx
push eax
mov eax, 40
push eax
mov eax, 5
push eax
pop ebx
pop eax
cdq
idiv ebx
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