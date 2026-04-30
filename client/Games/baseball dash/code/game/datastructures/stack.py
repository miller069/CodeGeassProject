"""
stack.py - Stack data structure implementation

A Last-In-First-Out (LIFO) data structure.
The last item added is the first item removed (like a stack of plates).

Author: [Your Name]
Date: [Date]
Lab: Lab 4 - Time Travel with Stacks
"""
from datastructures.array import ArrayList

class Stack:
    """
    A LIFO (Last-In-First-Out) data structure.
    
    The last item added is the first item removed.
    Think of it like a stack of plates - you add to the top and remove from the top.
    """
    
    def __init__(self):
        """
        Initialize an empty stack.
        """
        self.stack = ArrayList()
        self.stack.array = [None] * 0  
        self.stack.capacity = 0
        self.stack.size = 0 
        pass
    
    def push(self, item):
        """
        Add an item to the top of the stack.
        
        Args:
            item: The item to add to the stack
        """
        self.stack.append(item)
        pass
    
    def pop(self):
        """
        Remove and return the top item from the stack.
        
        Returns:
            The item that was on top of the stack, or None if empty
        """
        for i in range(len(self.stack.array) - 1, -1, -1):
            if self.stack.array[i] is not None:
                value = self.stack.array[i]
                self.stack.array[i] = None
                return value
        return None 
    
    def peek(self):
        """
        Return the top item without removing it.
        
        Returns:
            The item on top of the stack, or None if empty
        """
        for i in range(len(self.stack.array) - 1, -1, -1):
            if self.stack.array[i] is not None:
                return self.stack.array[i]
        return None
        
    
    def is_empty(self):
        """
        Check if the stack is empty.
        
        Returns:
            bool: True if stack is empty, False otherwise
        """
        if self.peek() == None:
            return True
        else:            
            return False
       
    
    def size(self):
        """
        Get the number of items in the stack.
        
        Returns:
            int: The number of items currently in the stack
        """
        count = 0
        for x in self.stack.array:
            if x != None:
                count += 1
        return count
    
    
    def clear(self):
        """Remove all items from the stack."""
        for i in range(len(self.stack.array)):
            self.stack.array[i] = None
    
    def __str__(self):
        """String representation of the stack (for debugging)."""
        return f"Stack({str(self.stack.array)})"