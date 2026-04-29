"""
graph.py - Graph data structure

Author: Ibrahim Chatila
Date:   2026-04-26
Lab:    Lab 7 - NPC Dialog with Graphs

Implement an adjacency-list graph that can be directed or undirected.
All method bodies are currently `pass`; replace them with your implementation.

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
        self._adj = HashTable()   # node_id -> list of (neighbor_id, weight, edge_data)
        self._data = HashTable()  # node_id -> arbitrary payload

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
        if from_id not in self._adj:
            self.add_node(from_id)
        if to_id not in self._adj:
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
        # Remove all incoming edges from remaining nodes
        for nid in self._adj:
            self._adj[nid] = [
                (nb, w, ed) for nb, w, ed in self._adj[nid] if nb != node_id
            ]

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
        if from_id not in self._adj:
            raise KeyError(from_id)
        if to_id not in self._adj:
            raise KeyError(to_id)
        old = self._adj[from_id]
        new = [(nb, w, ed) for nb, w, ed in old if nb != to_id]
        if len(new) == len(old):
            raise KeyError((from_id, to_id))
        self._adj[from_id] = new
        if not self.directed:
            self._adj[to_id] = [
                (nb, w, ed) for nb, w, ed in self._adj[to_id] if nb != from_id
            ]

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
        return list(self._adj[node_id])

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
        for nb, w, ed in self._adj[from_id]:
            if nb == to_id:
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
        return self._data[node_id]

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
        visited = []
        seen = HashTable()
        seen[start_id] = True
        queue = [start_id]
        head = 0
        while head < len(queue):
            node = queue[head]
            head += 1
            visited.append(node)
            for nb, w, ed in self._adj[node]:
                if nb not in seen:
                    seen[nb] = True
                    queue.append(nb)
        return visited

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
        visited = []
        seen = HashTable()
        stack = [start_id]
        while stack:
            node = stack.pop()
            if node in seen:
                continue
            seen[node] = True
            visited.append(node)
            # Push neighbors in reverse so we visit them in forward order
            neighbors = self._adj[node]
            for i in range(len(neighbors) - 1, -1, -1):
                nb, w, ed = neighbors[i]
                if nb not in seen:
                    stack.append(nb)
        return visited

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
        seen = HashTable()
        parent = HashTable()
        seen[start_id] = True
        queue = [start_id]
        head = 0
        while head < len(queue):
            node = queue[head]
            head += 1
            for nb, w, ed in self._adj[node]:
                if nb not in seen:
                    seen[nb] = True
                    parent[nb] = node
                    if nb == end_id:
                        # Reconstruct path
                        path = []
                        cur = end_id
                        while cur != start_id:
                            path.append(cur)
                            cur = parent[cur]
                        path.append(start_id)
                        path.reverse()
                        return path
                    queue.append(nb)
        return []

    def __len__(self):
        """Return the number of nodes.  Time: O(1)."""
        return len(self._adj)

    def __str__(self):
        """Return a human-readable summary of the graph."""
        lines = [f"Graph(directed={self.directed}, nodes={len(self)})"]
        for node_id in self._adj:
            nb_str = ", ".join(
                f"{nb}(w={w})" for nb, w, ed in self._adj[node_id]
            )
            lines.append(f"  {node_id} -> [{nb_str}]")
        return "\n".join(lines)
