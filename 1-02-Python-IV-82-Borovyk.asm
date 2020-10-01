mov eax, 20
push eax
mov eax, 2
neg eax

push eax
pop ebx
pop eax
mov edx, 1
neg edx
idiv ebx

neg eax
