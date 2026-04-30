"""
graph_tests.py - Unit tests for Graph

Author: Chuqi Zhang
Date:   2026-04-28
Lab:    Lab 7 - NPC Dialog with Graphs
-------------
Write at least ten tests. Your tests must cover all of these:
  - add_node, add_edge, has_node, has_edge
  - get_neighbors, get_node_data
  - remove_node, remove_edge
  - bfs  (check discovery order and reachability)
  - dfs  (check discovery order and reachability)
  - shortest_path (path exists, no path exists, self-path)
  - directed vs. undirected edge semantics
  - edge cases: disconnected graph, isolated node, self-loop

Run with:
    cd code/game/datastructures/tests
    python graph_tests.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from datastructures.graph import Graph


# ---------------------------------------------------------------------------
# TODO: Write at least 10 tests below.
# Each function must start with 'test_', use assert, and print "PASS <name>".
# Below are some examples you could implement.
# ---------------------------------------------------------------------------

def test_add_node_and_has_node():
    g = Graph()
    g.add_node("a")
    assert g.has_node("a")
    assert not g.has_node("b")
    assert len(g) == 1
    print("PASS test_add_node_and_has_node")
 
def test_add_node_with_data():
    g = Graph()
    g.add_node("a", data={"text": "hello"})
    assert g.get_node_data("a") == {"text": "hello"}
    g.add_node("a", data={"text": "updated"})
    assert g.get_node_data("a") == {"text": "updated"}
    assert len(g) == 1
    print("PASS test_add_node_with_data")
 
def test_add_edge_undirected():
    g = Graph(directed=False)
    g.add_edge("a", "b")
    assert g.has_edge("a", "b")
    assert g.has_edge("b", "a")
    assert g.has_node("a") and g.has_node("b")
    print("PASS test_add_edge_undirected")
 
def test_add_edge_directed():
    g = Graph(directed=True)
    g.add_edge("a", "b")
    assert g.has_edge("a", "b")
    assert not g.has_edge("b", "a")
    print("PASS test_add_edge_directed")
 
def test_add_edge_auto_creates_nodes():
    g = Graph(directed=True)
    g.add_edge("x", "y", weight=5, edge_data="choice")
    assert g.has_node("x") and g.has_node("y")
    assert len(g) == 2
    print("PASS test_add_edge_auto_creates_nodes")
 
def test_get_neighbors():
    g = Graph(directed=True)
    g.add_edge("a", "b", edge_data="go to b")
    g.add_edge("a", "c", edge_data="go to c")
    neighbors = g.get_neighbors("a")
    assert len(neighbors) == 2
    ids = [n[0] for n in neighbors]
    assert "b" in ids and "c" in ids
    print("PASS test_get_neighbors")
 
def test_remove_node():
    g = Graph(directed=True)
    g.add_edge("a", "b")
    g.add_edge("b", "c")
    g.add_edge("c", "a")
    g.remove_node("b")
    assert not g.has_node("b")
    assert not g.has_edge("a", "b")
    assert len(g) == 2
    print("PASS test_remove_node")
 
def test_remove_edge():
    g = Graph(directed=False)
    g.add_edge("a", "b")
    g.remove_edge("a", "b")
    assert not g.has_edge("a", "b")
    assert not g.has_edge("b", "a")
    assert g.has_node("a") and g.has_node("b")
    print("PASS test_remove_edge")
 
def test_nodes():
    g = Graph()
    g.add_node("a")
    g.add_node("b")
    g.add_node("c")
    n = g.nodes()
    assert len(n) == 3
    assert set(n) == {"a", "b", "c"}
    print("PASS test_nodes")
 
def test_bfs():
    g = Graph(directed=True)
    g.add_edge("a", "b")
    g.add_edge("a", "c")
    g.add_edge("b", "d")
    g.add_edge("c", "d")
    result = g.bfs("a")
    assert result[0] == "a"
    assert set(result) == {"a", "b", "c", "d"}
    assert result.index("a") < result.index("b")
    assert result.index("a") < result.index("c")
    print("PASS test_bfs")
 
def test_dfs():
    g = Graph(directed=True)
    g.add_edge("a", "b")
    g.add_edge("a", "c")
    g.add_edge("b", "d")
    g.add_edge("c", "d")
    result = g.dfs("a")
    assert result[0] == "a"
    assert set(result) == {"a", "b", "c", "d"}
    print("PASS test_dfs")
 
def test_shortest_path_exists():
    g = Graph(directed=True)
    g.add_edge("a", "b")
    g.add_edge("b", "c")
    g.add_edge("a", "c")
    path = g.shortest_path("a", "c")
    assert path == ["a", "c"]
    print("PASS test_shortest_path_exists")
 
def test_shortest_path_no_path():
    g = Graph(directed=True)
    g.add_node("a")
    g.add_node("b")
    path = g.shortest_path("a", "b")
    assert path == []
    print("PASS test_shortest_path_no_path")
 
def test_shortest_path_self():
    g = Graph(directed=True)
    g.add_node("a")
    path = g.shortest_path("a", "a")
    assert path == ["a"]
    print("PASS test_shortest_path_self")
 
def test_isolated_node():
    g = Graph()
    g.add_node("alone")
    assert g.has_node("alone")
    assert g.get_neighbors("alone") == []
    result = g.bfs("alone")
    assert result == ["alone"]
    print("PASS test_isolated_node")
 
def test_str():
    g = Graph(directed=True)
    g.add_edge("a", "b")
    s = str(g)
    assert "Directed" in s
    assert "2" in s
    print("PASS test_str")


# ---------------------------------------------------------------------------
# Do not modify
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    tests = [
        (name, fn)
        for name, fn in sorted(globals().items())
        if name.startswith("test_") and callable(fn)
    ]
 
    passed = failed = 0
    for name, fn in tests:
        try:
            fn()
            passed += 1
        except Exception as exc:
            print(f"FAIL {name}: {exc}")
            failed += 1
 
    print(f"\n{'=' * 50}")
    print(f"Results: {passed} passed, {failed} failed / {passed + failed} total")
    if failed:
        sys.exit(1)
    else:
        print("All tests passed!")
