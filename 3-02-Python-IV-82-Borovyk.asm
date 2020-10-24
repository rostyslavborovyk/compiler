mov eax, 10
neg eax
push eax
mov eax, 5
push eax
pop ebx
pop eax
sub eax, ebx
push eax
mov eax, 7
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