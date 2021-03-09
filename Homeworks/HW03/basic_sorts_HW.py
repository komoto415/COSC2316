# Jeffrey
# Submission date here
# basic_sorts_HW.py
# This program contains the same sorting algorithms from basic_sorts.py
# The goal of this assignment is to instrument the code (count the operations)
# so we can verify the performance of sorting algorithms.
# The modifications you perform should not change how the sorting algorithms work, only
# totalling up their operations.
# When dealing with recursive operations, remember we have to return the total operations up the chain
# to ensure full accounting is done (see the recursive fibonacci code for details)
import sys
from os import walk


def main():
    print("In this program will will demonstrate the functionality of a variety of sorting algorithms!")
    print(
            "You will instrument the algorithms and have them print out the total number of operations that they "
            "perform to sort the data")

    print(sys.getrecursionlimit())
    sys.setrecursionlimit(10_000)
    print(sys.getrecursionlimit())

    _, _, file_names = next(walk("./"))
    print(file_names)
    text_files = [x for x in file_names if ".txt" in x and x != "results.txt"]
    print(text_files)
    try:
        # I have a table builder that reads from a file, so that's why I have it set up like this
        with open("results.txt", "w") as n_f:
            n_f.write("Sorting_File Bubble Selection Insertion Shell Merge Quick")
            n_f.write('\n')
            for i, text_file in enumerate(text_files):
                try:
                    print(text_file)
                    with open(text_file, "r") as f:
                        my_data = []
                        for line in f.readlines():
                            temp = line.split()
                            my_data.append(float(temp[0]))


                        ops_list = []
                        print("The data file has been read in, we will now sort it via each method")


                        to_sort = build_array(my_data)
                        print("Before bubble sorting is our data sorted: %s" %
                              isSorted(to_sort), end=". ")
                        ops = bubbleSort(to_sort)
                        print("After bubble sorting our data is sorted: %s" % isSorted(to_sort))
                        ops_list.append(ops)

                        to_sort = build_array(my_data)
                        print("Before selection sorting is our data sorted: %s" % isSorted(to_sort), end=". ")
                        ops = selectionSort(to_sort)
                        print("After selection sorting our data is sorted: %s" % isSorted(to_sort))
                        ops_list.append(ops)

                        to_sort = build_array(my_data)
                        print("Before insertion sorting is our data sorted: %s" % isSorted(to_sort), end=". ")
                        ops = insertionSort(to_sort)
                        print("After insertion sorting our data is sorted: %s" % isSorted(to_sort))
                        ops_list.append(ops)

                        to_sort = build_array(my_data)
                        print("Before shell sorting is our data sorted: %s" % isSorted(to_sort), end=". ")
                        ops = shellSort(to_sort)
                        print("After shell sorting our data is sorted: %s" % isSorted(to_sort))
                        ops_list.append(ops)

                        to_sort = build_array(my_data)
                        print("Before merge sorting is our data sorted: %s" % isSorted(to_sort), end=". ")
                        ops = mergeSort(to_sort, ops=0)
                        print("After merge sorting our data is sorted: %s" % isSorted(to_sort))
                        ops_list.append(ops)

                        to_sort = build_array(my_data)
                        print("Before quick sorting is our data sorted: %s" % isSorted(to_sort), end=". ")
                        ops = quickSort(to_sort, 0, len(to_sort) - 1, ops=0)
                        print("After quick sorting our data is sorted: %s" % isSorted(to_sort))
                        ops_list.append(ops)

                        print('\n\n\n')
                        print(results := f"{text_file.strip('.txt')} {' '.join([str(x) for x in ops_list])}")

                    n_f.write(results)
                    if i != len(text_files) - 1:
                        n_f.write('\n')
                        print('\n' * 80)

                except IOError:
                    print("There was an error reading the file!")

    except IOError:
        print("There was an error reading the file!")

def build_array(my_array):
    result = []
    for item in my_array:
        result.append(item)
    return result

def isSorted(my_array):
    for i in range(len(my_array) - 1):
        if (my_array[i] > my_array[i + 1]):
            return False
    return True

def bubbleSort(my_array):
    ops = 0

    n = len(my_array)
    ops += 1  # assignment
    # Traverse through all array elements
    for i in range(n):
        ops += 2  # loop initialisation
        swapped = False
        ops += 1  # assignment
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            ops += 2  # loop initialisation
            # traverse the array from 0 to n-i-1

            # Swap if the element found is greater
            # than the next element
            ops += 3  # boolean check is always made and double access
            if my_array[j] > my_array[j + 1]:
                my_array[j], my_array[j + 1] = my_array[j + 1], my_array[j]
                ops += 4  # double assignment and access
                swapped = True
                ops += 1  # assignment

        ops += 1  # boolean check is always made
        if (not swapped):
            break

    return ops

def selectionSort(my_array):
    ops = 0

    # Traverse through all array elements
    for i in range(len(my_array)):
        ops += 2  # for loop establishment
        # Find the minimum element in remaining
        # unsorted array
        min_idx = i
        ops += 1  # assignment
        for j in range(i + 1, len(my_array)):
            ops += 2  # for loop establishment
            ops += 3  # boolean check is always made and double access
            if my_array[min_idx] > my_array[j]:
                min_idx = j
                ops += 1  # assignment

        # Swap the found minimum element with
        # the first element
        my_array[i], my_array[min_idx] = my_array[min_idx], my_array[i]
        ops += 4  # double assignment and access

    return ops

def insertionSort(my_array):
    ops = 0

    # Traverse through 1 to len(my_array)
    for i in range(1, len(my_array)):
        ops += 2  # for loop establishment
        key = my_array[i]
        ops += 2  # assignment and array access

        # Move elements of my_array[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j = i - 1
        ops += 2  # assignment and maths

        while j >= 0 and key < my_array[j]:
            ops += 3  # condition checks of the loop AND an array access
            my_array[j + 1] = my_array[j]
            ops += 2  # access and assignment
            j -= 1
            ops += 2  # maths and assignment
        my_array[j + 1] = key
        ops += 1  # assignment

    return ops

def shellSort(my_array):
    ops = 0
    # Start with a big gap, then reduce the gap
    n = len(my_array)
    ops += 1  # assignment
    gap = n // 2
    ops += 2  # assignment and maths

    # Do a gapped insertion sort for this gap size.
    # The first gap elements a[0..gap-1] are already in gapped
    # order keep adding one more element until the entire array
    # is gap sorted
    while gap > 0:
        ops += 1  # loops termination check

        for i in range(gap, n):
            ops += 2  # for loop initialisation

            # add a[i] to the elements that have been gap sorted
            # save a[i] in temp and make a hole at position i
            temp = my_array[i]
            ops += 2  # assignment and array access

            # shift earlier gap-sorted elements up until the correct
            # location for a[i] is found
            j = i
            ops += 1  # assignment
            while j >= gap and my_array[j - gap] > temp:
                ops += 3  # condition checks of the loop AND an array access
                my_array[j] = my_array[j - gap]
                ops += 2  # assignment and array access
                j -= gap
                ops += 2  # assignment and maths

            # put temp (the original a[i]) in its correct location
            my_array[j] = temp
            ops += 1  # assignment
        gap //= 2
        ops += 2  # assignment and maths

    return ops

def mergeSort(my_array, ops) -> int:
    ops += 1  # condition check
    if len(my_array) > 1:
        mid = len(my_array) // 2  # Finding the mid of the array
        ops += 2  # maths
        L = my_array[:mid]  # Dividing the array elements
        ops += 2  # split and assignment
        R = my_array[mid:]  # into 2 halves
        ops += 2  # split and assignment

        ops += mergeSort(L, 0)  # Sorting the first half
        ops += mergeSort(R, 0)  # Sorting the second half

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            ops += 2  # loop condition checks
            ops += 3  # condition is always checked with 2 array accesses
            if L[i] < R[j]:
                my_array[k] = L[i]
                ops += 2  # array access and assignment
                i += 1
                ops += 2  # maths and assignment
            else:
                my_array[k] = R[j]
                ops += 2  # array access and assignment
                j += 1
                ops += 2  # maths and assignment
            k += 1
            ops += 2  # maths and assignment

        # Checking if any element was left
        while i < len(L):
            ops += 1  # loop condition check
            my_array[k] = L[i]
            ops += 2  # array access and assignment
            i += 1
            ops += 2  # maths and assignment
            k += 1
            ops += 2  # maths and assignment

        while j < len(R):
            ops += 1  # loop condition check
            my_array[k] = R[j]
            ops += 2  # array access and assignment
            j += 1
            ops += 2  # maths and assignment
            k += 1
            ops += 2  # maths and assignment

    return ops

def partition(my_array, low, high, ops):
    i = (low - 1)  # index of smaller element
    ops += 2  # maths and assignment
    pivot = my_array[high]  # pivot
    ops += 2  # assignment and access

    for j in range(low, high):
        ops += 2  # loop initialisation
        # If current element is smaller than the pivot

        ops += 1  # boolean check always made and access
        if my_array[j] < pivot:
            # increment index of smaller element
            i = i + 1
            ops += 2  # maths and assignment
            my_array[i], my_array[j] = my_array[j], my_array[i]
            ops += 4  # double assignment and access

    my_array[i + 1], my_array[high] = my_array[high], my_array[i + 1]
    ops += 4  # double assignment and access

    return (i + 1), ops

def quickSort(my_array, low, high, ops):
    ops += 1  # boolean check always made
    if low < high:

        # pi is partitioning index, my_array[p] is now
        # at right place
        pi, ops_to_add = partition(my_array, low, high, 0)
        ops += ops_to_add

        # Separately sort elements before
        # partition and after partition
        ops += quickSort(my_array, low, pi - 1, 0)
        ops += quickSort(my_array, pi + 1, high, 0)

    return ops

main()
