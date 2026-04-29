"""
graph_tests.py - Unit tests for Graph

Author: Ibrahim Chatila
Date:   2026-04-26
Lab:    Lab 7 - NPC Dialog with Graphs

Run with:
    cd code/game/datastructures/tests
    python graph_tests.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from datastructures.graph import Graph


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_add_node():
    g = Graph()
    g.add_node("a")
    g.add_node("b", data=42)
    assert g.has_node("a")
    assert g.has_node("b")
    assert not g.has_node("c")
    print("PASS test_add_node")


def test_add_node_data():
    g = Graph()
    g.add_node("x", data={"hp": 100})
    assert g.get_node_data("x") == {"hp": 100}
    g.add_node("x", data={"hp": 50})  # update
    assert g.get_node_data("x") == {"hp": 50}
    print("PASS test_add_node_data")


def test_add_edge_directed():
    g = Graph(directed=True)
    g.add_edge("a", "b")
    assert g.has_edge("a", "b")
    assert not g.has_edge("b", "a")
    print("PASS test_add_edge_directed")


def test_add_edge_undirected():
    g = Graph(directed=False)
    g.add_edge("a", "b")
    assert g.has_edge("a", "b")
    assert g.has_edge("b", "a")
    print("PASS test_add_edge_undirected")


def test_add_edge_auto_creates_nodes():
    g = Graph(directed=True)
    g.add_edge("x", "y")
    assert g.has_node("x")
    assert g.has_node("y")
    print("PASS test_add_edge_auto_creates_nodes")


def test_get_neighbors():
    g = Graph(directed=True)
    g.add_edge("a", "b", weight=3, edge_data="choice1")
    g.add_edge("a", "c", weight=5, edge_data="choice2")
    neighbors = g.get_neighbors("a")
    assert len(neighbors) == 2
    nbs = {nb for nb, w, ed in neighbors}
    assert "b" in nbs
    assert "c" in nbs
    # Check weight and edge_data are preserved
    for nb, w, ed in neighbors:
        if nb == "b":
            assert w == 3
            assert ed == "choice1"
        elif nb == "c":
            assert w == 5
            assert ed == "choice2"
    print("PASS test_get_neighbors")


def test_remove_node():
    g = Graph(directed=True)
    g.add_edge("a", "b")
    g.add_edge("c", "b")
    g.remove_node("b")
    assert not g.has_node("b")
    # Incoming edges to b must be removed
    assert not g.has_edge("a", "b")
    assert not g.has_edge("c", "b")
    try:
        g.remove_node("z")
        assert False, "Should have raised KeyError"
    except KeyError:
        pass
    print("PASS test_remove_node")


def test_remove_edge():
    g = Graph(directed=True)
    g.add_edge("a", "b")
    g.add_edge("a", "c")
    g.remove_edge("a", "b")
    assert not g.has_edge("a", "b")
    assert g.has_edge("a", "c")
    try:
        g.remove_edge("a", "b")
        assert False, "Should have raised KeyError"
    except KeyError:
        pass
    print("PASS test_remove_edge")


def test_remove_edge_undirected():
    g = Graph(directed=False)
    g.add_edge("a", "b")
    g.remove_edge("a", "b")
    assert not g.has_edge("a", "b")
    assert not g.has_edge("b", "a")
    print("PASS test_remove_edge_undirected")


def test_bfs_order():
    g = Graph(directed=True)
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 4)
    g.add_edge(3, 5)
    result = g.bfs(1)
    assert result[0] == 1
    # BFS must visit 2 and 3 before 4 and 5
    assert result.index(2) < result.index(4)
    assert result.index(3) < result.index(5)
    assert set(result) == {1, 2, 3, 4, 5}
    print("PASS test_bfs_order")


def test_dfs_order():
    g = Graph(directed=True)
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 4)
    result = g.dfs(1)
    assert result[0] == 1
    assert set(result) == {1, 2, 3, 4}
    # In DFS 2 must appear before 3 (forward neighbor order), and 4 after 2
    assert result.index(2) < result.index(3)
    assert result.index(4) < result.index(3)
    print("PASS test_dfs_order")


def test_shortest_path_exists():
    g = Graph(directed=True)
    g.add_edge("a", "b")
    g.add_edge("b", "c")
    g.add_edge("a", "c")  # shortcut
    path = g.shortest_path("a", "c")
    assert path[0] == "a"
    assert path[-1] == "c"
    assert len(path) == 2  # direct edge a->c is shorter
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


def test_disconnected_graph():
    g = Graph(directed=False)
    g.add_edge(1, 2)
    g.add_node(3)  # isolated
    bfs_result = g.bfs(1)
    assert set(bfs_result) == {1, 2}
    assert 3 not in bfs_result
    dfs_result = g.dfs(3)
    assert dfs_result == [3]
    print("PASS test_disconnected_graph")


def test_self_loop():
    g = Graph(directed=True)
    g.add_edge("a", "a")
    assert g.has_edge("a", "a")
    path = g.shortest_path("a", "a")
    assert path == ["a"]
    print("PASS test_self_loop")


def test_len():
    g = Graph()
    assert len(g) == 0
    g.add_node(1)
    g.add_node(2)
    assert len(g) == 2
    g.add_edge(3, 4)  # auto-creates 2 nodes
    assert len(g) == 4
    g.remove_node(1)
    assert len(g) == 3
    print("PASS test_len")


def test_nodes():
    g = Graph()
    g.add_node("a")
    g.add_node("b")
    g.add_node("c")
    ns = g.nodes()
    assert set(ns) == {"a", "b", "c"}
    print("PASS test_nodes")


def test_get_node_data_missing():
    g = Graph()
    g.add_node("a")
    try:
        g.get_node_data("z")
        assert False, "Should have raised KeyError"
    except KeyError:
        pass
    print("PASS test_get_node_data_missing")


def test_edge_weight_stored():
    g = Graph(directed=True)
    g.add_edge("a", "b", weight=7)
    neighbors = g.get_neighbors("a")
    assert len(neighbors) == 1
    nb, w, ed = neighbors[0]
    assert nb == "b"
    assert w == 7
    print("PASS test_edge_weight_stored")


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
