"""
arraylist.py - Dynamic Array Implementation

Students implement a dynamic array (like Python's list) from scratch.
This will be used throughout the course in place of built-in lists.

Author: Nicholas Waller
Date: 2/9/2026
Lab: Lab 3 - ArrayList and Inventory System
"""

class ArrayList:
    """
    Implement the methods discussed here: 
    https://docs.python.org/3/tutorial/datastructures.html#more-on-lists
    """
    
    def __init__(self, initial_capacity=10):
        """ Iniitializes an array with a default capacity of 10.
        """
        # TODO: Initialize instance variables
        self.array = [None] * initial_capacity
        self.capacity = initial_capacity
        self.size = 0
        pass
    
    # Returns the number of elements when you call len(my_array)
    def __len__(self):
        """ return the number of elements inside of the array
        """
        # TODO: Return the size
        i = len(self.array) - 1
        for i in range(len(self.array)):
            if self.array[i] is not None:
                self.size += 1
        return self.size
    
    # Enables bracket notation for accessing elements: my_array[3]
    def __getitem__(self, index):
        """ returns an item at a given position in the array 
        """
        # TODO: Return element at index
        if index < 0 or index >= self.capacity:
            return False
        return self.array[index]
    
    # Enables bracket notation for setting elements: my_array[3] = 42
    def __setitem__(self, index, value):
        """ sets an item at a given position in the array
        """
        # TODO: Set element at index
        self.array[index] = value
        pass
    
    def append(self, value):
        """ adds an item to the end of the array. if the array is full the function will increase its size by 1.
        """
        
        
        if len(self.array) >= self.capacity:
            self.capacity += 1
            new_array = [None] * self.capacity
            for i in range(self.capacity - 1):
                new_array[i] = self.array[i]
                
            self.array = new_array

        for i in range(len(self.array)):
            if self.array[i] is None:
                self.array[i] = value
                
        return self.array
    
    def insert(self, index, value):
        """inserts and item at a given position in the array. All items will be shifted up one. if the array is full the function will increase its size by 1.
        """
        push = index + 1
        if len(self.array) >= self.capacity:
            self.capacity += 1
            new_array = [None] * self.capacity
            for i in range(self.capacity - 1):
                new_array[i] = self.array[i]
                
            self.array = new_array
        for i in range(self.capacity - 1, index, -1):
            self.array[i] = self.array[i - 1]

        self.array[index] = value
        pass
    
    def remove(self, value):
        """ removes a value from the array
        """
        idx = self.index(value)  

        for i in range(idx, len(self.array) - 1):
            self.array[i] = self.array[i + 1]

        self.capacity -= 1
        new_array = [None] * self.capacity
        for i in range(self.capacity - 1):
                new_array[i] = self.array[i]
                
        self.array = new_array

        pass
    
    def pop(self, index=-1):
        """ removes the first item in the array and decreases the size of the array by 1.
        """

        for i in range(index, self.size - 1):
            self.array[i] = self.array[i + 1]

        self.array[self.capacity - 1] = None
        pass
    
    def clear(self):
        """ clears the array of all items
        """
        for i in range(self.capacity):
            self.array[i] = None

        self.capacity = 0
        pass
    
    def index(self, value):
        """ returns the location of an item in the array
        """
        for i in range(self.capacity):
            if self.array[i] == value:
                return i
        
        
        

    def count(self, value):
        """ counts the number of times a value appears in the array
        """
        c = 0
        for i in range(self.capacity):
            if self.array[i] == value:
                c += 1
        return c
        

    def extend(self, iterable):
        """ adds all items from a list to the end of the array
        """
        for item in iterable:
            self.append(item)
        pass
    
    # Makes the "in" operator work: if 5 in my_array:
    def __contains__(self, value):
        """ returns true if a value is in the array and false otherwise
        """
        for i in range(self.capacity):
            if self.array[i] == value:
                return True
        return False
    
    # Returns a user-friendly string representation when you call str(my_array) or print(my_array)
    def __str__(self):
        """ returns a string representation of the array
        """
        return f"ArrayList({str(self.array)})"
        
    
    # Returns a developer-friendly string representation (often the same as __str__ for simple classes), 
    # used in the interactive shell
    def __repr__(self):
        """ returns a string representation of the array
        """
        return f"ArrayList({str(self.array)})"
    
    # Makes the list iterable so you can use it in for loops: for item in my_array:
    def __iter__(self):
        for i in range(self.capacity):
            if self.array[i] is not None:
                yield self.array[i]

        
    def get_capacity(self):
        """ returns the capacity of the array
       
        """
        return len(self.array)