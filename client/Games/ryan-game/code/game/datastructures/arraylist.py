"""
arraylist.py - Dynamic Array Implementation

Students implement a dynamic array (like Python's list) from scratch.
This will be used throughout the course in place of built-in lists.

Author: Ryan Miller
Date: 2/11
Lab: Lab 3 - ArrayList and Inventory System
"""

class ArrayList:
    """
    Implement the methods discussed here: 
    https://docs.python.org/3/tutorial/datastructures.html#more-on-lists
    """
    
    def __init__(self, initial_capacity=10):
        """
        """
        if not isinstance(initial_capacity, int):
            raise TypeError("initial_capacity must be an int")
        if initial_capacity <= 0:
            raise ValueError("initial_capacity must be > 0")

        self._capacity = initial_capacity
        self._size = 0
        self._data = [None] * self._capacity
    
    # Returns the number of elements when you call len(my_array)
    def __len__(self):
        """
        """
        return self._size
    
    # Enables bracket notation for accessing elements: my_array[3]
    def __getitem__(self, index):
        """
        """
        if not isinstance(index, int):
            raise TypeError("index must be an int")

        if index < 0:
            index += self._size

        if index < 0 or index >= self._size:
            raise IndexError("ArrayList index out of range")

        return self._data[index]
    
    # Enables bracket notation for setting elements: my_array[3] = 42
    def __setitem__(self, index, value):
        """
        """
        if not isinstance(index, int):
            raise TypeError("index must be an int")

        if index < 0:
            index += self._size

        if index < 0 or index >= self._size:
            raise IndexError("ArrayList assignment index out of range")

        self._data[index] = value
    
    def _resize(self, new_capacity):
        if new_capacity < self._size:
            new_capacity = self._size
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity
    
    def append(self, value):
        """
        """
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        self._data[self._size] = value
        self._size += 1
    
    def insert(self, index, value):
        """
        """
        if not isinstance(index, int):
            raise TypeError("index must be an int")

        if index < 0:
            index += self._size

        if index < 0:
            index = 0
        if index > self._size:
            index = self._size

        if self._size == self._capacity:
            self._resize(self._capacity * 2)

        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]

        self._data[index] = value
        self._size += 1
    
    def remove(self, value):
        """
        """
        idx = self.index(value)
        for i in range(idx, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._data[self._size - 1] = None
        self._size -= 1
    
    def pop(self, index=-1):
        """
        """
        if not isinstance(index, int):
            raise TypeError("index must be an int")

        if self._size == 0:
            raise IndexError("pop from empty ArrayList")

        if index < 0:
            index += self._size

        if index < 0 or index >= self._size:
            raise IndexError("pop index out of range")

        value = self._data[index]
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._data[self._size - 1] = None
        self._size -= 1
        return value
    
    def clear(self):
        """
        """
        for i in range(self._size):
            self._data[i] = None
        self._size = 0
    
    def index(self, value):
        """
        """
        for i in range(self._size):
            if self._data[i] == value:
                return i
        raise ValueError("value not in ArrayList")

    def count(self, value):
        """
        """
        c = 0
        for i in range(self._size):
            if self._data[i] == value:
                c += 1
        return c

    def extend(self, iterable):
        """
        """
        for item in iterable:
            self.append(item)
    
    # Makes the "in" operator work: if 5 in my_array:
    def __contains__(self, value):
        """
        """
        for i in range(self._size):
            if self._data[i] == value:
                return True
        return False
    
    # Returns a user-friendly string representation when you call str(my_array) or print(my_array)
    def __str__(self):
        """
        """
        return "[" + ", ".join(str(self._data[i]) for i in range(self._size)) + "]"
    
    # Returns a developer-friendly string representation (often the same as __str__ for simple classes), 
    # used in the interactive shell
    def __repr__(self):
        """
        """
        return str(self)
    
    # Makes the list iterable so you can use it in for loops: for item in my_array:
    def __iter__(self):
        """
        """
        for i in range(self._size):
            yield self._data[i]
