mov eax, 16
push eax
mov eax, 2
push eax
mov eax, 12
push eax
mov eax, 3
push eax
pop ebx
pop eax
cdq
idiv ebx
push eax
pop eax
pop ebx
xor edx, edx
cdq
imul ebx
push eax
mov eax, 4
push eax
pop ebx
pop eax
cdq
idiv ebx
push eax
pop eax
pop ebx
add eax, ebx
push eax
mov eax, 2
push eax
mov eax, [ebp - 8]
push eax
mov eax, [ebp - 4]
push eax
mov eax, [ebp - 8]
push eax
pop eax
pop ebx
add eax, ebx
push eax
pop eax
pop ebx
xor edx, edx
cdq
imul ebx
mov [ebp - 8], eax
mov eax, [ebp - 8]