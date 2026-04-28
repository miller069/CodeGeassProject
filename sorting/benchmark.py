"""
Benchmarks for Mergesort and Heapsort.
Run from the CodeGeassProject directory: python sorting/benchmark.py

Author: Ibrahim Chatila
Date: 2026-04-26
"""

import time
import random
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sorting.mergesort import Mergesort
from sorting.heapsort  import Heapsort
from data_structures.array_list import ArrayList

SEED = 42


def generate_sessions(n, seed=SEED):
    rng      = random.Random(seed)
    sessions = ArrayList()
    games    = ("snake", "tetris", "pong", "pacman", "breakout")
    outcomes = ("win", "loss", "draw")
    year     = 2025
    for i in range(n):
        month = rng.randint(1, 12)
        day   = rng.randint(1, 28)
        date  = f"{year}-{month:02d}-{day:02d}"
        sessions.append({
            "session_id": f"s{i}",
            "player_id":  f"p{rng.randint(1, 100)}",
            "game_id":    games[rng.randint(0, len(games) - 1)],
            "start_time": date,
            "end_time":   date,
            "score":      rng.randint(0, 10000),
            "outcome":    outcomes[rng.randint(0, len(outcomes) - 1)],
        })
    return sessions


def benchmark_sorting(sizes=None):
    """Compare Mergesort vs Heapsort on score field. Saves sorting_benchmark.png."""
    if sizes is None:
        sizes = (1000, 5000, 10000, 50000, 100000)

    ms = Mergesort()
    hs = Heapsort()

    ms_times = ArrayList()
    hs_times = ArrayList()

    print("\nSorting Benchmark")
    print(f"{'n':>8}  {'Mergesort (s)':>15}  {'Heapsort (s)':>14}")

    for n in sizes:
        data = generate_sessions(n)

        t0 = time.perf_counter()
        ms.sort(data, key=lambda x: x["score"])
        ms_time = time.perf_counter() - t0

        t0 = time.perf_counter()
        hs.sort(data, key=lambda x: x["score"])
        hs_time = time.perf_counter() - t0

        ms_times.append(ms_time)
        hs_times.append(hs_time)
        print(f"{n:>8}  {ms_time:>15.6f}  {hs_time:>14.6f}")

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(sizes, list(ms_times), marker="o", label="Mergesort")
    ax.plot(sizes, list(hs_times), marker="s", label="Heapsort")
    ax.set_xlabel("Number of sessions (n)")
    ax.set_ylabel("Time (seconds)")
    ax.set_title("Mergesort vs Heapsort - sort by score")
    ax.legend()
    ax.grid(True, alpha=0.4)
    fig.tight_layout()
    out = os.path.join(os.path.dirname(__file__), "sorting_benchmark.png")
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved {out}")


def benchmark_range_query(sizes=None):
    """Compare linear scan vs sort-then-filter for scores in [3000, 7000]. Saves range_benchmark.png."""
    if sizes is None:
        sizes = (1000, 5000, 10000, 50000, 100000)

    ms = Mergesort()
    LO, HI = 3000, 7000

    linear_times = ArrayList()
    sort_times   = ArrayList()

    print("\nRange Query Benchmark (scores in [3000, 7000])")
    print(f"{'n':>8}  {'Linear scan (s)':>17}  {'Sort+filter (s)':>16}")

    for n in sizes:
        data = generate_sessions(n)

        t0 = time.perf_counter()
        result_lin = ArrayList()
        for s in data:
            if LO <= s["score"] <= HI:
                result_lin.append(s)
        lin_time = time.perf_counter() - t0

        t0 = time.perf_counter()
        sorted_data = ms.sort(data, key=lambda x: x["score"])
        result_sf   = ArrayList()
        for s in sorted_data:
            if s["score"] < LO:
                continue
            if s["score"] > HI:
                break
            result_sf.append(s)
        sf_time = time.perf_counter() - t0

        linear_times.append(lin_time)
        sort_times.append(sf_time)
        print(f"{n:>8}  {lin_time:>17.6f}  {sf_time:>16.6f}")

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(sizes, list(linear_times), marker="o", label="Linear scan")
    ax.plot(sizes, list(sort_times),   marker="s", label="Sort then filter")
    ax.set_xlabel("Number of sessions (n)")
    ax.set_ylabel("Time (seconds)")
    ax.set_title("Range Query - Linear Scan vs Sort+Filter")
    ax.legend()
    ax.grid(True, alpha=0.4)
    fig.tight_layout()
    out = os.path.join(os.path.dirname(__file__), "range_benchmark.png")
    fig.savefig(out)
    plt.close(fig)
    print(f"  saved {out}")


if __name__ == "__main__":
    benchmark_sorting()
    benchmark_range_query()
    print("\nBenchmarks complete. Plots saved.")
