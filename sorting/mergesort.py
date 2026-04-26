"""
sorting/mergesort.py - Stable top-down merge sort

Author: Ibrahim Chatila
Date:   2026-04-26
Project: The Arcade — ECE 3822

No sorted(), list.sort(), or collections used.
"""


class Mergesort:
    """
    Stable O(n log n) merge sort.

    Usage
    -----
        ms = Mergesort()
        sorted_list = ms.sort(data, key=lambda x: x['score'])
    """

    def sort(self, arr, key=None):
        """
        Return a new list containing the elements of arr in sorted
        (ascending) order.

        Args:
            arr : list — input data (not modified).
            key : callable or None — key function applied before comparison.

        Returns:
            list — new sorted list (stable).

        Time complexity: O(n log n)
        Space complexity: O(n)
        """
        if key is None:
            key = lambda x: x
        copy = []
        for item in arr:
            copy.append(item)
        return self.__mergesort(copy, key)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def __mergesort(self, arr, key):
        """Recursively split arr and merge sorted halves."""
        n = len(arr)
        if n <= 1:
            return arr
        mid   = n // 2
        left  = self.__mergesort(arr[:mid],  key)
        right = self.__mergesort(arr[mid:],  key)
        return self.__merge(left, right, key)

    def __merge(self, left, right, key):
        """
        Merge two sorted lists into one sorted list.

        Equal elements preserve their original relative order (stable).
        """
        result = []
        i = 0
        j = 0
        while i < len(left) and j < len(right):
            # Use <= so equal elements from left come first (stability)
            if key(left[i]) <= key(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        # Append any remaining elements
        while i < len(left):
            result.append(left[i])
            i += 1
        while j < len(right):
            result.append(right[j])
            j += 1
        return result
