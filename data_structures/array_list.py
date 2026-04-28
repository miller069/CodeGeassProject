"""
ArrayList implementation for ECE 3822.
Replaces Python's built-in list throughout the project.

Author: Ibrahim Chatila
Date: 2026-04-26
"""


class ArrayList:
    """Dynamic array that doubles in size when it runs out of space."""

    def __init__(self, initial_capacity=10):
        if initial_capacity is None or initial_capacity < 1:
            initial_capacity = 10

        self._capacity = int(initial_capacity)
        self._size = 0
        self._data = [None] * self._capacity

    def __len__(self):
        return self._size

    def __getitem__(self, index):
        idx = self._normalize_index(index)
        return self._data[idx]

    def __setitem__(self, index, value):
        idx = self._normalize_index(index)
        self._data[idx] = value

    def append(self, value):
        self._ensure_capacity(self._size + 1)
        self._data[self._size] = value
        self._size += 1

    def insert(self, index, value):
        if index is None:
            index = self._size
        if index < 0:
            index = 0
        if index > self._size:
            index = self._size

        self._ensure_capacity(self._size + 1)

        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]

        self._data[index] = value
        self._size += 1

    def remove(self, value):
        """Remove the first occurrence of value. Raises ValueError if not found."""
        idx = self.index(value)

        for i in range(idx, self._size - 1):
            self._data[i] = self._data[i + 1]

        self._data[self._size - 1] = None
        self._size -= 1

    def pop(self, index=-1):
        if self._size == 0:
            raise IndexError("pop from empty ArrayList")

        idx = self._normalize_index(index)
        value = self._data[idx]

        for i in range(idx, self._size - 1):
            self._data[i] = self._data[i + 1]

        self._data[self._size - 1] = None
        self._size -= 1
        return value

    def clear(self):
        for i in range(self._size):
            self._data[i] = None
        self._size = 0

    def index(self, value):
        for i in range(self._size):
            if self._data[i] == value:
                return i
        raise ValueError("ArrayList.index(x): x not in ArrayList")

    def count(self, value):
        c = 0
        for i in range(self._size):
            if self._data[i] == value:
                c += 1
        return c

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def __contains__(self, value):
        for item in self:
            if item == value:
                return True
        return False

    def __str__(self):
        result = ""
        for i in range(self._size):
            if i > 0:
                result += ", "
            result += repr(self._data[i])
        return "[" + result + "]"

    def __repr__(self):
        return f"ArrayList({str(self)})"

    def __iter__(self):
        for i in range(self._size):
            yield self._data[i]

    def _ensure_capacity(self, needed):
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
        if not isinstance(index, int):
            raise TypeError("ArrayList indices must be integers")

        if index < 0:
            index = self._size + index

        if index < 0 or index >= self._size:
            raise IndexError("ArrayList index out of range")

        return index
