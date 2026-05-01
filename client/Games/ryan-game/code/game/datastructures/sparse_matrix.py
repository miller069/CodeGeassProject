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

try:
    from .arraylist import ArrayList
except ImportError:
    from arraylist import ArrayList


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
        self.entries = ArrayList()

    def set(self, row, col, value):
        for i in range(len(self.entries)):
            r, c, v = self.entries[i]
            if r == row and c == col:
                if value == self.default:
                    self.entries.pop(i)
                else:
                    self.entries[i] = (row, col, value)
                return

        if value != self.default:
            self.entries.append((row, col, value))

    def get(self, row, col):
        for r, c, v in self.entries:
            if r == row and c == col:
                return v
        return self.default

    def items(self):
        for r, c, v in self.entries:
            yield ((r, c), v)

    def __len__(self):
        return len(self.entries)

    def multiply(self, other):
        result = SparseMatrix(self.rows, other.cols, self.default)

        for r1, c1, v1 in self.entries:
            for r2, c2, v2 in other.entries:
                if c1 == r2:
                    current = result.get(r1, c2)
                    if current == result.default:
                        current = 0
                    result.set(r1, c2, current + (v1 * v2))

        return result

    def __str__(self):
        return f"SparseMatrix(rows={self.rows}, cols={self.cols}, default={self.default}, stored={len(self)})"