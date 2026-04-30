"""
graph_tests.py - Unit tests for Graph

Author: [Your Name]
Date:   [Date]
Lab:    Lab 7 - NPC Dialog with Graphs

TODO (Part 5)
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
    g.add_node("A", data="hello")

    assert g.has_node("A") is True
    assert g.has_node("B") is False
    assert len(g) == 1

    print("PASS test_add_node_and_has_node")


def test_add_edge_creates_missing_nodes():
    g = Graph()
    g.add_edge("A", "B")

    assert g.has_node("A") is True
    assert g.has_node("B") is True
    assert g.has_edge("A", "B") is True
    assert g.has_edge("B", "A") is True

    print("PASS test_add_edge_creates_missing_nodes")


def test_directed_edge_semantics():
    g = Graph(directed=True)
    g.add_edge("A", "B")

    assert g.has_edge("A", "B") is True
    assert g.has_edge("B", "A") is False

    print("PASS test_directed_edge_semantics")


def test_undirected_edge_semantics():
    g = Graph(directed=False)
    g.add_edge("A", "B")

    assert g.has_edge("A", "B") is True
    assert g.has_edge("B", "A") is True

    print("PASS test_undirected_edge_semantics")


def test_get_neighbors():
    g = Graph(directed=True)
    g.add_edge("A", "B", weight=5, edge_data="choice text")

    neighbors = g.get_neighbors("A")

    assert len(neighbors) == 1
    assert neighbors[0] == ("B", 5, "choice text")

    print("PASS test_get_neighbors")


def test_get_node_data():
    g = Graph()
    g.add_node("A", data={"name": "NPC"})

    assert g.get_node_data("A") == {"name": "NPC"}

    g.add_node("A", data={"name": "Updated NPC"})
    assert g.get_node_data("A") == {"name": "Updated NPC"}

    print("PASS test_get_node_data")


def test_remove_edge():
    g = Graph()
    g.add_edge("A", "B")

    assert g.has_edge("A", "B") is True
    assert g.has_edge("B", "A") is True

    g.remove_edge("A", "B")

    assert g.has_edge("A", "B") is False
    assert g.has_edge("B", "A") is False

    print("PASS test_remove_edge")


def test_remove_node():
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("B", "C")

    g.remove_node("B")

    assert g.has_node("B") is False
    assert g.has_node("A") is True
    assert g.has_node("C") is True
    assert g.has_edge("A", "B") is False
    assert g.has_edge("C", "B") is False

    print("PASS test_remove_node")


def test_bfs_discovery_order_and_reachability():
    g = Graph(directed=True)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("C", "E")
    g.add_node("Z")

    assert g.bfs("A") == ["A", "B", "C", "D", "E"]
    assert "Z" not in g.bfs("A")

    print("PASS test_bfs_discovery_order_and_reachability")


def test_dfs_discovery_order_and_reachability():
    g = Graph(directed=True)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("C", "E")
    g.add_node("Z")

    assert g.dfs("A") == ["A", "B", "D", "C", "E"]
    assert "Z" not in g.dfs("A")

    print("PASS test_dfs_discovery_order_and_reachability")


def test_shortest_path_exists():
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("A", "D")
    g.add_edge("D", "C")

    path = g.shortest_path("A", "C")

    assert path == ["A", "B", "C"] or path == ["A", "D", "C"]

    print("PASS test_shortest_path_exists")


def test_shortest_path_no_path_exists():
    g = Graph(directed=True)
    g.add_edge("A", "B")
    g.add_node("C")

    assert g.shortest_path("A", "C") == []

    print("PASS test_shortest_path_no_path_exists")


def test_shortest_path_self_path():
    g = Graph()
    g.add_node("A")

    assert g.shortest_path("A", "A") == ["A"]

    print("PASS test_shortest_path_self_path")


def test_disconnected_graph_and_isolated_node():
    g = Graph()
    g.add_edge("A", "B")
    g.add_node("C")

    assert g.has_node("C") is True
    assert g.get_neighbors("C") == []
    assert g.bfs("C") == ["C"]
    assert g.dfs("C") == ["C"]

    print("PASS test_disconnected_graph_and_isolated_node")


def test_self_loop():
    g = Graph(directed=True)
    g.add_edge("A", "A", weight=2, edge_data="loop")

    assert g.has_node("A") is True
    assert g.has_edge("A", "A") is True
    assert g.get_neighbors("A") == [("A", 2, "loop")]
    assert g.bfs("A") == ["A"]
    assert g.dfs("A") == ["A"]
    assert g.shortest_path("A", "A") == ["A"]

    print("PASS test_self_loop")


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