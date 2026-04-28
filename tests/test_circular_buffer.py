"""
Unit tests for CircularBuffer.

Author: Ibrahim Chatila
Date: 2026-04-26
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from data_structures.circular_buffer import CircularBuffer
from data_structures.array_list import ArrayList


def test_push_and_get_recent():
    buf = CircularBuffer(5)
    buf.push("a")
    buf.push("b")
    buf.push("c")
    result = buf.get_recent(3)
    assert len(result) == 3 and result[0] == "a" and result[1] == "b" and result[2] == "c", f"Expected ['a','b','c'], got {result}"
    print("PASS test_push_and_get_recent")


def test_overwrite_when_full():
    buf = CircularBuffer(3)
    buf.push(1)
    buf.push(2)
    buf.push(3)
    buf.push(4)  # should overwrite 1
    result = buf.get_recent(3)
    assert len(result) == 3 and result[0] == 2 and result[1] == 3 and result[2] == 4, f"Expected [2,3,4], got {result}"
    print("PASS test_overwrite_when_full")


def test_get_recent_fewer_than_n():
    buf = CircularBuffer(5)
    buf.push("x")
    buf.push("y")
    result = buf.get_recent(5)
    assert len(result) == 2 and result[0] == "x" and result[1] == "y", f"Expected ['x','y'], got {result}"
    print("PASS test_get_recent_fewer_than_n")


def test_is_full():
    buf = CircularBuffer(3)
    assert not buf.is_full()
    buf.push(1)
    buf.push(2)
    assert not buf.is_full()
    buf.push(3)
    assert buf.is_full(), "Buffer should be full after 3 pushes into capacity-3"
    print("PASS test_is_full")


def test_is_empty():
    buf = CircularBuffer(4)
    assert buf.is_empty(), "New buffer should be empty"
    buf.push("hello")
    assert not buf.is_empty(), "Buffer should not be empty after push"
    print("PASS test_is_empty")


if __name__ == "__main__":
    all_tests = ArrayList()
    for name in sorted(dir()):
        obj = globals().get(name)
        if name.startswith("test_") and callable(obj):
            all_tests.append((name, obj))

    passed = 0
    failed = 0
    for name, fn in all_tests:
        try:
            fn()
            passed += 1
        except Exception as exc:
            print(f"FAIL {name}: {exc}")
            failed += 1
    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed / {passed+failed} total")
    if failed:
        raise SystemExit(1)
    print("All tests passed!")
