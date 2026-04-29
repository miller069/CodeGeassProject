"""
sparse_matrix.py - Sparse Matrix implementation (Option B: COO)

Backing store: ArrayList of (row, col, value) triples.
Only non-default entries are stored, saving memory for tile maps
where most cells share the same value (-1 = empty).

No Python built-in list, dict, or set is used inside this class.

Author: Ibrahim Chatila
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
# COO (Coordinate List) implementation
# =============================================================================

class SparseMatrix(SparseMatrixBase):
    """
    COO sparse matrix backed by ArrayList.

    Each non-default entry is stored as a (row, col, value) tuple
    inside a single ArrayList.  All other positions return self.default.

    Complexity:
      get / set : O(nnz)  — linear scan over stored entries
      items     : O(nnz)
      multiply  : O(nnz_A * nnz_B)
    """

    def __init__(self, rows=None, cols=None, default=0):
        super().__init__(rows, cols, default)
        # ArrayList of (row, col, value) tuples — no built-in list/dict/set
        self._entries = ArrayList()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _find_index(self, row, col):
        """
        Return the ArrayList index of the entry for (row, col),
        or -1 if no such entry exists.
        """
        for i in range(len(self._entries)):
            r, c, _ = self._entries[i]
            if r == row and c == col:
                return i
        return -1

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def set(self, row, col, value):
        """
        Store value at (row, col).
        If value == default, remove the entry (keeps the matrix sparse).
        """
        idx = self._find_index(row, col)

        if value == self.default:
            # Remove existing entry so default positions stay absent
            if idx >= 0:
                self._entries.pop(idx)
        else:
            if idx >= 0:
                # Overwrite existing entry
                self._entries[idx] = (row, col, value)
            else:
                # New entry
                self._entries.append((row, col, value))

    def get(self, row, col):
        """
        Return the stored value at (row, col), or default if absent.
        """
        idx = self._find_index(row, col)
        if idx >= 0:
            _, _, value = self._entries[idx]
            return value
        return self.default

    def items(self):
        """
        Yield ((row, col), value) for every stored (non-default) entry.
        """
        for i in range(len(self._entries)):
            r, c, v = self._entries[i]
            yield (r, c), v

    def __len__(self):
        """Return the number of stored (non-default) entries."""
        return len(self._entries)

    def multiply(self, other):
        """
        Return a new SparseMatrix equal to self * other.

        Standard matrix multiplication:
            result[r, c] = sum over k of self[r, k] * other[k, c]

        Only iterates over non-default entries in both matrices.
        """
        result = SparseMatrix(self.rows, other.cols, self.default)

        for i in range(len(self._entries)):
            r, k, v = self._entries[i]

            for j in range(len(other._entries)):
                k2, c, v2 = other._entries[j]

                if k == k2:
                    current = result.get(r, c)
                    result.set(r, c, current + v * v2)

        return result

    def __str__(self):
        """Human-readable summary."""
        return (
            f"SparseMatrix({self.rows}x{self.cols}, "
            f"{len(self)} stored entries, "
            f"default={self.default})"
        )
