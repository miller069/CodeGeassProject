from data_structures.arraylist import ArrayList


class MaxHeap:
    """Max heap for leaderboard top-N queries."""

    def __init__(self, key=lambda x: x):
        self._data = ArrayList()
        self._key = key

    def __len__(self):
        return len(self._data)

    def _higher_priority(self, a, b):
        return self._key(a) > self._key(b)

    def _swap(self, i, j):
        temp = self._data[i]
        self._data[i] = self._data[j]
        self._data[j] = temp

    def insert(self, value):
        self._data.append(value)
        self._sift_up(len(self._data) - 1)

    #sifts up the last element to maintain heap property after insertion
    def _sift_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self._higher_priority(self._data[index], self._data[parent]):
                self._swap(index, parent)
                index = parent
            else:
                break
    # added sift to maintain heap property after extraction of max element
    def _sift_down(self, index):
        size = len(self._data)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            largest = index
            if left < size and self._higher_priority(self._data[left], self._data[largest]):
                largest = left
            if right < size and self._higher_priority(self._data[right], self._data[largest]):
                largest = right
            if largest != index:
                self._swap(index, largest)
                index = largest
            else:
                break
    #returns the max element 
    def peek(self):
        if len(self._data) == 0:
            return None
        return self._data[0]

    def extract_max(self):
        if len(self._data) == 0:
            return None
        maximum = self._data[0]
        last = self._data.pop()
        if len(self._data) > 0:
            self._data[0] = last
            self._sift_down(0)
        return maximum

    def copy(self):
        new_heap = MaxHeap(self._key)
        for item in self._data:
            new_heap.insert(item)
        return new_heap
