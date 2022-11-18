def reverse_string(str):
    reverse_str = ""
    for i in range(len(str)-1, -1, -1):
        reverse_str += str[i]
    return reverse_str

def recursive_fib(n):
    if(n < 2):
        return n
    fib1 = n-1
    fib2 = n-2
    return (recursive_fib(fib1) + recursive_fib(fib2))

def iterative_fib(n):
    index = 0
    fib_sum = 0
    previous_total = 2
    temp_prev_total = 0
    while(index != n + 1):
        if (index <= 2):
            fib_sum += index
        else:
            temp_prev_total = previous_total
            previous_total = fib_sum
            fib_sum += previous_total
            previous_total = temp_prev_total
        print (fib_sum)
        index += 1
    return fib_sum
print(reverse_string("hello"))

print(recursive_fib(10))

print(iterative_fib(10))