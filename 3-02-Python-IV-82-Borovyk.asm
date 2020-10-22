mov eax, 10
push eax
mov eax, 21
push eax
mov eax, 4
push eax
pop ebx
pop eax
cdq
idiv ebx
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
add eax, ebx