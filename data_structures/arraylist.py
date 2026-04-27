

class ArrayList:
    """A small dynamic array used instead of Python's built-in list in project code."""

    def __init__(self, initial_capacity=10):
        if initial_capacity <= 0:
            initial_capacity = 1
        self.array = [None] * initial_capacity
        self.capacity = initial_capacity
        self.size = 0

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        if index < 0:
            index = self.size + index
        if index < 0 or index >= self.size:
            raise IndexError("ArrayList index out of range")
        return self.array[index]

    def __setitem__(self, index, value):
        if index < 0:
            index = self.size + index
        if index < 0 or index >= self.size:
            raise IndexError("ArrayList index out of range")
        self.array[index] = value

    def _resize(self, new_capacity):
        if new_capacity < 1:
            new_capacity = 1
        new_array = [None] * new_capacity
        for i in range(self.size):
            new_array[i] = self.array[i]
        self.array = new_array
        self.capacity = new_capacity

    def append(self, value):
        if self.size >= self.capacity:
            self._resize(self.capacity * 2)
        self.array[self.size] = value
        self.size += 1
        return self

    def insert(self, index, value):
        if index < 0:
            index = self.size + index
        if index < 0:
            index = 0
        if index > self.size:
            index = self.size
        if self.size >= self.capacity:
            self._resize(self.capacity * 2)
        for i in range(self.size, index, -1):
            self.array[i] = self.array[i - 1]
        self.array[index] = value
        self.size += 1

    def remove(self, value):
        idx = self.index(value)
        if idx == -1:
            return False
        self.pop(idx)
        return True

    def pop(self, index=-1):
        if self.size == 0:
            raise IndexError("pop from empty ArrayList")
        if index < 0:
            index = self.size + index
        if index < 0 or index >= self.size:
            raise IndexError("ArrayList index out of range")
        value = self.array[index]
        for i in range(index, self.size - 1):
            self.array[i] = self.array[i + 1]
        self.array[self.size - 1] = None
        self.size -= 1
        if self.capacity > 10 and self.size <= self.capacity // 4:
            self._resize(self.capacity // 2)
        return value

    def clear(self):
        for i in range(self.capacity):
            self.array[i] = None
        self.size = 0

    def index(self, value):
        for i in range(self.size):
            if self.array[i] == value:
                return i
        return -1

    def count(self, value):
        c = 0
        for i in range(self.size):
            if self.array[i] == value:
                c += 1
        return c

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def __contains__(self, value):
        return self.index(value) != -1

    def __iter__(self):
        for i in range(self.size):
            yield self.array[i]

    def get_capacity(self):
        return self.capacity

    def to_list(self):
        return [self.array[i] for i in range(self.size)]

    def __str__(self):
        return "ArrayList(" + str(self.to_list()) + ")"

    def __repr__(self):
        return self.__str__()
