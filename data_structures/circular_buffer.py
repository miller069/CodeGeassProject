"""
data_structures/circular_buffer.py - Fixed-size circular (ring) buffer

Author: Ibrahim Chatila
Date:   2026-04-26
Project: The Arcade — ECE 3822
"""


class CircularBuffer:
    """
    A fixed-capacity circular buffer (ring buffer).

    When the buffer is full, the oldest entry is silently overwritten
    by the newest push.  get_recent(n) always returns items in
    chronological order (oldest first).
    """

    def __init__(self, capacity):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.__capacity = capacity
        self.__buf      = [None] * capacity
        self.__head     = 0     # index of the oldest item
        self.__tail     = 0     # index of the next write position
        self.__size     = 0

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def push(self, item):
        """
        Write item at __tail and advance __tail.

        If the buffer is already full, __head advances too so the
        oldest entry is overwritten.

        Time complexity: O(1)
        """
        self.__buf[self.__tail] = item
        self.__tail = self.__advance(self.__tail)
        if self.__size == self.__capacity:
            # Full — oldest entry has been overwritten; move head forward
            self.__head = self.__advance(self.__head)
        else:
            self.__size += 1

    def get_recent(self, n):
        """
        Return the n most recent items in chronological order
        (oldest of the n first, newest last).

        If fewer than n items are stored, return all of them.

        Time complexity: O(min(n, size))
        """
        count = n if n < self.__size else self.__size
        result = []
        # Start from (tail - count) positions back, wrapping around
        start = (self.__tail - count) % self.__capacity
        for i in range(count):
            result.append(self.__buf[(start + i) % self.__capacity])
        return result

    def is_full(self):
        """Return True if the buffer has reached capacity."""
        return self.__size == self.__capacity

    def is_empty(self):
        """Return True if no items have been pushed."""
        return self.__size == 0

    def size(self):
        """Return the current number of items stored."""
        return self.__size

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def __advance(self, ptr):
        """Return (ptr + 1) % __capacity."""
        return (ptr + 1) % self.__capacity
