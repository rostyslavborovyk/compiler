mov eax, 64
push eax
mov eax, 2

push eax
pop ebx
pop eax
idiv ebx


push eax
mov eax, 4

push eax
mov eax, 2

push eax
pop ebx
pop eax
idiv ebx


push eax
pop ebx
pop eax
mov edx, 1
neg edx
neg eax
idiv ebx
