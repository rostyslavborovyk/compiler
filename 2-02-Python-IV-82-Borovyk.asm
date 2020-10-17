mov eax, 12
neg eax
push eax
mov eax, 4
push eax
pop eax
pop ebx
cdq
imul ebx
push eax


mov eax, 60
push eax
mov eax, 15
push eax
pop ebx
pop eax
cdq
idiv ebx
push eax


mov eax, [ebp - 4]
neg eax
push eax
mov eax, [ebp - 8]
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

