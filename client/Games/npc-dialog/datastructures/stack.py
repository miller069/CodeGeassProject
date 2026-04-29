"""
stack.py - Stack data structure implementation

A Last-In-First-Out (LIFO) data structure.
The last item added is the first item removed (like a stack of plates).

Lab 4 - Time Travel with Stacks
"""

from datastructures.array import ArrayList


class Stack:
    """
    A LIFO (Last-In-First-Out) data structure.
    """

    def __init__(self):
        """Initialize an empty stack."""
        self._data = ArrayList()

    def push(self, item):
        """
        Add an item to the top of the stack.
        """
        self._data.append(item)

    def pop(self):
        """
        Remove and return the top item.
        Returns None if stack is empty.
        """
        if self.is_empty():
            return None
        return self._data.pop()

    def peek(self):
        """
        Return the top item without removing it.
        Returns None if stack is empty.
        """
        if self.is_empty():
            return None
        return self._data[len(self._data) - 1]

    def is_empty(self):
        """Return True if stack is empty."""
        return len(self._data) == 0

    def size(self):
        """Return number of items in stack."""
        return len(self._data)

    def clear(self):
        """Remove all items from stack."""
        self._data.clear()

    def __str__(self):
        """String representation for debugging."""
        return f"Stack({[self._data[i] for i in range(len(self._data))]})"
