# Jeffrey Ng
# inclass_two.py
# Created 2/8/2021
# This file shall be used to work through inclass assignment two.
# For this assignment we will utilize a stack object and implement three operations
# Operation One: Given two stacks, determine if the stacks are identical (same items in same order)
# This operation MUST be performed without permanent modification to the original stack.
# Operation Two: Given two input stacks, determine if the stacks contain the same set of items, without respect to order 
# This operation MUST be performed without permanent modification to the original stack.
# Operation Three: Using two stacks, simulate the performance of a queue. You must create the enqueue and dequeue functions


class Queue:

    def __init__(self):
        self.size = 0
        self.queue = []

    # head will be arr[0
    # tail will be arr[size-1]
    def enqueue(self, item):
        self.queue.append(item)
        self.size += 1

    def dequeue(self):
        self.queue.pop(0)
        self.size -= 1

    def peek(self):
        return self.queue[0]

    def get_size(self):
        return self.size

    def __str__(self):
        result: str = "["
        for i, e in enumerate(self.queue):
            result += f"{e}"
            if i != self.get_size() - 1:
                result += ", "
        return result + "]"

# This class contains implementation of an array stack.
class Stack():

    # Declares an initially empty stack 
    def __init__(self):
        self.size = 0
        self.stack = []

    # Pushes an item to the top of the stack
    def push(self, item):
        self.stack.append(item)
        self.size += 1
        
    # Removes the top item from the stack
    def	pop(self):
        if (self.size <= 0):
            print("You are attempting to delete from an empty stack.")
            print("In a proper code environment we would throw an exception here")
        else:
            self.size -= 1
            return self.stack.pop()

    # Returns the top item of the stack (without removing it)
    def peek(self):
        if (self.size == 0):
            print("Currently the stack is empty!")
        else:
            print("The top item of the stack is currently: %s" % self.stack[self.size-1])

    # Returns the size of the stack
    def get_size(self):
        return self.size

    # Tostring method for the stack
    def __str__(self):
        result: str = "["
        for i, e in enumerate(self.stack):
            result += f"{e}"
            if i != self.get_size() - 1:
                result += ", "
        return result + "]"



def rebuild_stack(stack, aux_list):
    for i in reversed(aux_list):
        stack.push(i)

# This function will check to see if two stacks are identical to one another
# It will not permanently modify either stack.        
def func_one(stack1, stack2):
    s1_hold: list = []
    s2_hold: list = []
    retVal: bool = False
    if stack1.get_size() == stack2.get_size():
        still_equal: bool = True
        while still_equal and stack1.get_size() > 0:
            s1_hold.append(stack1.pop())
            s2_hold.append(stack2.pop())
            still_equal = s1_hold == s2_hold
            # print(still_equal)

        retVal = still_equal
        
        rebuild_stack(stack1, s1_hold)
        rebuild_stack(stack2, s2_hold)

    return retVal
    
    
# This function will check to see if two stacks contain the same content (not necessarily same order)
# It will not permanently modify either stack.    
def func_two(stack1, stack2):
    s1_hold: list = []
    s2_hold: list = []
    retVal: bool = False
    if stack1.get_size() == stack2.get_size():
        while stack1.get_size() > 0:
            s1_hold.append(stack1.pop())
            s2_hold.append(stack2.pop())

        retVal = set(s1_hold) == set(s2_hold)

        rebuild_stack(stack1, s1_hold)
        rebuild_stack(stack2, s2_hold)

    return retVal

# This class will utilize two stacks to represent a queue
class StackQueue:
    
    def __init__(self):
        self.stack1 = Stack()
        self.stack2 = Stack()
        self.size = 0
        # You may wish to declare other variables
        

    # top of the stack is the head
    # bottom of the stack is the tail
    def enqueue(self, data):
        while self.stack1.get_size() > 0:
            self.stack2.push(self.stack1.pop())
        self.stack2.push(data)
        while self.stack2.get_size() > 0:
            self.stack1.push(self.stack2.pop())
        self.size += 1
        
    def dequeue(self):
        self.stack1.pop()
        self.size -= 1
            
    def __str__(self):
        return "The contents of the StackQueue are:\nStack1:\n%s\n\nStack2:\n%s" % (self.stack1, self.stack2)
		

def foo(num1: int, num2: int, str: str) -> str:
    pass
		
		
def main():
    queue1 = Queue()
    for i in range(5):
        queue1.enqueue(i+5)
    print("Queue:", queue1)
    print("This file will execute the methods of inclass two.")

    queue1.dequeue()
    print("Newly dequeued queue:", queue1)
    
    # First to create the stacks that will test functions one and two.
    sStack1 = Stack()
    sStack2 = Stack()
    sStack3 = Stack()
    sStack4 = Stack()
    lStack1 = Stack()
    lStack2 = Stack()
    lStack3 = Stack()
    lStack4 = Stack()
    
    for i in range(5):
        sStack1.push(i)
        sStack2.push(i)
    
    for i in range(4,-1,-1):
        sStack3.push(i)
        
    sStack4.push(1)
    sStack4.push(3)
    sStack4.push(5)
    
    print(sStack1)
    print(sStack2)
    print(sStack3)
    print(sStack4)
    
    for i in range(50):
        lStack1.push(i)
        lStack2.push(i)
    
    for i in range(49,-1,-1):
        lStack3.push(i)
        
    for i in range(0,50,2):
        lStack4.push(i)

    # print(lStack1)
    # print(lStack2)
    # print(lStack3)
    # print(lStack4)
    
    print("First we will test whether or not the stacks are identical.")
    print("Stacks 1 and 2 for small and large are identical.\nStacks 1, 2, and 3 all contain the same datapoints.\nStack 4 is missing datapoints compared to stacks 1, 2, and 3.")
    print("The result of calling func_one on sStack1 and sStack2 is: %s" % func_one(sStack1, sStack2))
    print("The result of calling func_one on sStack1 and sStack3 is: %s" % func_one(sStack1, sStack3))
    print("The result of calling func_one on sStack1 and sStack4 is: %s" % func_one(sStack1, sStack4))
    print("The result of calling func_one on sStack2 and sStack1 is: %s" % func_one(sStack2, sStack1))
    print("The result of calling func_one on sStack2 and sStack3 is: %s" % func_one(sStack2, sStack3))
    print("The result of calling func_one on sStack2 and sStack4 is: %s" % func_one(sStack2, sStack4))
    print("The result of calling func_one on sStack3 and sStack4 is: %s" % func_one(sStack3, sStack4))
    
    # print("The result of calling func_one on lStack1 and lStack2 is: %s" % func_one(lStack1, lStack2))
    # print("The result of calling func_one on lStack1 and lStack3 is: %s" % func_one(lStack1, lStack3))
    # print("The result of calling func_one on lStack1 and lStack4 is: %s" % func_one(lStack1, lStack4))
    # print("The result of calling func_one on lStack2 and lStack1 is: %s" % func_one(lStack2, lStack1))
    # print("The result of calling func_one on lStack2 and lStack3 is: %s" % func_one(lStack2, lStack3))
    # print("The result of calling func_one on lStack2 and lStack4 is: %s" % func_one(lStack2, lStack4))
    # print("The result of calling func_one on lStack3 and lStack4 is: %s" % func_one(lStack3, lStack4))


    print("\n\nNow for function 2")
    print("The result of calling func_two on sStack1 and sStack2 is: %s" % func_two(sStack1, sStack2))
    print("The result of calling func_two on sStack1 and sStack3 is: %s" % func_two(sStack1, sStack3))
    print("The result of calling func_two on sStack1 and sStack4 is: %s" % func_two(sStack1, sStack4))
    print("The result of calling func_two on sStack2 and sStack1 is: %s" % func_two(sStack2, sStack1))
    print("The result of calling func_two on sStack2 and sStack3 is: %s" % func_two(sStack2, sStack3))
    print("The result of calling func_two on sStack2 and sStack4 is: %s" % func_two(sStack2, sStack4))
    print("The result of calling func_two on sStack3 and sStack4 is: %s" % func_two(sStack3, sStack4))
    
    # print("The result of calling func_two on lStack1 and lStack2 is: %s" % func_two(lStack1, lStack2))
    # print("The result of calling func_two on lStack1 and lStack3 is: %s" % func_two(lStack1, lStack3))
    # print("The result of calling func_two on lStack1 and lStack4 is: %s" % func_two(lStack1, lStack4))
    # print("The result of calling func_two on lStack2 and lStack1 is: %s" % func_two(lStack2, lStack1))
    # print("The result of calling func_two on lStack2 and lStack3 is: %s" % func_two(lStack2, lStack3))
    # print("The result of calling func_two on lStack2 and lStack4 is: %s" % func_two(lStack2, lStack4))
    # print("The result of calling func_two on lStack3 and lStack4 is: %s" % func_two(lStack3, lStack4))
    
    
    print("\n\nNow for the StackQueue")
    my_queue = StackQueue()
    my_queue.enqueue(1)
    my_queue.enqueue(2)
    my_queue.enqueue(3)
    my_queue.enqueue(4)
    my_queue.enqueue(5)
    print(my_queue)
    my_queue.dequeue()
    my_queue.dequeue()
    print(my_queue)
    my_queue.enqueue(6)
    print(my_queue)
    my_queue.enqueue(7)
    my_queue.dequeue()
    print(my_queue)

main()
