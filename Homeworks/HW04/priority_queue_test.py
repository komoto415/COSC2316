# YOUR NAME HERE
# heap.py
# 3/15/21
# This program contains implementation for a basic heap structure.
# We will expand on this for in class practice and for the homework
# A heap is a semi sorted datastructure that gives us instant access 
# to the item of most priority in the structure, typically the minimal
# or maximal value. This implementation is for min-heaps.

import random

class MinHeap:
	
    def __init__(self):
        self.size = 0
        self.data = [None]
    
    def peak(self):
        if self.size > 0:
            return self.data[1]
        else:
            return None
    
    def insert(self, item):
        if self.size == 0:
            self.data.append(item)
            self.size += 1
        else:
            self.heapify_up(item)
            self.size += 1
            
    def delete_min(self):
        return None
            
            
    def swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]
        
    def heapify_up(self, item):
        curr = self.size + 1
        self.data.append(item)
        #print("*****************\nAt the start our data is this: %s" % self.data)
        while (curr > 1 and self.data[curr] < self.data[curr // 2]):
            #print("Flipping %s and %s" % (self.data[curr], self.data[curr // 2]))
            self.swap(curr, curr // 2)
            #print("The array is now: %s" % self.data)
            curr = curr // 2
    
    def heapify_down(self):
        return None
                

    def decremenet_all(self, val):
        return None

    
    def __str__(self):
        # return "%s" % self.data
        result = ""
        count = 2
        for i in range(1, len(self.data)):
            if i == count:
                count *= 2
                result += "\n"
            result += "%s\t" % self.data[i]
        return result


def main():
    print("Welcome to the test code for heaps!")
    print("Our first calls will fill the heap, and then we will remove the min value several times")
    print("Afterwards we shall have a test of decrement-all")
    print("Finally you will engage in the teller simulation")
    print("This teller simulation may take the form of a loop here in main OR a method which will be called")
    my_heap = MinHeap()
    
    my_heap.insert(7)
    my_heap.insert(9)
    my_heap.insert(5)
    my_heap.insert(3)
    my_heap.insert(12)
    my_heap.insert(4)
    my_heap.insert(14)
    my_heap.insert(10)
    my_heap.insert(6)
    my_heap.insert(3)
    print(my_heap)
    # The results of the heap should be the following
    # 3
    # 3       4
    # 6       5       7       14
    # 10      9       12
    
    print("Now for removal")
    my_heap.delete_min()
    print(my_heap)
    # After removal one, 12 is rotated to root, swapped with 3, and then 5. 5 has no children so the rotation ends
    # 3
    # 5       4
    # 6       12      7       14
    # 10      9
        
    my_heap.delete_min()
    print(my_heap)
    # After removal two, 9 is rotated to root, swapped with 4, swapped with 7. 7 has no children so the rotation ends
    # 4
    # 5       7
    # 6       12      9       14
    # 10
    
    my_heap.delete_min()
    print(my_heap)
    # After removal three, 10 is rotated to root, swapped with 5, swapped with 6
    # 5
    # 6       7
    # 10      12      9       14
    
    
    print('Now to add four values of 2 and three of 7 to demonstrate the power of decremenet_all')
    my_heap.insert(2)
    my_heap.insert(2)
    my_heap.insert(7)
    my_heap.insert(2)
    my_heap.insert(2)
    my_heap.insert(7)
    my_heap.insert(7)
    print(my_heap)
    # HEre is what the heap should be after the above deletions
    # 2
    # 2       2
    # 5       2       7       7
    # 10      6       12      7       9       7       14
    tmp = my_heap.delete_min()
    my_heap.decremenet_all(tmp)
    # After a call of delete min and then decrement all, this is our heap
    # 3
    # 4       5
    # 5       5       7       5
    # 8       12      10
    print('\n\n%s' % my_heap)
    tmp = my_heap.delete_min()
    my_heap.decremenet_all(tmp)
    print('\n\n%s' % my_heap)
    # After a second delete min (removing 3) our heap now looks like this
    # 1
    # 2       2
    # 5       2       4       2
    # 7       9
    
    # Now run the simulation. As a reminder, your simulation will have X number of tellers
    # and an input array of wait times. You will load X items from the array into the heap
    # Then perform delete-min and decrement all. Then refill the heap to size X and repeat until 
    # all items from the array have passed through the array.
    # If our heap size is 5, and our array is [1,1,5,2,2,3,1], we get the following as the original heap
    # 1
    # 1 5
    # 2 2
    # After delete-min and decrementing, we have the following heap
    # 1
    # 1 4
    # When we load 3 and 1 in, the heap becomes
    # 1
    # 1 4
    # 3 1
    # Delete and decrement gives us
    # 2
    # 3
    # We delete and decrement 2, leaving us with 1 remaining in the heap, then delete and finish


main()