"""
graph.py - Graph data structure

Author: Chuqi Zhang
Date:   2026-04-28
Lab:    Lab 7 - NPC Dialog with Graphs

Adjacency-list graph implementation.

Each edge stores:
    (neighbor_id, weight, edge_data)

where weight defaults to 1 and edge_data is an arbitrary payload (used by
the dialog system to store the player's choice text on each edge).

Rule: you may NOT use Python's built-in dict or set inside this class.
Use your HashTable from Lab 6 as the adjacency map:

    from datastructures.hash_table import HashTable
"""

from datastructures.hash_table import HashTable


class Graph:
    """
    Adjacency-list graph.

    Nodes are identified by a hashable node_id (int, str, etc.).
    Edges carry an optional weight (default 1) and arbitrary edge_data.

    Parameters
    ----------
    directed : bool
        True  → each add_edge call creates one directed edge.
        False → each add_edge call creates edges in both directions (default).
    """

    def __init__(self, directed=False):
        """
        Initialize an empty graph.

        Time complexity: O(1)
        """
        self.directed = directed
        # TODO: initialize your HashTable-backed adjacency list and node data store.
        # Example:
        #   self._adj  = HashTable()   # node_id -> list of (neighbor_id, weight, edge_data)
        #   self._data = HashTable()   # node_id -> arbitrary payload
        self._adj = HashTable()
        self._data = HashTable()
        self._size = 0

    def add_node(self, node_id, data=None):
        """
        Add a node with an optional data payload.

        If the node already exists, update its data without changing edges.

        Time complexity: O(1) average

        Args:
            node_id : Hashable identifier.
            data    : Arbitrary payload (default None).
        """
        if node_id not in self._adj:
            self._adj[node_id] = []
            self._size += 1
        self._data[node_id] = data

    def add_edge(self, from_id, to_id, weight=1, edge_data=None):
        """
        Add an edge from from_id to to_id.

        Creates either node automatically if it does not yet exist.
        For undirected graphs, also adds the reverse edge.

        Time complexity: O(1) average

        Args:
            from_id  : Source node.
            to_id    : Destination node.
            weight   : Numeric edge weight (default 1).
            edge_data: Arbitrary payload stored on this edge (default None).
        """
        if not self.has_node(from_id):
            self.add_node(from_id)
        if not self.has_node(to_id):
            self.add_node(to_id)

        self._adj[from_id].append((to_id, weight, edge_data))
        
        if not self.directed:
            self._adj[to_id].append((from_id, weight, edge_data))

    def remove_node(self, node_id):
        """
        Remove a node and all edges that touch it.

        Time complexity: O(V + E)

        Args:
            node_id: Node to remove.

        Raises:
            KeyError: If node_id does not exist.
        """
        if node_id not in self._adj:
            raise KeyError(node_id)

        del self._adj[node_id]
        del self._data[node_id]
        self._size -= 1

        for nid in self._adj:
            edges = self._adj[nid]
            filtered = [e for e in edges if e[0] != node_id]
            self._adj[nid] = filtered

    def remove_edge(self, from_id, to_id):
        """
        Remove the edge from from_id to to_id.

        For undirected graphs, also removes the reverse edge.

        Time complexity: O(degree(from_id))

        Args:
            from_id: Source node.
            to_id  : Destination node.

        Raises:
            KeyError: If either node does not exist or the edge is absent.
        """
        if from_id not in self._adj or to_id not in self._adj:
            raise KeyError(f"Node not found")
        edges = self._adj[from_id]
        new_edges = [e for e in edges if e[0] != to_id]
        if len(new_edges) == len(edges):
            raise KeyError(f"Edge {from_id} -> {to_id} not found")
        self._adj[from_id] = new_edges

        if not self.directed:
            edges = self._adj[to_id]
            new_edges = [e for e in edges if e[0] != from_id]
            self._adj[to_id] = new_edges

    def get_neighbors(self, node_id):
        """
        Return all edges leaving node_id.

        Time complexity: O(1)

        Args:
            node_id: The node to query.

        Returns:
            list of (neighbor_id, weight, edge_data) tuples.
            Returns [] if the node has no outgoing edges.

        Raises:
            KeyError: If node_id does not exist.
        """
        if node_id not in self._adj:
            raise KeyError(node_id)
        return self._adj[node_id]

    def has_node(self, node_id):
        """
        Return True if node_id is in the graph.

        Time complexity: O(1) average
        """
        return node_id in self._adj

    def has_edge(self, from_id, to_id):
        """
        Return True if an edge from_id → to_id exists.

        Time complexity: O(degree(from_id))
        """
        if from_id not in self._adj:
            return False
        for neighbor, _, _ in self._adj[from_id]:
            if neighbor == to_id:
                return True
        return False

    def get_node_data(self, node_id):
        """
        Return the data payload stored at node_id, or None if none.

        Time complexity: O(1) average

        Raises:
            KeyError: If node_id does not exist.
        """
        if node_id not in self._adj:
            raise KeyError(node_id)
        return self._data.get(node_id)

    def nodes(self):
        """
        Return a list of all node IDs.

        Time complexity: O(V)
        """
        return list(self._adj)

    def bfs(self, start_id):
        """
        Breadth-first traversal from start_id.

        Visits only nodes reachable from start_id.
        Time complexity: O(V + E)

        Args:
            start_id: Node to start from.

        Returns:
            list of node_ids in BFS discovery order.

        Raises:
            KeyError: If start_id does not exist.
        """
        if start_id not in self._adj:
            raise KeyError(start_id)
        visited = HashTable()
        visited[start_id] = True
        queue = [start_id]
        head = 0
        result = []

        while head < len(queue):
            current = queue[head]
            head += 1
            result.append(current)

            for neighbor, _, _ in self._adj[current]:
                if neighbor not in visited:
                    visited[neighbor] = True
                    queue.append(neighbor)
        
        return result

    def dfs(self, start_id):
        """
        Depth-first traversal from start_id (iterative).

        Visits only nodes reachable from start_id.
        Time complexity: O(V + E)

        Args:
            start_id: Node to start from.

        Returns:
            list of node_ids in DFS discovery order.

        Raises:
            KeyError: If start_id does not exist.
        """
        if start_id not in self._adj:
            raise KeyError(start_id)

        visited = HashTable()
        stack = [start_id]
        result = []

        while len(stack) > 0:
            current = stack.pop()
            if current in visited:
                continue
            visited[current] = True
            result.append(current)

            neighbors = self._adj[current]
            for i in range(len(neighbors) - 1, -1, -1):
                neighbor = neighbors[i][0]
                if neighbor not in visited:
                    stack.append(neighbor)
        
        return result

    def shortest_path(self, start_id, end_id):
        """
        Find the path with the fewest edges between two nodes (BFS-based).

        Time complexity: O(V + E)

        Args:
            start_id: Starting node.
            end_id  : Destination node.

        Returns:
            list of node_ids from start_id to end_id inclusive,
            or [] if no path exists.

        Raises:
            KeyError: If either node does not exist.
        """
        if start_id not in self._adj:
            raise KeyError(start_id)
        if end_id not in self._adj:
            raise KeyError(end_id)

        if start_id == end_id:
            return [start_id]

        visited = HashTable()
        parent = HashTable()
        visited[start_id] = True
        parent[start_id] = None
        queue = [start_id]
        head = 0

        while head < len(queue):
            current = queue[head]
            head += 1

            for neighbor, _, _ in self._adj[current]:
                if neighbor not in visited:
                    visited[neighbor] = True
                    parent[neighbor] = current

                    if neighbor == end_id:
                        path = []
                        node = end_id
                        while node is not None:
                            path.append(node)
                            node = parent.get(node)
                        path.reverse()
                        return path

                    queue.append(neighbor)
        
        return []


    def __len__(self):
        """Return the number of nodes.  Time: O(1)."""
        return self._size

    def __str__(self):
        """Return a human-readable summary of the graph."""
        edge_count = 0
        for nid in self._adj:
            edge_count += len(self._adj[nid])
        if not self.directed:
            edge_count //= 2
        kind = "Directed" if self.directed else "Undirected"
        return f"Graph({kind}, nodes={self._size}, edges={edge_count})"
