def main():
    a = 1
    n = 4
    while n:
        if n-2:
            a *= 2
        else:
            break
        n = n - 1
    return a

main()