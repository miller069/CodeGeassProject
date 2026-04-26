"""
tests/test_trie.py - Unit tests for Trie

Author: Ibrahim Chatila
Date:   2026-04-26
Project: The Arcade — ECE 3822
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from data_structures.trie import Trie


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_insert_and_contains():
    t = Trie()
    t.insert("alice", "p001")
    assert t.contains("alice") is True,  "alice should be in trie"
    assert t.contains("ali")   is False, "ali is not a complete word"
    assert t.contains("alicee") is False, "alicee was never inserted"
    print("PASS test_insert_and_contains")


def test_prefix_search_basic():
    t = Trie()
    t.insert("alice", "p001")
    t.insert("alex",  "p002")
    t.insert("bob",   "p003")

    al_results = t.prefix_search("al")
    names = [name for name, pid in al_results]
    assert "alice" in names, "alice should appear in prefix_search('al')"
    assert "alex"  in names, "alex should appear in prefix_search('al')"
    assert "bob" not in names, "bob should NOT appear in prefix_search('al')"
    assert len(al_results) == 2

    bo_results = t.prefix_search("bo")
    assert len(bo_results) == 1
    assert bo_results[0][0] == "bob"
    print("PASS test_prefix_search_basic")


def test_prefix_search_empty_prefix():
    t = Trie()
    t.insert("alice", "p001")
    t.insert("bob",   "p002")
    t.insert("carol", "p003")

    results = t.prefix_search("")
    names = [name for name, pid in results]
    assert "alice" in names
    assert "bob"   in names
    assert "carol" in names
    assert len(results) == 3
    print("PASS test_prefix_search_empty_prefix")


def test_prefix_search_no_match():
    t = Trie()
    t.insert("alice", "p001")
    t.insert("bob",   "p002")

    results = t.prefix_search("xyz")
    assert results == [], f"Expected [], got {results}"
    print("PASS test_prefix_search_no_match")


def test_insert_duplicate():
    t = Trie()
    t.insert("alice", "p001")
    t.insert("alice", "p001_updated")   # same username, updated id

    results = t.prefix_search("alice")
    # Should still be exactly one entry
    assert len(results) == 1, f"Expected 1 result, got {len(results)}"
    assert results[0][0] == "alice"
    # player_id should be the latest one
    assert results[0][1] == "p001_updated"
    # size should still be 1
    assert t.size() == 1
    print("PASS test_insert_duplicate")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    tests = [(k, v) for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    passed = failed = 0
    for name, fn in tests:
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
