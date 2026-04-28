"""
Stable top-down merge sort using ArrayList.
No built-in sort functions used.

Author: Ibrahim Chatila
Date: 2026-04-26
"""

from data_structures.array_list import ArrayList


class Mergesort:

    def sort(self, arr, key=None):
        """Return a new sorted ArrayList. Original is not modified."""
        if key is None:
            key = lambda x: x

        copy = ArrayList()
        for item in arr:
            copy.append(item)

        return self.__mergesort(copy, key)

    def __mergesort(self, arr, key):
        n = len(arr)
        if n <= 1:
            return arr

        mid = n // 2

        left  = ArrayList()
        right = ArrayList()
        for i in range(mid):
            left.append(arr[i])
        for i in range(mid, n):
            right.append(arr[i])

        left  = self.__mergesort(left,  key)
        right = self.__mergesort(right, key)
        return self.__merge(left, right, key)

    def __merge(self, left, right, key):
        result = ArrayList()
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            if key(left[i]) <= key(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        while i < len(left):
            result.append(left[i])
            i += 1

        while j < len(right):
            result.append(right[j])
            j += 1

        return result
