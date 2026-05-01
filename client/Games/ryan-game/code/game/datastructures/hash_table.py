"""
hash_table.py - Hash Table implementation

Only required if you implement SparseMatrix using DOK (Option A).

Author: Ryan Miller
Date:   [Date]
Lab:    Lab 6 - Sparse World Map
"""


class HashTable:

    def __init__(self, initial_capacity=64):
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [None] * self.capacity

    def _hash(self, key):
        key_string = str(key)
        total = 0

        for char in key_string:
            total = (total * 31 + ord(char)) % self.capacity

        return total

    def set(self, key, value):
        index = self._hash(key)

        if self.buckets[index] is None:
            self.buckets[index] = []

        bucket = self.buckets[index]

        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.size += 1

        if self.size / self.capacity > 0.7:
            self._resize()

    def get(self, key, default=None):
        index = self._hash(key)
        bucket = self.buckets[index]

        if bucket is None:
            return default

        for item in bucket:
            if item[0] == key:
                return item[1]

        return default

    def delete(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]

        if bucket is None:
            return False

        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket.pop(i)
                self.size -= 1
                return True

        return False

    def __contains__(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]

        if bucket is None:
            return False

        for item in bucket:
            if item[0] == key:
                return True

        return False

    def __len__(self):
        return self.size

    def items(self):
        all_items = []

        for bucket in self.buckets:
            if bucket is not None:
                for item in bucket:
                    all_items.append(item)

        return all_items

    def _resize(self):
        old_buckets = self.buckets

        self.capacity *= 2
        self.size = 0
        self.buckets = [None] * self.capacity

        for bucket in old_buckets:
            if bucket is not None:
                for key, value in bucket:
                    self.set(key, value)