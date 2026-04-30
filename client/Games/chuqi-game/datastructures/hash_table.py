"""
hash_table.py - Hash Table implementation

A dict-like mapping from keys to values using an array of buckets
and chaining for collision resolution.

Required by Graph (Lab 7) as the adjacency map.
Also used by SparseMatrix if you chose DOK (Option A) in Lab 6.

Author: Chuqi Zhang
Date:   2026-04-28
Lab:    Lab 6 - Sparse World Map
"""


class HashTable:
    """
    A hash table that supports the same interface as Python's dict.

    Internally uses an array of buckets. Each bucket holds a list of
    (key, value) pairs to handle collisions via chaining.

    Resizes when the load factor exceeds 0.75.
    """

    LOAD_FACTOR_THRESHOLD = 0.75

    def __init__(self, initial_capacity=64):
        """
        Initialize an empty hash table.

        Args:
            initial_capacity (int): Number of buckets to start with.
        """
        self.capacity = initial_capacity
        self._size = 0
        self._buckets = [[] for _ in range(self.capacity)]

    # ------------------------------------------------------------------
    # Core internals
    # ------------------------------------------------------------------

    def _hash(self, key):
        """
        Map a key to a bucket index in [0, capacity).

        Do NOT use Python's built-in hash(). Instead, compute your own:
          - For strings: combine character ordinals (e.g. polynomial rolling hash)
          - For tuples:  combine the hashes of each element
          - For ints:    a simple formula like (key * prime) % capacity works

        Args:
            key: A hashable key (str, int, tuple, …)

        Returns:
            int: Bucket index in [0, self.capacity)
        """
        FNV_OFFSET =2166136261
        FNV_PRIME = 16777619
        h = FNV_OFFSET

        if isinstance(key, tuple):
            parts = key
        else:
            parts = (key, )
        
        for part in parts:
            if isinstance(part, str):
                for ch in part:
                    h ^= ord(ch)
                    h = (h * FNV_PRIME) & 0xFFFFFFFF
            else:
                val = int(part)
                if val < 0:
                    val = val + (1 << 32)
                for _ in range(4):
                    byte = val & 0xFF
                    h ^= byte
                    h = (h * FNV_PRIME) & 0xFFFFFFFF
                    val >>= 8

        return h % self.capacity

    def _resize(self):
        """
        Double the number of buckets and rehash all existing entries.

        Called automatically by __setitem__ when load factor > 0.75.

        Steps:
          1. Save the old buckets
          2. Double self.capacity
          3. Re-initialize self._buckets with the new capacity
          4. Reset self._size to 0
          5. Re-insert every (key, value) pair from the old buckets
        """
        # TODO
        old_buckets = self._buckets
        self.capacity *= 2
        self._buckets = [[] for _ in range(self.capacity)]
        self._size = 0
        for bucket in old_buckets:
            for k, v in bucket:
                self[k] = v
    
    def _load_factor(self):
        return self._size / self.capacity

    # ------------------------------------------------------------------
    # dict-compatible interface
    # ------------------------------------------------------------------

    def __setitem__(self, key, value):
        """
        Insert or update: table[key] = value

        Steps:
          1. Hash the key to find the bucket
          2. Search the bucket for an existing entry with this key
          3. If found, update its value
          4. If not found, append (key, value) and increment _size
          5. If load factor exceeds threshold, call _resize()
        """
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self._load_factor() > self.LOAD_FACTOR_THRESHOLD:
            self._resize()

    def __getitem__(self, key):
        """
        Retrieve a value: table[key]

        Raises KeyError if the key is not present.
        """
        idx = self._hash(key)
        for k, v in self._buckets[idx]:
            if k == key:
                return v
        raise KeyError(key)

    def __delitem__(self, key):
        """
        Remove an entry: del table[key]

        Raises KeyError if the key is not present.
        """
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._size -= 1
                return
        raise KeyError(key)

    def __contains__(self, key):
        """Support: key in table"""
        idx = self._hash(key)
        for k, v in self._buckets[idx]:
            if k == key:
                return True
        return False

    def __len__(self):
        """Return the number of key-value pairs."""
        return self._size

    def __iter__(self):
        """Iterate over keys (like dict)."""
        for bucket in self._buckets:
            for k, v in bucket:
                yield k

    def get(self, key, default=None):
        """
        Return table[key] if present, otherwise default.
        Never raises KeyError.
        """
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key, *args):
        """
        Remove and return table[key].
        If key is missing and a default was provided, return it.
        If key is missing and no default, raise KeyError.
        """
        try:
            val = self[key]
            del self[key]
            return val
        except KeyError:
            if args:
                return args[0]
            raise

    def keys(self):
        """Return all keys."""
        return list(self)

    def values(self):
        """Return all values."""
        return [v for bucket in self._buckets for k, v in bucket]

    def items(self):
        """Return all (key, value) pairs."""
        result = []
        for bucket in self._buckets:
            for k, v in bucket:
                result.append((k, v))
        return result

    def clear(self):
        """Remove all entries."""
        self._buckets = [[] for _ in range(self.capacity)]
        self._size = 0

    def __str__(self):
        pairs = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return "{" + pairs + "}"

    def __repr__(self):
        return f"HashTable({self})"
