# PYTHON COMPILER

##### Compiles python programs to asm and executable file

## Description

- compiles .py files to .asm, .cpp(with inline assembly), and executables(via g++)
- supports:
  - almost all arithmetical and logical operations
  - variable assignment(only integer type in dec, hex and bin)
  - if-else conditional statements
  - while loops(with break and continue)
  - functions 


## Quickstart

#### `src.py`
``` python
def is_prime(n):
    curr = 2
    # checks mod of all numbers from 2 end n-1, if mod == 0 then number is not prime
    while curr < n:
        if n % curr == 0:
            return 0
        else:
            curr += 1
    return 1


def main(start, end):
    summ = 0
    curr = start
    # checks all numbers in range (start, end), if number is prime then adds it's value to summ
    while curr <= end:
        if is_prime(curr):
            summ += curr
            curr += 1
        else:
            curr += 1
    return summ


main(2, 10)
```

``` shell script
python compiler.py --src src.py --arch 64
```
P.S. set arch to 32 if you have a 32 bit g++

#### `output.asm`
``` nasm
jmp _func_is_prime_end
_func_is_prime:
push rbp
mov rbp, rsp
mov rax, 2
push rax
_start_cycle_1:
mov rax, [rbp - 8]
push rax
mov rax, [rbp + 16]
push rax
pop rbx
pop rcx
xor rax, rax
cmp rcx, rbx
setl al
cmp rax, 0
je _end_cycle_1
mov rax, [rbp + 16]
push rax
mov rax, [rbp - 8]
push rax
pop rbx
pop rax
cqo
idiv rbx
mov rax, rdx
push rax
mov rax, 0
push rax
pop rbx
pop rcx
xor rax, rax
cmp rcx, rbx
sete al
cmp rax, 0
je _else_2
mov rax, 0
jmp _func_is_prime_pre_end
jmp _post_cond_2
_else_2:
mov rax, [rbp - 8]
push rax
mov rax, 1
push rax
pop rax
pop rbx
add rax, rbx
mov [rbp - 8], rax
_post_cond_2:
jmp _start_cycle_1
_end_cycle_1:
mov rax, 1
jmp _func_is_prime_pre_end
_func_is_prime_pre_end:
mov rsp, rbp
pop rbp
ret 8
_func_is_prime_end:
jmp _func_main_end
_func_main:
push rbp
mov rbp, rsp
mov rax, 0
push rax
mov rax, [rbp + 16]
push rax
_start_cycle_3:
mov rax, [rbp - 16]
push rax
mov rax, [rbp + 24]
push rax
pop rbx
pop rcx
xor rax, rax
cmp rcx, rbx
setle al
cmp rax, 0
je _end_cycle_3
mov rax, [rbp - 16]
push rax
call _func_is_prime
cmp rax, 0
je _else_4
mov rax, [rbp - 8]
push rax
mov rax, [rbp - 16]
push rax
pop rax
pop rbx
add rax, rbx
mov [rbp - 8], rax
mov rax, [rbp - 16]
push rax
mov rax, 1
push rax
pop rax
pop rbx
add rax, rbx
mov [rbp - 16], rax
jmp _post_cond_4
_else_4:
mov rax, [rbp - 16]
push rax
mov rax, 1
push rax
pop rax
pop rbx
add rax, rbx
mov [rbp - 16], rax
_post_cond_4:
jmp _start_cycle_3
_end_cycle_3:
mov rax, [rbp - 8]
jmp _func_main_pre_end
_func_main_pre_end:
mov rsp, rbp
pop rbp
ret 16
_func_main_end:
push 10
push 2
call _func_main
```

### Result of executable file
```shell script
./output
17
```
