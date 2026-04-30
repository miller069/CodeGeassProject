"""
graph_complexity.py - Performance benchmarks for Graph

Author: Chuqi Zhang
Date:   2026-04-28
Lab:    Lab 7 - NPC Dialog with Graphs
-------------
Write a benchmarking script that measures the performance of your Graph
implementation. Your script must:

  1. Build graphs of at least three different sizes (e.g. 100, 500, 1000 nodes).
  2. Measure the time for each of these operations at each size:
       - Building the graph (add_node / add_edge)
       - has_node (many random queries)
       - bfs from a starting node
       - dfs from a starting node
       - shortest_path for several random pairs
  3. Print a results table you can paste into analysis_write_up.md.

Optionally, compare against networkx (pip install networkx).

Run with:
    cd code/game/datastructures/complexity
    python graph_complexity.py
"""

import time
import random
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from datastructures.graph import Graph

def build_random_graph(n, edge_factor=3, directed=True):
  g = Graph(directed=directed)
  for i in range(n):
    g.add_node(i)
  for _ in range(n * edge_factor):
    a = random.randint(0, n - 1)
    b = random.randint(0, n - 1)
    if a != b:
      g.add_edge(a, b)
  return g

def benchmark_build(sizes):
  print("=" * 55)
  print("Benchmark: Build Graph (add_node + add_edge)")
  print("=" * 55)
  print(f"{'nodes':>8} | {'edges':>8} | {'Time (s)':>10}")
  print("-" * 32)

  for n in sizes:
    edges = n * 3
    start = time.time()
    g = Graph(directed=True)
    for i in range(n):
      g.add_node(i)
    for _ in range(edges):
      a = random.randint(0, n-1)
      b = random.randint(0, n-1)
      if a != b:
        g.add_edge(a, b)
    elapsed = time.time() - start
    print(f"{n:>8} | {edges:>8} | {elapsed:>10.6f}")
  
  print()

def benchmark_has_node(sizes, queries=5000):
  print("=" * 55)
  print(f"Benchmark: has_node x {queries}")
  print("=" * 55)
  print(f"{'nodes':>8} | {'Time (s)':>10}")
  print("-" * 22)

  for n in sizes:
    g = build_random_graph(n)
    targets = [random.randint(0, n*2) for _ in range(queries)]

    start = time.time()
    for t in targets:
      g.has_node(t)
    elapsed = time.time() - start
    print(f"{n:>8} | {elapsed:>10.6f}")
  print()

def benchmark_bfs_dfs(sizes):
  print("=" * 55)
  print("Benchmark: BFS vs DFS")
  print("=" * 55)
  print(f"{'nodes':>8} | {'BFS (s):>10'} | {'DFS (s)':>10}")
  print("-" * 34)

  for n in sizes:
    g = build_random_graph(n)
    start = time.time()
    g.bfs(0)
    bfs_t = time.time() - start

    start = time.time()
    g.dfs(0)
    dfs_t = time.time() - start

    print(f"{n:>8} | {bfs_t:>10.6f} | {dfs_t:>10.6f}")

  print()

def benchmark_shortest_path(sizes, queries=100):
  print("=" * 55)
  print(f"Benchmark: shortest_path x {queries}")
  print("=" * 55)
  print(f"{'nodes':>8} | {'Time (s)':>10}")
  print("-" * 22)

  for n in sizes:
    g = build_random_graph(n)
    pairs = [(random.randint(0, n-1), random.randint(0, n-1)) for _ in range(queries)]
    start = time.time()
    for a, b in pairs:
      g.shortest_path(a, b)
    elapsed = time.time() - start
    print(f"{n:>8} | {elapsed:>10.6f}")

  print()


def main():
  print("\n" + "=" * 55)
  print("GRAPH COMPLEXITY ANALYSIS")
  print("=" * 55 + "\n")

  sizes = [100, 500, 1000]

  benchmark_build(sizes)
  benchmark_has_node(sizes)
  benchmark_bfs_dfs(sizes)
  benchmark_shortest_path(sizes)

  print("=" * 55)
  print("ANALYSIS COMPLETE")
  print("=" * 55)

if __name__ == "__main__":
  main()