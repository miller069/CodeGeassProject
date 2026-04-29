"""
arraylist.py - Dynamic Array Implementation

Students implement a dynamic array (like Python's list) from scratch.
This will be used throughout the course in place of built-in lists.

Author: Ibrahim Chatila
Date: [Date]
Lab: Lab 3 - ArrayList and Inventory System
"""


class ArrayList:
    """
    A simple dynamic array that mimics common Python list behavior.
    Stores items in a fixed-size internal array and grows when needed.
    """

    def __init__(self, initial_capacity=10):
        """
        Create an empty ArrayList.

        Args:
            initial_capacity (int): starting capacity for the internal array.
        """
        if initial_capacity is None or initial_capacity < 1:
            initial_capacity = 10

        self._capacity = int(initial_capacity)
        self._size = 0
        self._data = [None] * self._capacity

    def __len__(self):
        """
        Return the number of stored elements.
        """
        return self._size

    def __getitem__(self, index):
        """
        Return the element at the given index (supports negative indexing).
        """
        idx = self._normalize_index(index)
        return self._data[idx]

    def __setitem__(self, index, value):
        """
        Set the element at the given index (supports negative indexing).
        """
        idx = self._normalize_index(index)
        self._data[idx] = value

    def append(self, value):
        """
        Add a value to the end of the list.
        """
        self._ensure_capacity(self._size + 1)
        self._data[self._size] = value
        self._size += 1

    def insert(self, index, value):
        """
        Insert a value before the given index.
        Like Python list.insert, index is clamped into [0, size].
        """
        if index is None:
            index = self._size

        if index < 0:
            index = 0
        if index > self._size:
            index = self._size

        self._ensure_capacity(self._size + 1)

        # Shift right to make room
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]

        self._data[index] = value
        self._size += 1

    def remove(self, value):
        """
        Remove the first occurrence of value.
        Raises ValueError if value is not found.
        """
        idx = self.index(value)  # will raise ValueError if missing

        # Shift left to fill the gap
        for i in range(idx, self._size - 1):
            self._data[i] = self._data[i + 1]

        self._data[self._size - 1] = None
        self._size -= 1

    def pop(self, index=-1):
        """
        Remove and return the element at index (default: last).
        Raises IndexError if list is empty or index out of range.
        """
        if self._size == 0:
            raise IndexError("pop from empty ArrayList")

        idx = self._normalize_index(index)
        value = self._data[idx]

        # Shift left
        for i in range(idx, self._size - 1):
            self._data[i] = self._data[i + 1]

        self._data[self._size - 1] = None
        self._size -= 1
        return value

    def clear(self):
        """
        Remove all elements from the list.
        """
        for i in range(self._size):
            self._data[i] = None
        self._size = 0

    def index(self, value):
        """
        Return the index of the first occurrence of value.
        Raises ValueError if not found.
        """
        for i in range(self._size):
            if self._data[i] == value:
                return i
        raise ValueError("ArrayList.index(x): x not in ArrayList")

    def count(self, value):
        """
        Return how many times value appears in the list.
        """
        c = 0
        for i in range(self._size):
            if self._data[i] == value:
                c += 1
        return c

    def extend(self, iterable):
        """
        Add all values from iterable to the end of the list.
        """
        for item in iterable:
            self.append(item)

    def __contains__(self, value):
        """
        Support: value in array_list
        """
        for item in self:
            if item == value:
                return True
        return False

    def __str__(self):
        """
        Return a readable string version of the list.
        """
        parts = []
        for i in range(self._size):
            parts.append(repr(self._data[i]))
        return "[" + ", ".join(parts) + "]"

    def __repr__(self):
        """
        Return a developer-friendly representation.
        """
        return f"ArrayList({str(self)})"

    def __iter__(self):
        """
        Iterate over elements in the list from index 0..size-1.
        """
        for i in range(self._size):
            yield self._data[i]

    # -----------------------
    # Helper methods
    # -----------------------

    def _ensure_capacity(self, needed):
        """
        Grow internal storage if we need more room.
        """
        if needed <= self._capacity:
            return

        new_capacity = self._capacity * 2
        while new_capacity < needed:
            new_capacity *= 2

        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]

        self._data = new_data
        self._capacity = new_capacity

    def _normalize_index(self, index):
        """
        Convert negative indexes and validate range.
        """
        if not isinstance(index, int):
            raise TypeError("ArrayList indices must be integers")

        if index < 0:
            index = self._size + index

        if index < 0 or index >= self._size:
            raise IndexError("ArrayList index out of range")

        return index
