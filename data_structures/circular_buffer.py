"""
Fixed-size circular buffer. When full, the oldest item gets overwritten.

Author: Ibrahim Chatila
Date: 2026-04-26
"""

from data_structures.array_list import ArrayList


class CircularBuffer:

    def __init__(self, capacity):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.__capacity = capacity
        self.__buf      = [None] * capacity
        self.__head     = 0
        self.__tail     = 0
        self.__size     = 0

    def push(self, item):
        self.__buf[self.__tail] = item
        self.__tail = self.__advance(self.__tail)
        if self.__size == self.__capacity:
            # buffer was full so the oldest entry was just overwritten
            self.__head = self.__advance(self.__head)
        else:
            self.__size += 1

    def get_recent(self, n):
        """Return up to n most recent items in chronological order."""
        count = n if n < self.__size else self.__size
        result = ArrayList()
        start = (self.__tail - count) % self.__capacity
        for i in range(count):
            result.append(self.__buf[(start + i) % self.__capacity])
        return result

    def is_full(self):
        return self.__size == self.__capacity

    def is_empty(self):
        return self.__size == 0

    def size(self):
        return self.__size

    def __advance(self, ptr):
        return (ptr + 1) % self.__capacity
