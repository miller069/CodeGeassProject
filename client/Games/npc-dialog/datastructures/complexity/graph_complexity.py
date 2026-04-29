"""
graph_complexity.py - Performance benchmarks for Graph

Author: Ibrahim Chatila
Date:   2026-04-26
Lab:    Lab 7 - NPC Dialog with Graphs

Measures build time, has_node, bfs, dfs, and shortest_path across
three graph sizes and optionally compares against networkx.

Run with:
    cd code/game/datastructures/complexity
    python graph_complexity.py
"""

import sys
import os
import time
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from datastructures.graph import Graph

SIZES   = [100, 500, 1000]
QUERIES = 200   # number of random has_node / shortest_path queries per size
SEED    = 42


def build_graph(n, seed=SEED):
    """Build a directed graph with n nodes and ~3n random edges."""
    rng = random.Random(seed)
    g = Graph(directed=True)
    for i in range(n):
        g.add_node(i)
    for _ in range(n * 3):
        a = rng.randint(0, n - 1)
        b = rng.randint(0, n - 1)
        g.add_edge(a, b)
    return g


def time_it(fn, repeat=1):
    """Return elapsed seconds for fn() averaged over `repeat` calls."""
    start = time.perf_counter()
    for _ in range(repeat):
        fn()
    return (time.perf_counter() - start) / repeat


def benchmark():
    rng = random.Random(SEED)

    col_w = [6, 14, 14, 12, 12, 16]
    header = (
        f"{'Nodes':>{col_w[0]}} "
        f"{'Build (s)':>{col_w[1]}} "
        f"{'has_node (s)':>{col_w[2]}} "
        f"{'bfs (s)':>{col_w[3]}} "
        f"{'dfs (s)':>{col_w[4]}} "
        f"{'shortest (s)':>{col_w[5]}}"
    )
    sep = "-" * len(header)

    print("\nGraph Performance Benchmarks")
    print(sep)
    print(header)
    print(sep)

    results = []

    for n in SIZES:
        # Build
        t_build = time_it(lambda n=n: build_graph(n))
        g = build_graph(n)

        nodes = g.nodes()

        # has_node — mix of present and absent keys
        queries_hn = [rng.randint(0, n * 2 - 1) for _ in range(QUERIES)]
        t_has = time_it(lambda: [g.has_node(q) for q in queries_hn])

        # bfs from node 0
        t_bfs = time_it(lambda: g.bfs(0))

        # dfs from node 0
        t_dfs = time_it(lambda: g.dfs(0))

        # shortest_path — random pairs
        pairs = [(rng.randint(0, n - 1), rng.randint(0, n - 1))
                 for _ in range(QUERIES)]
        t_sp = time_it(lambda: [g.shortest_path(a, b) for a, b in pairs])

        results.append((n, t_build, t_has, t_bfs, t_dfs, t_sp))

        print(
            f"{n:>{col_w[0]}} "
            f"{t_build:>{col_w[1]}.6f} "
            f"{t_has:>{col_w[2]}.6f} "
            f"{t_bfs:>{col_w[3]}.6f} "
            f"{t_dfs:>{col_w[4]}.6f} "
            f"{t_sp:>{col_w[5]}.6f}"
        )

    print(sep)

    # Optional: compare bfs against networkx
    try:
        import networkx as nx
        print("\nnetworkx comparison (bfs only):")
        print(f"{'Nodes':>6}  {'Graph bfs (s)':>14}  {'nx bfs (s)':>12}  {'ratio':>7}")
        print("-" * 46)
        for n, t_build, t_has, t_bfs, t_dfs, t_sp in results:
            ng = nx.DiGraph()
            rng2 = random.Random(SEED)
            ng.add_nodes_from(range(n))
            for _ in range(n * 3):
                a = rng2.randint(0, n - 1)
                b = rng2.randint(0, n - 1)
                ng.add_edge(a, b)
            t_nx = time_it(lambda ng=ng: list(nx.bfs_tree(ng, 0)))
            ratio = t_bfs / t_nx if t_nx > 0 else float("inf")
            print(f"{n:>6}  {t_bfs:>14.6f}  {t_nx:>12.6f}  {ratio:>7.2f}x")
    except ImportError:
        print("\n(networkx not installed — skipping comparison)")

    print()
    return results


if __name__ == "__main__":
    benchmark()
