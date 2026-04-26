"""
sorting/heapsort.py - In-place max-heap sort

Author: Ibrahim Chatila
Date:   2026-04-26
Project: The Arcade — ECE 3822

No sorted(), list.sort(), heapq, or collections used.
"""


class Heapsort:
    """
    O(n log n) heap sort using a binary max-heap.

    Supports an optional key function and reverse=True for descending
    order (useful for leaderboard rankings).

    Usage
    -----
        hs = Heapsort()
        top_scores = hs.sort(data, key=lambda x: x['score'], reverse=True)
    """

    def sort(self, arr, key=None, reverse=False):
        """
        Return a new list containing elements of arr in sorted order.

        Args:
            arr     : list — input data (not modified).
            key     : callable or None — key function for comparisons.
            reverse : bool — True → descending order (default False).

        Returns:
            list — new sorted list.

        Time complexity: O(n log n)
        Space complexity: O(n)
        """
        if key is None:
            key = lambda x: x

        # Work on a copy so we never mutate the caller's list
        work = []
        for item in arr:
            work.append(item)

        n = len(work)
        if n <= 1:
            return work

        # Build max-heap
        self.__build_heap(work, key)

        # Extract elements one by one: swap root (max) with last,
        # shrink heap, sift down
        for end in range(n - 1, 0, -1):
            work[0], work[end] = work[end], work[0]
            self.__sift_down(work, 0, end, key)

        # Heapsort naturally produces ascending order.
        # If caller wants descending, reverse the result.
        if reverse:
            left  = 0
            right = n - 1
            while left < right:
                work[left], work[right] = work[right], work[left]
                left  += 1
                right -= 1

        return work

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def __build_heap(self, arr, key):
        """
        Convert arr into a max-heap in O(n) time by sifting down
        every non-leaf node from the bottom up.
        """
        n = len(arr)
        # Last non-leaf index is (n // 2) - 1
        for i in range(n // 2 - 1, -1, -1):
            self.__sift_down(arr, i, n, key)

    def __sift_down(self, arr, i, n, key):
        """
        Restore the max-heap property by sifting arr[i] downward.

        Only indices [0, n) are considered part of the active heap.

        Time complexity: O(log n)
        """
        while True:
            largest = i
            left    = 2 * i + 1
            right   = 2 * i + 2

            if left < n and key(arr[left]) > key(arr[largest]):
                largest = left
            if right < n and key(arr[right]) > key(arr[largest]):
                largest = right

            if largest == i:
                break   # heap property satisfied

            arr[i], arr[largest] = arr[largest], arr[i]
            i = largest
