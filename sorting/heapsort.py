"""
Max-heap sort using ArrayList.
Supports a key function and reverse=True for descending order.

Author: Ibrahim Chatila
Date: 2026-04-26
"""

from data_structures.array_list import ArrayList


class Heapsort:

    def sort(self, arr, key=None, reverse=False):
        """Return a new sorted ArrayList. Use reverse=True for descending order."""
        if key is None:
            key = lambda x: x

        work = ArrayList()
        for item in arr:
            work.append(item)

        n = len(work)
        if n <= 1:
            return work

        self.__build_heap(work, key)

        for end in range(n - 1, 0, -1):
            tmp       = work[0]
            work[0]   = work[end]
            work[end] = tmp
            self.__sift_down(work, 0, end, key)

        if reverse:
            left  = 0
            right = n - 1
            while left < right:
                tmp         = work[left]
                work[left]  = work[right]
                work[right] = tmp
                left  += 1
                right -= 1

        return work

    def __build_heap(self, arr, key):
        n = len(arr)
        for i in range(n // 2 - 1, -1, -1):
            self.__sift_down(arr, i, n, key)

    def __sift_down(self, arr, i, n, key):
        while True:
            largest = i
            left    = 2 * i + 1
            right   = 2 * i + 2

            if left < n and key(arr[left]) > key(arr[largest]):
                largest = left
            if right < n and key(arr[right]) > key(arr[largest]):
                largest = right

            if largest == i:
                break

            tmp          = arr[i]
            arr[i]       = arr[largest]
            arr[largest] = tmp
            i = largest
