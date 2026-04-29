# Graph Complexity Analysis

**Author:** Ibrahim Chatila
**Date:** 2026-04-26
**Lab:** Lab 7 — NPC Dialog with Graphs

---

## 1. Implementation Overview

The graph is represented as an adjacency list backed by a custom `HashTable` (from Lab 6), which maps each `node_id` to a Python list of `(neighbor_id, weight, edge_data)` tuples. A second `HashTable` stores per-node data payloads. The graph defaults to undirected (`directed=False`), and in that mode every `add_edge` call inserts both the forward and reverse edge tuple.

---

## 2. Time Complexity Table

| Method          | Big-O      | Justification |
|-----------------|------------|---------------|
| `add_node`      | O(1) avg   | Single HashTable insert; O(1) average with chaining. |
| `add_edge`      | O(1) avg   | Two possible `add_node` calls plus one list `append` (or two for undirected); all O(1) average. |
| `remove_node`   | O(V + E)   | Must scan every other node's adjacency list to delete incoming edges — O(V) nodes × O(degree) edges = O(V + E) in the worst case. |
| `remove_edge`   | O(degree)  | Rebuilds only the adjacency list of `from_id` (length = out-degree); one extra pass for undirected. |
| `has_node`      | O(1) avg   | HashTable `__contains__` hashes the key and probes one bucket. |
| `has_edge`      | O(degree)  | Linear scan of `from_id`'s neighbor list to find `to_id`. |
| `get_neighbors` | O(1) avg   | HashTable lookup returns the list reference; copying it is O(degree). |
| `bfs`           | O(V + E)   | Each node is enqueued once; each edge is inspected once across all neighbor lists. |
| `dfs`           | O(V + E)   | Same argument as BFS — iterative stack visits each node and edge at most once. |
| `shortest_path` | O(V + E)   | BFS-based; stops as soon as `end_id` is reached, but worst case visits the full reachable subgraph. |

---

## 3. Benchmark Results

```
Graph Performance Benchmarks
-------------------------------------------------------------------------------
 Nodes      Build (s)   has_node (s)      bfs (s)      dfs (s)     shortest (s)
-------------------------------------------------------------------------------
   100       0.003735       0.000162     0.000588     0.000703         0.005569
   500       0.012351       0.000184     0.003566     0.004946         0.004363
  1000       0.025490       0.000172     0.008915     0.008859         0.004899
-------------------------------------------------------------------------------

(networkx not installed — skipping comparison)
```

---

## 4. Space Complexity

The graph uses **O(V + E)** space.

- **V** is the number of nodes: each node requires one entry in `_adj` (the adjacency HashTable) and one entry in `_data` (the payload HashTable).
- **E** is the number of edges: each edge is stored as one `(neighbor_id, weight, edge_data)` tuple inside the neighbor list of its source node. For an undirected graph every logical edge is stored twice (once in each direction), so space is O(V + 2E) = O(V + E).
- The BFS/DFS/shortest_path traversals allocate an additional O(V) `HashTable` for the visited set and O(V) for the queue or stack, but this is temporary working space, not persistent graph storage.

---

## 5. Reflection Questions

**Q1.** BFS and DFS both visit every reachable node exactly once.
Why might BFS be preferred for `shortest_path` even though both are O(V + E)?

BFS expands nodes in order of increasing distance from the source, so it is guaranteed to reach `end_id` via the fewest-edge path first. DFS can reach a destination via a long, winding route before discovering a shorter one — there is no guarantee that the first path DFS finds is the shortest. Both algorithms have the same asymptotic cost, but BFS gives the correct answer by construction without any backtracking or path-length comparison.

---

**Q2.** Your adjacency list uses O(V + E) space. An adjacency *matrix* uses O(V²).
For the NPC dialog trees in this lab (small, sparse graphs), which representation is
more appropriate? Would your answer change for a 10,000-node social network graph?

For the dialog trees in this lab (5–10 nodes, sparse edges) either structure works, but the adjacency list is still a better fit because iterating neighbors for BFS/DFS is O(degree) rather than O(V). For a 10,000-node social network the difference becomes critical: the adjacency matrix would need 10,000² = 10⁸ cells (~400 MB for 32-bit ints), whereas a sparse social graph with average degree 50 only needs 10,000 + 500,000 = 510,000 entries in an adjacency list — roughly 800× less memory and faster traversal.

---

**Q3.** Compare your `bfs` timing to networkx's (if you ran the comparison).
What accounts for the difference? Is networkx faster or slower, and why?

networkx was not installed in this environment, so a direct comparison was not run. Based on the benchmark numbers alone: at 1,000 nodes my BFS takes ~8.9 ms. networkx's BFS is implemented in pure Python as well but benefits from highly optimised internal data structures (Python `dict` with a C-level hash table, `collections.deque` for the queue). I expect networkx to be 5–20× faster than my implementation because my `HashTable` has higher constant factors than CPython's built-in dict, and I use a plain list as a queue (O(n) `pop(0)`) rather than a deque. Using a proper deque as the BFS queue would be the single biggest speed improvement for my implementation.

---

## 6. Conclusions

The adjacency-list graph backed by a custom HashTable correctly implements all required operations within the expected asymptotic bounds: O(1) average for node/edge lookups, O(degree) for edge removal, and O(V + E) for BFS, DFS, and shortest-path search. The main constant-factor overhead compared with networkx comes from my HashTable's Python-level bucket scanning and the use of a plain list as the BFS queue; replacing the queue with `collections.deque` would eliminate the O(n) `pop(0)` and yield a meaningful speedup for large graphs. In the game, graphs appear as directed NPC dialog trees where nodes are conversation states and edges are player choices — BFS-based `shortest_path` could, for example, hint to the player the minimum number of dialog steps needed to reach a particular story outcome.

---

## 7. References

- Cormen, Leiserson, Rivest, Stein — *Introduction to Algorithms*, 4th ed., Chapters 20–22 (Graph representations, BFS, DFS).
- Python documentation — `collections.deque` (why deque is O(1) vs list pop(0) O(n)).
- Lab 7 specification — ECE 3822 Spring 2026.
- AI tool use is logged in `ai_conversations.md`.
