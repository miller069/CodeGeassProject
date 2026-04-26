"""
sorting/benchmark.py - Performance benchmarks for Mergesort and Heapsort

Author: Ibrahim Chatila
Date:   2026-04-26
Project: The Arcade — ECE 3822

Run:
    cd CodeGeassProject
    python sorting/benchmark.py
"""

import time
import random
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import matplotlib
matplotlib.use("Agg")   # non-interactive backend — works without a display
import matplotlib.pyplot as plt

from sorting.mergesort import Mergesort
from sorting.heapsort  import Heapsort

SEED = 42


# ---------------------------------------------------------------------------
# Data generator
# ---------------------------------------------------------------------------

def generate_sessions(n, seed=SEED):
    """Generate n fake session dicts with random scores, dates, player_ids."""
    rng      = random.Random(seed)
    sessions = []
    games    = ["snake", "tetris", "pong", "pacman", "breakout"]
    outcomes = ["win", "loss", "draw"]
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


# ---------------------------------------------------------------------------
# Benchmark 1 — Sorting speed
# ---------------------------------------------------------------------------

def benchmark_sorting(sizes=None):
    """
    Time Mergesort vs Heapsort on score field across several dataset sizes.
    Saves the plot as sorting_benchmark.png.
    """
    if sizes is None:
        sizes = [1000, 5000, 10000, 50000, 100000]

    ms = Mergesort()
    hs = Heapsort()

    ms_times = []
    hs_times = []

    print("\n--- Sorting Benchmark ---")
    print(f"{'n':>8}  {'Mergesort (s)':>15}  {'Heapsort (s)':>14}")
    print("-" * 42)

    for n in sizes:
        data = generate_sessions(n)

        t0 = time.perf_counter()
        ms.sort(data, key=lambda x: x["score"])
        t1 = time.perf_counter()
        ms_time = t1 - t0

        t0 = time.perf_counter()
        hs.sort(data, key=lambda x: x["score"])
        t1 = time.perf_counter()
        hs_time = t1 - t0

        ms_times.append(ms_time)
        hs_times.append(hs_time)
        print(f"{n:>8}  {ms_time:>15.6f}  {hs_time:>14.6f}")

    # Plot
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(sizes, ms_times, marker="o", label="Mergesort")
    ax.plot(sizes, hs_times, marker="s", label="Heapsort")
    ax.set_xlabel("Number of sessions (n)")
    ax.set_ylabel("Time (seconds)")
    ax.set_title("Sorting Benchmark — Mergesort vs Heapsort (sort by score)")
    ax.legend()
    ax.grid(True, alpha=0.4)
    fig.tight_layout()
    out = os.path.join(os.path.dirname(__file__), "sorting_benchmark.png")
    fig.savefig(out)
    plt.close(fig)
    print(f"  → saved {out}")


# ---------------------------------------------------------------------------
# Benchmark 2 — Range query: linear scan vs sort-then-filter
# ---------------------------------------------------------------------------

def benchmark_range_query(sizes=None):
    """
    Compare linear scan vs mergesort-then-filter for finding scores in
    [3000, 7000].  Saves the plot as range_benchmark.png.
    """
    if sizes is None:
        sizes = [1000, 5000, 10000, 50000, 100000]

    ms = Mergesort()
    LO, HI = 3000, 7000

    linear_times = []
    sort_times   = []

    print("\n--- Range Query Benchmark (scores in [3000, 7000]) ---")
    print(f"{'n':>8}  {'Linear scan (s)':>17}  {'Sort+filter (s)':>16}")
    print("-" * 46)

    for n in sizes:
        data = generate_sessions(n)

        # Linear scan
        t0 = time.perf_counter()
        result_lin = []
        for s in data:
            if LO <= s["score"] <= HI:
                result_lin.append(s)
        t1 = time.perf_counter()
        lin_time = t1 - t0

        # Sort then filter
        t0 = time.perf_counter()
        sorted_data = ms.sort(data, key=lambda x: x["score"])
        result_sf   = []
        for s in sorted_data:
            if s["score"] < LO:
                continue
            if s["score"] > HI:
                break
            result_sf.append(s)
        t1 = time.perf_counter()
        sf_time = t1 - t0

        linear_times.append(lin_time)
        sort_times.append(sf_time)
        print(f"{n:>8}  {lin_time:>17.6f}  {sf_time:>16.6f}")

    # Plot
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(sizes, linear_times, marker="o", label="Linear scan")
    ax.plot(sizes, sort_times,   marker="s", label="Sort then filter")
    ax.set_xlabel("Number of sessions (n)")
    ax.set_ylabel("Time (seconds)")
    ax.set_title("Range Query Benchmark — Linear Scan vs Sort+Filter")
    ax.legend()
    ax.grid(True, alpha=0.4)
    fig.tight_layout()
    out = os.path.join(os.path.dirname(__file__), "range_benchmark.png")
    fig.savefig(out)
    plt.close(fig)
    print(f"  → saved {out}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    benchmark_sorting()
    benchmark_range_query()
    print("\nBenchmarks complete. Plots saved.")
