mov eax, 16

push eax
mov eax, 2
push eax
pop ebx
pop eax
idiv ebx

push eax
mov eax, 10
push eax
mov eax, 5
push eax
pop ebx
pop eax
idiv ebx


push eax
pop ebx
pop eax
idiv ebx
