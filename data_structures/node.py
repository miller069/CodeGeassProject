"""
data_structures/node.py - TrieNode for the player-username Trie

Author: Ibrahim Chatila
Date:   2026-04-26
Project: The Arcade — ECE 3822
"""


class TrieNode:
    """
    A single node in the Trie.

    One dict is allowed here (maps single chars → child TrieNode).
    """

    def __init__(self):
        self.__children  = {}       # char -> TrieNode
        self.__is_end    = False
        self.__player_id = None

    # ------------------------------------------------------------------
    # Child management
    # ------------------------------------------------------------------

    def get_child(self, char):
        """Return the child TrieNode for char, or None if absent."""
        return self.__children.get(char, None)

    def set_child(self, char, node):
        """Map char to node in the children dict."""
        self.__children[char] = node

    def has_child(self, char):
        """Return True if char is a key in __children."""
        return char in self.__children

    def get_children(self):
        """Return a list of (char, TrieNode) pairs for all children."""
        result = []
        for char, node in self.__children.items():
            result.append((char, node))
        return result

    # ------------------------------------------------------------------
    # End-of-word marker
    # ------------------------------------------------------------------

    def is_end(self):
        """Return True if this node marks the end of a complete username."""
        return self.__is_end

    def set_end(self, player_id):
        """Mark this node as the end of a username and store player_id."""
        self.__is_end    = True
        self.__player_id = player_id

    def get_player_id(self):
        """Return the player_id stored at this end node, or None."""
        return self.__player_id
