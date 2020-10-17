mov eax, 32
neg eax
push eax
mov eax, 2
push eax
pop ebx
pop eax
cdq
idiv ebx
push eax


mov eax, 32
push eax
mov eax, 2
push eax
pop ebx
pop eax
cdq
idiv ebx
push eax
mov eax, 2
neg eax
push eax
mov eax, 2
push eax
pop ebx
pop eax
cdq
idiv ebx
push eax
pop ebx
pop eax
cdq
idiv ebx
push eax


mov eax, [ebp - 4]
push eax
mov eax, 2
neg eax
push eax
pop ebx
pop eax
cdq
idiv ebx
neg eax
push eax
mov eax, [ebp - 8]
push eax
mov eax, 8
push eax
pop ebx
pop eax
cdq
idiv ebx
push eax
pop ebx
pop eax
cdq
idiv ebx

