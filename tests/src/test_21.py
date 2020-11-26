def is_prime(n):
    curr = 2
    # checks mod of all numbers from 2 end n-1, if mod == 0 then number is not prime
    while curr < n:
        if n % curr == 0:
            return 0
        else:
            curr = curr + 1
    return 1


def main(start, end):
    summ = 0
    curr = start
    # checks all numbers in range (start, end), if number is prime then adds it value to summ
    while curr <= end:
        if is_prime(curr):
            summ = summ + curr
            curr = curr + 1
        else:
            curr = curr + 1
    return summ


main(2, 100)
