from data_structures.arraylist import ArrayList


class HashEntry:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashTable:
    def __init__(self, capacity=1024, max_load=0.75):
        self.__capacity = max(8, capacity)
        self.__buckets = ArrayList(self.__capacity)
        for _ in range(self.__capacity):
            self.__buckets.append(None)
        self.__size = 0
        self.__max_load = max_load

    def __len__(self):
        return self.__size

    def __hash(self, key):
        key = str(key)
        h = 5381
        for ch in key:
            h = ((h << 5) + h) + ord(ch)
        return h % self.__capacity

    def __load_factor(self):
        return self.__size / self.__capacity

    def __rehash(self):
        old_buckets = self.__buckets
        self.__capacity *= 2
        self.__buckets = ArrayList(self.__capacity)
        for _ in range(self.__capacity):
            self.__buckets.append(None)
        old_size = self.__size
        self.__size = 0
        for bucket in old_buckets:
            if bucket is not None:
                for entry in bucket:
                    self.insert(entry.key, entry.value)
        self.__size = old_size

    def insert(self, key, value):
        if self.__load_factor() > self.__max_load:
            self.__rehash()
        index = self.__hash(key)
        bucket = self.__buckets[index]
        if bucket is None:
            bucket = ArrayList()
            self.__buckets[index] = bucket
        for entry in bucket:
            if entry.key == key:
                entry.value = value
                return
        bucket.append(HashEntry(key, value))
        self.__size += 1

    def get(self, key, default=None):
        index = self.__hash(key)
        bucket = self.__buckets[index]
        if bucket is None:
            return default
        for entry in bucket:
            if entry.key == key:
                return entry.value
        return default

    def contains(self, key):
        sentinel = object()
        return self.get(key, sentinel) is not sentinel

    def items(self):
        for bucket in self.__buckets:
            if bucket is not None:
                for entry in bucket:
                    yield entry.key, entry.value
