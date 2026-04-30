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

from datastructures.hash_table import HashTable


class SparseMatrix(SparseMatrixBase):

    def __init__(self, rows=None, cols=None, default=0):
        super().__init__(rows, cols, default)
        # TODO: initialize your backing data structure
        self.data = HashTable()

    def set(self, row, col, value):
        # TODO
        if row < 0 or col < 0:
            raise IndexError

        if self.rows is not None and row >= self.rows:
            raise IndexError
        if self.cols is not None and col >= self.cols:
            raise IndexError

        key = (row, col)

        if value == self.default:
            if key in self.data:
                del self.data[key]
        else:
            self.data[key] = value

    def get(self, row, col):
        # TODO
        if row < 0 or col < 0:
            raise IndexError

        if self.rows is not None and row >= self.rows:
            raise IndexError
        if self.cols is not None and col >= self.cols:
            raise IndexError

        return self.data.get((row, col), self.default)

    def items(self):
        # TODO
        return self.data.items()

    def __len__(self):
        # TODO
        return len(self.data)

    def multiply(self, other):
        # TODO
        if self.cols != other.rows:
            raise ValueError

        result = SparseMatrix(self.rows, other.cols, self.default)

        for (r1, c1), v1 in self.items():
            for (r2, c2), v2 in other.items():
                if c1 == r2:
                    current = result.get(r1, c2)
                    result.set(r1, c2, current + v1 * v2)

        return result

    def __str__(self):
        # TODO
        if self.rows is None or self.cols is None:
            return str(self.data)

        output = ""

        for r in range(self.rows):
            row_vals = []
            for c in range(self.cols):
                row_vals.append(str(self.get(r, c)))
            output += " ".join(row_vals)
            if r != self.rows - 1:
                output += "\n"

        return output