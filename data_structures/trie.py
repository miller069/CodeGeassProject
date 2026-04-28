"""
Trie for fast username prefix search.
Maps usernames to player IDs using a character-by-character tree.

Author: Ibrahim Chatila
Date: 2026-04-26
"""

from data_structures.node import TrieNode
from data_structures.array_list import ArrayList


class Trie:

    def __init__(self):
        self.__root = TrieNode()
        self.__size = 0

    def insert(self, username, player_id):
        """Add a username and its player ID. Updates the ID if the username already exists."""
        node = self.__root
        for char in username:
            if not node.has_child(char):
                node.set_child(char, TrieNode())
            node = node.get_child(char)
        if not node.is_end():
            self.__size += 1
        node.set_end(player_id)

    def contains(self, username):
        """Return True only if the full username was inserted."""
        node = self.__root
        for char in username:
            if not node.has_child(char):
                return False
            node = node.get_child(char)
        return node.is_end()

    def prefix_search(self, prefix):
        """Return an ArrayList of (username, player_id) pairs that start with prefix."""
        node = self.__root
        for char in prefix:
            if not node.has_child(char):
                return ArrayList()
            node = node.get_child(char)
        return self.__traverse(node, prefix)

    def size(self):
        return self.__size

    def __traverse(self, node, prefix_so_far):
        results = ArrayList()
        if node.is_end():
            results.append((prefix_so_far, node.get_player_id()))
        for char, child in node.get_children():
            child_results = self.__traverse(child, prefix_so_far + char)
            for item in child_results:
                results.append(item)
        return results
