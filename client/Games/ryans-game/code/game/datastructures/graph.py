"""
graph.py - Graph data structure

Author: Ryan Miller
Date:   [Date]
Lab:    Lab 7 - NPC Dialog with Graphs

Implement an adjacency-list graph that can be directed or undirected.
"""

from datastructures.hash_table import HashTable


class Graph:
    """
    Adjacency-list graph.
    """

    def __init__(self, directed=False):
        """
        Initialize an empty graph.

        Time complexity: O(1)
        """
        self.directed = directed
        self._adj = HashTable()
        self._data = HashTable()

    def add_node(self, node_id, data=None):
        """
        Add a node with an optional data payload.

        Time complexity: O(1) average
        """
        if node_id not in self._adj:
            self._adj.set(node_id, [])

        self._data.set(node_id, data)

    def add_edge(self, from_id, to_id, weight=1, edge_data=None):
        """
        Add an edge from from_id to to_id.

        Time complexity: O(1) average
        """
        if from_id not in self._adj:
            self.add_node(from_id)

        if to_id not in self._adj:
            self.add_node(to_id)

        neighbors = self._adj.get(from_id)
        neighbors.append((to_id, weight, edge_data))
        self._adj.set(from_id, neighbors)

        if not self.directed:
            reverse_neighbors = self._adj.get(to_id)
            reverse_neighbors.append((from_id, weight, edge_data))
            self._adj.set(to_id, reverse_neighbors)

    def remove_node(self, node_id):
        """
        Remove a node and all edges that touch it.

        Time complexity: O(V + E)
        """
        if node_id not in self._adj:
            raise KeyError("Node does not exist")

        self._adj.delete(node_id)
        self._data.delete(node_id)

        for current_id, neighbors in self._adj.items():
            new_neighbors = []

            for neighbor_id, weight, edge_data in neighbors:
                if neighbor_id != node_id:
                    new_neighbors.append((neighbor_id, weight, edge_data))

            self._adj.set(current_id, new_neighbors)

    def remove_edge(self, from_id, to_id):
        """
        Remove the edge from from_id to to_id.

        Time complexity: O(degree(from_id))
        """
        if from_id not in self._adj or to_id not in self._adj:
            raise KeyError("Node does not exist")

        removed = self._remove_one_edge(from_id, to_id)

        if not removed:
            raise KeyError("Edge does not exist")

        if not self.directed:
            self._remove_one_edge(to_id, from_id)

    def _remove_one_edge(self, from_id, to_id):
        """
        Helper method to remove one directed edge.

        Time complexity: O(degree(from_id))
        """
        neighbors = self._adj.get(from_id)
        new_neighbors = []
        removed = False

        for neighbor_id, weight, edge_data in neighbors:
            if neighbor_id == to_id and not removed:
                removed = True
            else:
                new_neighbors.append((neighbor_id, weight, edge_data))

        self._adj.set(from_id, new_neighbors)
        return removed

    def get_neighbors(self, node_id):
        """
        Return all edges leaving node_id.

        Time complexity: O(1)
        """
        if node_id not in self._adj:
            raise KeyError("Node does not exist")

        return self._adj.get(node_id)

    def has_node(self, node_id):
        """
        Return True if node_id is in the graph.

        Time complexity: O(1) average
        """
        return node_id in self._adj

    def has_edge(self, from_id, to_id):
        """
        Return True if an edge from_id to to_id exists.

        Time complexity: O(degree(from_id))
        """
        if from_id not in self._adj:
            return False

        neighbors = self._adj.get(from_id)

        for neighbor_id, weight, edge_data in neighbors:
            if neighbor_id == to_id:
                return True

        return False

    def get_node_data(self, node_id):
        """
        Return the data payload stored at node_id.

        Time complexity: O(1) average
        """
        if node_id not in self._adj:
            raise KeyError("Node does not exist")

        return self._data.get(node_id)

    def nodes(self):
        """
        Return a list of all node IDs.

        Time complexity: O(V)
        """
        node_list = []

        for node_id, neighbors in self._adj.items():
            node_list.append(node_id)

        return node_list

    def bfs(self, start_id):
        """
        Breadth-first traversal from start_id.

        Time complexity: O(V + E)
        """
        if start_id not in self._adj:
            raise KeyError("Start node does not exist")

        visited = []
        queue = []

        visited.append(start_id)
        queue.append(start_id)

        while len(queue) > 0:
            current = queue.pop(0)

            for neighbor_id, weight, edge_data in self._adj.get(current):
                if neighbor_id not in visited:
                    visited.append(neighbor_id)
                    queue.append(neighbor_id)

        return visited

    def dfs(self, start_id):
        """
        Depth-first traversal from start_id.

        Time complexity: O(V + E)
        """
        if start_id not in self._adj:
            raise KeyError("Start node does not exist")

        visited = []
        stack = []

        stack.append(start_id)

        while len(stack) > 0:
            current = stack.pop()

            if current not in visited:
                visited.append(current)

                neighbors = self._adj.get(current)

                for i in range(len(neighbors) - 1, -1, -1):
                    neighbor_id = neighbors[i][0]

                    if neighbor_id not in visited:
                        stack.append(neighbor_id)

        return visited

    def shortest_path(self, start_id, end_id):
        """
        Find the path with the fewest edges between two nodes.

        Time complexity: O(V + E)
        """
        if start_id not in self._adj or end_id not in self._adj:
            raise KeyError("Node does not exist")

        if start_id == end_id:
            return [start_id]

        visited = []
        queue = []

        visited.append(start_id)
        queue.append((start_id, [start_id]))

        while len(queue) > 0:
            current, path = queue.pop(0)

            for neighbor_id, weight, edge_data in self._adj.get(current):
                if neighbor_id == end_id:
                    return path + [neighbor_id]

                if neighbor_id not in visited:
                    visited.append(neighbor_id)
                    queue.append((neighbor_id, path + [neighbor_id]))

        return []

    def __len__(self):
        """
        Return the number of nodes.

        Time complexity: O(1)
        """
        return len(self._adj)

    def __str__(self):
        """
        Return a human-readable summary of the graph.
        """
        edge_count = 0

        for node_id, neighbors in self._adj.items():
            edge_count += len(neighbors)

        if not self.directed:
            edge_count = edge_count // 2

        return "Graph(nodes=" + str(len(self)) + ", edges=" + str(edge_count) + ", directed=" + str(self.directed) + ")"