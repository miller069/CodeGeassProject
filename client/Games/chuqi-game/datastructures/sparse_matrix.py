"""
sparse_matrix.py - Sparse Matrix implementation

A sparse matrix stores only non-default entries, saving memory when most
cells share the same value (like -1 in a tile map).

Choose one of three backing representations:

  Option A — DOK (Dictionary of Keys): {(row, col): value}
    Requires implementing HashTable in hash_table.py.
    Do not use Python's built-in dict or set.

  Option B — COO (Coordinate List): list of (row, col, value) triples
    Use your ArrayList from Lab 3. Do not use Python's built-in list.

  Option C — CSR (Compressed Sparse Row): three parallel arrays
    row_ptr, col_idx, values. Most efficient for row-wise access.

All three options must satisfy the same interface.

Author: [Your Name]
Date:   [Date]
Lab:    Lab 6 - Sparse World Map
"""

from datastructures.array import ArrayList

# =============================================================================
# Do not modify SparseMatrixBase.
# =============================================================================

class SparseMatrixBase:
    """Interface definition. Your SparseMatrix must inherit from this."""

    def __init__(self, rows=None, cols=None, default=0):
        self.rows    = rows
        self.cols    = cols
        self.default = default

    def set(self, row, col, value):
        raise NotImplementedError

    def get(self, row, col):
        raise NotImplementedError

    def items(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def multiply(self, other):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


# =============================================================================
# Your implementation goes here.
# =============================================================================

class SparseMatrix(SparseMatrixBase):

    def __init__(self, rows=None, cols=None, default=0):
        super().__init__(rows, cols, default)
        self._data = ArrayList()

    def _find_index(self, row, col):
        for i in range(len(self._data)):
            entry = self._data[i]
            if entry[0] == row and entry[1] == col:
                return i
        return None

    def set(self, row, col, value):
        idx = self._find_index(row, col)
        if value == self.default:
            if idx is not None:
                self._data.pop(idx)
            return
        if idx is not None:
            self._data[idx] = (row, col, value)
        else:
            self._data.append((row, col, value))

    def get(self, row, col):
        idx = self._find_index(row, col)
        if idx is not None:
            return self._data[idx][2]
        return self.default

    def items(self):
        for i in range(len(self._data)):
            entry = self._data[i]
            yield ((entry[0], entry[1]), entry[2])

    def __len__(self):
        return len(self._data)

    def multiply(self, other):
        result = SparseMatrix(rows=self.rows, cols=other.cols, default=0)
        for (i, k), v1 in self.items():
            for (k2, j), v2 in other.items():
                if k == k2:
                    current = result.get(i, j)
                    result.set(i, j, current + v1 * v2)
        return result

    def __str__(self):
        return (f"SparseMatrix(rows={self.rows}, cols={self.cols}, "
                f"default={self.default}, entries={len(self)})")
