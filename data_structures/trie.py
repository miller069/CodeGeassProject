"""
data_structures/trie.py - Trie for fast username prefix search

Author: Ibrahim Chatila
Date:   2026-04-26
Project: The Arcade — ECE 3822
"""

from data_structures.node import TrieNode


class Trie:
    """
    Character-level trie that maps usernames → player_ids.

    Supports O(m) insert and lookup (m = username length) and
    O(m + k) prefix search (k = number of matches).
    """

    def __init__(self):
        self.__root = TrieNode()
        self.__size = 0             # number of complete usernames stored

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def insert(self, username, player_id):
        """
        Insert username into the trie and associate it with player_id.

        If the username already exists, its player_id is updated.

        Time complexity: O(m) where m = len(username)
        """
        node = self.__root
        for char in username:
            if not node.has_child(char):
                node.set_child(char, TrieNode())
            node = node.get_child(char)
        if not node.is_end():
            self.__size += 1
        node.set_end(player_id)

    def contains(self, username):
        """
        Return True if username exists as a complete word in the trie.

        Time complexity: O(m)
        """
        node = self.__root
        for char in username:
            if not node.has_child(char):
                return False
            node = node.get_child(char)
        return node.is_end()

    def prefix_search(self, prefix):
        """
        Return all (username, player_id) pairs whose username starts
        with prefix.  Returns [] if prefix is not found in the trie.

        Time complexity: O(m + k) where m = len(prefix), k = matches
        """
        node = self.__root
        for char in prefix:
            if not node.has_child(char):
                return []
            node = node.get_child(char)
        return self.__traverse(node, prefix)

    def size(self):
        """Return the number of complete usernames stored."""
        return self.__size

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def __traverse(self, node, prefix_so_far):
        """
        Recursively collect every complete (username, player_id) pair
        reachable from node, prepending prefix_so_far.
        """
        results = []
        if node.is_end():
            results.append((prefix_so_far, node.get_player_id()))
        for char, child in node.get_children():
            results = results + self.__traverse(child, prefix_so_far + char)
        return results
