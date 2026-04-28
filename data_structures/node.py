"""
TrieNode used by the Trie. Children are stored in a fixed 128-slot
array indexed by ASCII value instead of a dict.

Author: Ibrahim Chatila
Date: 2026-04-26
"""

from data_structures.array_list import ArrayList

_ASCII_SIZE = 128


class TrieNode:

    def __init__(self):
        self.__children  = [None] * _ASCII_SIZE
        self.__is_end    = False
        self.__player_id = None

    def get_child(self, char):
        return self.__children[ord(char)]

    def set_child(self, char, node):
        self.__children[ord(char)] = node

    def has_child(self, char):
        return self.__children[ord(char)] is not None

    def get_children(self):
        """Return all existing children as an ArrayList of (char, node) pairs."""
        result = ArrayList()
        for i in range(_ASCII_SIZE):
            if self.__children[i] is not None:
                result.append((chr(i), self.__children[i]))
        return result

    def is_end(self):
        return self.__is_end

    def set_end(self, player_id):
        self.__is_end    = True
        self.__player_id = player_id

    def get_player_id(self):
        return self.__player_id
