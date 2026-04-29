"""
Unit tests for GameInstanceManager and GameSession.

Author: Ibrahim Chatila
Date: 2026-04-26
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from platform_server.game_instance_manager import GameInstanceManager
from data_structures.array_list import ArrayList


def test_create_session():
    mgr = GameInstanceManager()
    s = mgr.create_session("s1", "snake")
    assert s is not None
    assert s.session_id == "s1"
    assert s.game_id == "snake"
    assert s.max_players is None  # no cap by default
    print("PASS test_create_session")


def test_no_player_cap_by_default():
    mgr = GameInstanceManager()
    mgr.create_session("s1", "tetris")
    # add way more than 10 players to prove there is no hardcoded cap
    for i in range(50):
        result = mgr.join_session("s1", f"p{i}")
        assert result is True, f"Player p{i} should have joined but was rejected"
    assert mgr.get_session("s1").player_count() == 50
    print("PASS test_no_player_cap_by_default")


def test_configurable_cap():
    mgr = GameInstanceManager()
    mgr.create_session("s1", "pong", max_players=3)
    assert mgr.join_session("s1", "p1") is True
    assert mgr.join_session("s1", "p2") is True
    assert mgr.join_session("s1", "p3") is True
    assert mgr.join_session("s1", "p4") is False  # cap reached
    assert mgr.get_session("s1").player_count() == 3
    print("PASS test_configurable_cap")


def test_join_and_leave():
    mgr = GameInstanceManager()
    mgr.create_session("s1", "snake")
    mgr.join_session("s1", "p1")
    mgr.join_session("s1", "p2")
    assert mgr.get_session("s1").player_count() == 2
    mgr.leave_session("s1", "p1")
    assert mgr.get_session("s1").player_count() == 1
    assert not mgr.get_session("s1").has_player("p1")
    print("PASS test_join_and_leave")


def test_duplicate_join():
    mgr = GameInstanceManager()
    mgr.create_session("s1", "snake")
    mgr.join_session("s1", "p1")
    mgr.join_session("s1", "p1")  # joining again should not duplicate
    assert mgr.get_session("s1").player_count() == 1
    print("PASS test_duplicate_join")


def test_remove_session():
    mgr = GameInstanceManager()
    mgr.create_session("s1", "snake")
    mgr.create_session("s2", "pong")
    mgr.remove_session("s1")
    assert mgr.get_session("s1") is None
    assert mgr.get_session("s2") is not None
    assert mgr.active_session_count() == 1
    print("PASS test_remove_session")


def test_duplicate_session_id():
    mgr = GameInstanceManager()
    s1 = mgr.create_session("s1", "snake")
    s2 = mgr.create_session("s1", "pong")  # duplicate ID
    assert s1 is not None
    assert s2 is None  # should be rejected
    assert mgr.active_session_count() == 1
    print("PASS test_duplicate_session_id")


def test_is_full():
    mgr = GameInstanceManager()
    mgr.create_session("s1", "snake", max_players=2)
    assert not mgr.get_session("s1").is_full()
    mgr.join_session("s1", "p1")
    mgr.join_session("s1", "p2")
    assert mgr.get_session("s1").is_full()
    print("PASS test_is_full")


def test_unlimited_session_never_full():
    mgr = GameInstanceManager()
    mgr.create_session("s1", "snake")  # no cap
    for i in range(100):
        mgr.join_session("s1", f"p{i}")
    assert not mgr.get_session("s1").is_full()
    print("PASS test_unlimited_session_never_full")


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
