"""
hash_table.py - Hash Table with separate chaining

Used by SparseMatrix Option A (DOK).

Collisions are resolved with chaining: each bucket holds an ArrayList
of (key, value) pairs.  No Python dict or set is used anywhere.

_hash() uses a custom polynomial hash — Python's built-in hash() is
never called.

Author: Ibrahim Chatila
Date:   [Date]
Lab:    Lab 6 - Sparse World Map
"""

from datastructures.array import ArrayList


class HashTable:
    """
    Hash table with separate chaining (ArrayList per bucket).

    Resizes (doubles capacity + rehash) when load factor exceeds 0.7.
    Keys can be any hashable type; tuples like (row, col) are supported.
    """

    # Load-factor threshold that triggers a resize
    _MAX_LOAD = 0.7

    def __init__(self, initial_capacity=64):
        self.capacity = initial_capacity
        self._size    = 0
        # Fixed-size array of buckets; each bucket is None or an ArrayList
        # of (key, value) tuples.  Using a raw Python list here mirrors how
        # ArrayList itself stores its internal array — it is the underlying
        # fixed-size store, not a high-level data structure.
        self._buckets = [None] * self.capacity

    # ------------------------------------------------------------------
    # Hash function — no call to Python's hash()
    # ------------------------------------------------------------------

    def _hash(self, key):
        """
        Custom polynomial hash.

        Handles int, str, and tuple keys without calling hash().
        Uses the djb2-style algorithm: h = h * 31 + next_value.
        """
        h = 17  # non-zero seed

        if isinstance(key, int):
            # Knuth multiplicative: spread integers across the table
            h = key * 2_654_435_769
        elif isinstance(key, str):
            for ch in key:
                h = h * 31 + ord(ch)
        elif isinstance(key, tuple):
            for item in key:
                if isinstance(item, int):
                    h = h * 31 + item
                elif isinstance(item, str):
                    for ch in item:
                        h = h * 31 + ord(ch)
                else:
                    for ch in str(item):
                        h = h * 31 + ord(ch)
        else:
            # Fallback: stringify
            for ch in str(key):
                h = h * 31 + ord(ch)

        return abs(h) % self.capacity

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def set(self, key, value):
        """Insert or update key → value.  Resizes if load factor > 0.7."""
        if (self._size + 1) / self.capacity > self._MAX_LOAD:
            self._resize()

        idx = self._hash(key)

        if self._buckets[idx] is None:
            self._buckets[idx] = ArrayList()

        bucket = self._buckets[idx]

        # Check for existing key — update in place
        for i in range(len(bucket)):
            k, _ = bucket[i]
            if k == key:
                bucket[i] = (key, value)
                return

        # New key
        bucket.append((key, value))
        self._size += 1

    def get(self, key, default=None):
        """Return value for key, or default if absent."""
        idx = self._hash(key)
        bucket = self._buckets[idx]

        if bucket is None:
            return default

        for i in range(len(bucket)):
            k, v = bucket[i]
            if k == key:
                return v

        return default

    def delete(self, key):
        """Remove key.  Raises KeyError if key is not present."""
        idx = self._hash(key)
        bucket = self._buckets[idx]

        if bucket is not None:
            for i in range(len(bucket)):
                k, _ = bucket[i]
                if k == key:
                    bucket.pop(i)
                    self._size -= 1
                    return

        raise KeyError(key)

    def __contains__(self, key):
        """Support: key in ht"""
        idx = self._hash(key)
        bucket = self._buckets[idx]

        if bucket is None:
            return False

        for i in range(len(bucket)):
            k, _ = bucket[i]
            if k == key:
                return True

        return False

    def __len__(self):
        """Return the number of stored entries."""
        return self._size

    def items(self):
        """Yield (key, value) for every stored entry."""
        for bucket in self._buckets:
            if bucket is not None:
                for i in range(len(bucket)):
                    yield bucket[i]

    # ------------------------------------------------------------------
    # Resize / rehash
    # ------------------------------------------------------------------

    def _resize(self):
        """Double capacity and rehash all existing entries."""
        old_buckets  = self._buckets
        self.capacity = self.capacity * 2
        self._buckets = [None] * self.capacity
        self._size    = 0          # set() will re-increment

        for bucket in old_buckets:
            if bucket is not None:
                for i in range(len(bucket)):
                    k, v = bucket[i]
                    self.set(k, v)

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __setitem__(self, key, value):
        self.set(key, value)

    def __getitem__(self, key):
        idx = self._hash(key)
        bucket = self._buckets[idx]
        if bucket is not None:
            for i in range(len(bucket)):
                k, v = bucket[i]
                if k == key:
                    return v
        raise KeyError(key)

    def __delitem__(self, key):
        self.delete(key)

    def __iter__(self):
        for bucket in self._buckets:
            if bucket is not None:
                for i in range(len(bucket)):
                    yield bucket[i][0]

    def __str__(self):
        return f"HashTable(capacity={self.capacity}, size={self._size})"
