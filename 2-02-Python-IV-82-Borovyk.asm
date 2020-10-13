mov eax, 16

push eax
mov eax, 4

push eax
pop ebx
pop eax
idiv ebx

push eax
mov eax, 32

push eax
mov eax, 16

push eax
pop ebx
pop eax
idiv ebx

push eax
pop ebx
pop eax
idiv ebx
