import os
import sys
import random
import time
import csv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from data_structures.hash_table import HashTable
from data_structures.max_heap import MaxHeap
from data_structures.avl_tree import AVLTree


SIZES = [100, 500, 1000, 5000, 10000, 25000]
TRIALS = 3


def time_function(func):
    start = time.perf_counter()
    func()
    end = time.perf_counter()
    return end - start


def average_time(func):
    total = 0
    for _ in range(TRIALS):
        total += time_function(func)
    return total / TRIALS


def benchmark_hash_table(n):
    keys = [f"user_{i}" for i in range(n)]

    def insert_test():
        table = HashTable()
        for key in keys:
            table.insert(key, random.randint(0, 100000))

    table = HashTable()
    for key in keys:
        table.insert(key, random.randint(0, 100000))

    def get_test():
        for key in keys:
            table.get(key)

    def contains_test():
        for key in keys:
            table.contains(key)

    return {
        "hash_insert": average_time(insert_test),
        "hash_get": average_time(get_test),
        "hash_contains": average_time(contains_test),
    }


def benchmark_max_heap(n):
    values = [random.randint(0, 1000000) for _ in range(n)]

    def insert_test():
        heap = MaxHeap()
        for value in values:
            heap.insert(value)

    heap = MaxHeap()
    for value in values:
        heap.insert(value)

    def extract_test():
        copied = heap.copy()
        for _ in range(min(100, n)):
            copied.extract_max()

    return {
        "heap_insert": average_time(insert_test),
        "heap_extract_top_100": average_time(extract_test),
    }


def benchmark_avl_tree(n):
    values = [random.randint(0, 1000000) for _ in range(n)]

    def insert_test():
        tree = AVLTree()
        for value in values:
            tree.insert(value, value)

    tree = AVLTree()
    for value in values:
        tree.insert(value, value)

    low = 250000
    high = 750000

    def range_query_test():
        tree.range_query(low, high)

    def rank_test():
        for _ in range(100):
            tree.rank_of_key_descending(random.choice(values))

    def linear_range_test():
        result = []
        for value in values:
            if low <= value <= high:
                result.append(value)

    return {
        "avl_insert": average_time(insert_test),
        "avl_range_query": average_time(range_query_test),
        "avl_rank_lookup_100": average_time(rank_test),
        "linear_range_scan": average_time(linear_range_test),
    }


def run_benchmarks():
    rows = []

    for n in SIZES:
        print(f"Running data structure benchmarks for n={n}...")

        results = {"n": n}
        results.update(benchmark_hash_table(n))
        results.update(benchmark_max_heap(n))
        results.update(benchmark_avl_tree(n))

        rows.append(results)

    output_path = os.path.join(PROJECT_ROOT, "tests", "benchmark_datastructures_results.csv")

    with open(output_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nDone. Results saved to: {output_path}")


if __name__ == "__main__":
    run_benchmarks()