mov eax, 4
neg eax
push eax
mov eax, 2
push eax
mov eax, [ebp - 4]
push eax
mov eax, [ebp - 8]
push eax
pop ebx
pop eax
cdq
idiv ebx