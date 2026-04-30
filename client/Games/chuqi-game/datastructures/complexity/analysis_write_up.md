# Graph Complexity Analysis

**Author:** Chuqi Zhang
**Date:** 2026-04-28
**Lab:** Lab 7 — NPC Dialog with Graphs

---

## 1. Implementation Overview

My Graph uses a HashTable-backed adjacency list. Each node ID maps to a Python list of (neighbor_id, weight, edge_data) tuples in `self._adj`, and node payloads are stored in a separate `self._data` HashTable. The graph is undirected by default; when `directed=False`, every `add_edge` call inserts the edge into both endpoints' adjacency lists.

---

## 2. Time Complexity Table

| Method            | Your Big-O | Justification (1 sentence each) |
|-------------------|------------|----------------------------------|
| `add_node`        | O(1)       | Single HashTable insertion. |
| `add_edge`        | O(1)       | Two HashTable lookups plus one or two list appends. |
| `remove_node`     | O(V + E)   | Deletes the node's entry, then scans every other node's edge list to remove references. |
| `remove_edge`     | O(deg)     | Filters the source node's edge list; for undirected, also filters the destination's list. |
| `has_node`        | O(1)       | Single HashTable `__contains__` check. |
| `has_edge`        | O(deg)     | Linear scan through from_id's neighbor list. |
| `get_neighbors`   | O(1)       | Returns the stored list directly from the HashTable. |
| `bfs`             | O(V + E)   | Visits each node once and inspects each edge once via the queue. |
| `dfs`             | O(V + E)   | Visits each node once and inspects each edge once via the stack. |
| `shortest_path`   | O(V + E)   | BFS with parent tracking; path reconstruction is O(V) in the worst case. |

---

## 3. Benchmark Results

 
```
============================================================
GRAPH COMPLEXITY ANALYSIS
============================================================
 
============================================================
Benchmark: Build Graph (add_node + add_edge)
============================================================
   nodes |    edges |   Time (s)
--------------------------------
     100 |      300 |   0.006234
     500 |     1500 |   0.027619
    1000 |     3000 |   0.055625
 
============================================================
Benchmark: has_node x 5000
============================================================
   nodes |   Time (s)
----------------------
     100 |   0.012639
     500 |   0.013533
    1000 |   0.013396
 
============================================================
Benchmark: BFS vs DFS
============================================================
   nodes | BFS (s)    |    DFS (s)
----------------------------------
     100 |   0.001671 |   0.001769
     500 |   0.009562 |   0.011658
    1000 |   0.018294 |   0.023030
 
============================================================
Benchmark: shortest_path x 100
============================================================
   nodes |   Time (s)
----------------------
     100 |   0.066422
     500 |   0.635235
    1000 |   0.983062
 
============================================================
ANALYSIS COMPLETE
============================================================
```

---

## 4. Space Complexity

The graph uses O(V + E) memory. V is the number of nodes, each occupying one HashTable entry in `_adj` and one in `_data`. E is the total number of edges; each edge is stored as a (neighbor_id, weight, edge_data) tuple in the source node's adjacency list (doubled for undirected graphs). The HashTable itself adds bucket-array overhead proportional to its capacity, but this stays within a constant factor of V due to the 0.75 load-factor threshold.

---

## 5. Reflection Questions

**Q1.** BFS and DFS both visit every reachable node exactly once.
Why might BFS be preferred for `shortest_path` even though both are O(V + E)?

BFS explores nodes in order of increasing distance from the source, so the first time it reaches the destination, that path is guaranteed to have the fewest edges.

---

**Q2.** Your adjacency list uses O(V + E) space. An adjacency *matrix* uses O(V²).
For the NPC dialog trees in this lab (small, sparse graphs), which representation is
more appropriate? Would your answer change for a 10,000-node social network graph?

For NPC dialog trees with roughly 5-10 nodes and 10-20edges, the adjacency list is more appropriate because it uses memory proportional to the actual edges rather than allocating a 10x10 matrix that is mostly empty.

---

**Q3.** Compare your `bfs` timing to networkx's (if you ran the comparison).
What accounts for the difference? Is networkx faster or slower, and why?

I did not run the networkx comparison in this benchmark.

---

## 6. Conclusions

My graph implementation scales as expected: build time grows linearly with V + E (5 x nodes -> ~5x time), has_node stays constant regardless of graph size (0.013s for all sizes), and BFS/DFS grow linearly with graph size.
---

## 7. References

- Lab 6 HashTable implementation