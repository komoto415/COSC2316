# YOUR NAME HERE
# inclass_one.py
# 1/27/2021
# This file is our first in class practice!
# There are three method prompts that we will look to fill out and analyze their performance
# Each method will utilize the fibonacci functions defined below.
# A main method with calls for testing has been provided

import random

# A recursive approach to generate the nth Fibonacci number 
# It returns the number and the total number of operations to generate
def recursive_fib(n):
    if (n <= 0):
        return [0, 2]
    elif (n == 1):
        return [1, 4]
    else:
        res1 = recursive_fib(n - 1)
        res2 = recursive_fib(n-2)
        ops = res1[1] + res2[1] + 12
        return [res1[0] + res2[0], ops]
        


# An iterative approach to generate the nth Fibonacci number 
# It returns the number and the total number of operations to generate
def iterative_fib(n):
    if (n <= 0):
        return [0,2]
    ops = 5
    num1 = 0
    num2 = 1
    for i in range(1,n):
        temp = num1 + num2
        num1 = num2
        num2 = temp 

        # num1, num2 = (num2, num1 + num2)

        ops += 6
    return [num2, ops]


# This function will return members of the input array that are members of the fibonacci sequence
def func1(my_data):
    fib_set = set()
    result = []
    num_ops = 2

    # fib_set, ops = zip(*[iterative_fib(x) for x in my_data])
    # num_ops += sum(ops) + len(ops)
    # result = [x for x in my_data if x in fib_set]
    # num_ops += len(my_data) + len(result)

    for i in my_data:
        data, ops = iterative_fib(i)
        fib_set.add(data)
        num_ops += ops + 2 # set adding and function call

    for i in my_data:
        if i in fib_set:
            result.append(i)
            num_ops += 1 # accounting only for append
        num_ops += 1 # condition check


    return [result,num_ops]
    
    
    
# This function will return a single value based on the input array.    
# It will return the product of the two largest fibonacci numbers present inside the original array.
def func2(my_data):
    fib_seq, ops = func1(my_data)
    max_fib = -1
    max_max_fib = -1
    num_ops = ops + 3         # account for ops of function, fucntion call and intialisations
    for i in fib_seq:
        if i > max_fib:
            if max_fib > max_max_fib:
                max_max_fib = i
            else: 
                max_fib = i
            num_ops += 2        # looking for even bigger and assignment
        num_ops += 1            # check if big enough
    result = max_fib * max_max_fib
    return [result, num_ops]


# This function will return a transformed array. 
# If a number is even, it will then perform a number of checks:
#   If it is divisible by 14, it will cube it. 
#   If it is not divisible by 14, but divisible by 4, it will square it. 
#   If it is just even (such as 6), it will not be modified. 
# If a number is odd, it will be replaced with the result of a recursive fibonacci call.

def func3(my_data):
    num_ops = 0 
    result = []
    for data in my_data:
        if data % 2 == 0:
            if data % 14 == 0:
                result.append(data ** 3)
            elif data % 14 != 0 and data % 4 == 0:
                result.append(data ** 2)
            else:
                result.append(data)
            num_ops += 2 # only to account for num checks because there will always been an append, accounted for outside of upper condition check
        else:
            result.append(iterative_fib(data))
        num_ops += 2        # 1 prelim check, will always end in an appending
    return [result, num_ops]

def main():
    print("This program's goal is to assist us in understanding the runtime complexity of our methods.")
    print("We will construct three methods and analyze their run time.")
    print("We will test each method with four arrays of integers.")
    print("One array will be of size 5, the other three will be of size 100.") 
    print("Method one will return members of the input array that are members of the fibonacci sequence")
    print("Method two will return a single value. It will return the product of the two largest fibonacci numbers present inside the original array.")
    print("Method three will return a transformed array. If a number is even, if it is divisible by 14, it will instead cube it. If it is not divisible by 14, but divisible by 4, it will square it. If it is just even (such as 6), it will not be modified. If the number is odd, it will be replaced with the result of a recursive fibonacci call.")
    for i in range(20):
        print("The fibonacci number %d is %r" % (i, recursive_fib(i)))
    for i in range(20):
        print("The fibonacci number %d is %r" % (i, iterative_fib(i)))
        
    data_one = [1,2,3,4,5]
    data_two = []
    data_three = []
    data_four = []
    for i in range(1,101):
        data_two.append(i)
    for i in range(2,201,2):
        data_three.append(i)
    for i in range(1,201,2):
        data_four.append(i)
    print("%s\n\n%s\n\n%s" % (data_two, data_three, data_four))

    # print("\n\nWe will now call the functions with the above arrays.")
    # print("\nFirst function 1 will be called.")
    # print("When called with data_one, the result is: ")
    # print(func1(data_one))
    # print("\nWhen called with data_two, the result is: ")
    # print(func1(data_two))
    # print("\nWhen called with data_three, the result is: ")
    # print(func1(data_three))
    # print("\nWhen called with data_four, the result is: ")
    # print(func1(data_four))
    
    # print("\nNext we call Function 2.")
    # print("When called with data_one, the result is: ")
    # print(func2(data_one))
    # print("When called with data_two, the result is: ")
    # print(func2(data_two))
    # print("When called with data_three, the result is: ")
    # print(func2(data_three))
    # print("When called with data_four, the result is: ")
    # print(func2(data_four))
    
    # print("\nFinally we call Function 3.")
    # print("When called with data_one, the result is: ")
    # print(func3(data_one))
    # print("When called with data_two, the result is: ")
    # print(func3(data_two))
    # print("When called with data_three, the result is: ")
    # print(func3(data_three))
    # print("When called with data_four, the result is: ")
    # print(func3(data_four))





main()
