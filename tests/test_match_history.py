"""
tests/test_match_history.py - Unit tests for MatchHistoryService

Author: Ibrahim Chatila
Date:   2026-04-26
Project: The Arcade — ECE 3822
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from platform_server.match_history_service import MatchHistoryService


def _make_session(sid, pid, gid, start, end, score, outcome):
    return {
        "session_id": sid,
        "player_id":  pid,
        "game_id":    gid,
        "start_time": start,
        "end_time":   end,
        "score":      score,
        "outcome":    outcome,
    }


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_add_and_get_history():
    svc = MatchHistoryService()
    svc.add_session(_make_session("s1", "p1", "snake",   "2025-02-01", "2025-02-01", 100, "win"))
    svc.add_session(_make_session("s2", "p1", "tetris",  "2025-03-01", "2025-03-01", 200, "loss"))
    svc.add_session(_make_session("s3", "p1", "pong",    "2025-04-01", "2025-04-01", 150, "win"))
    svc.add_session(_make_session("s4", "p2", "snake",   "2025-02-15", "2025-02-15", 300, "win"))
    svc.add_session(_make_session("s5", "p2", "tetris",  "2025-03-20", "2025-03-20",  50, "loss"))

    p1_history = svc.get_history("p1")
    assert len(p1_history) == 3, f"Expected 3 sessions for p1, got {len(p1_history)}"
    print("PASS test_add_and_get_history")


def test_results_sorted_by_date():
    svc = MatchHistoryService()
    # Insert out-of-order
    svc.add_session(_make_session("s3", "p1", "snake",  "2025-04-01", "2025-04-01", 150, "win"))
    svc.add_session(_make_session("s1", "p1", "snake",  "2025-01-01", "2025-01-01", 100, "loss"))
    svc.add_session(_make_session("s2", "p1", "tetris", "2025-02-15", "2025-02-15", 200, "win"))

    history = svc.get_history("p1")
    dates = [s["start_time"] for s in history]
    assert dates == ["2025-01-01", "2025-02-15", "2025-04-01"], \
        f"Dates not sorted: {dates}"
    print("PASS test_results_sorted_by_date")


def test_filter_by_game():
    svc = MatchHistoryService()
    svc.add_session(_make_session("s1", "p1", "snake",  "2025-01-01", "2025-01-01", 100, "win"))
    svc.add_session(_make_session("s2", "p1", "tetris", "2025-02-01", "2025-02-01", 200, "loss"))
    svc.add_session(_make_session("s3", "p1", "snake",  "2025-03-01", "2025-03-01", 150, "win"))

    all_p1 = svc.get_history("p1")
    snake_sessions = svc.filter_by(all_p1, "game_id", "snake")
    assert len(snake_sessions) == 2, f"Expected 2 snake sessions, got {len(snake_sessions)}"
    for s in snake_sessions:
        assert s["game_id"] == "snake"
    print("PASS test_filter_by_game")


def test_filter_by_outcome():
    svc = MatchHistoryService()
    svc.add_session(_make_session("s1", "p1", "snake",  "2025-01-01", "2025-01-01", 100, "win"))
    svc.add_session(_make_session("s2", "p1", "snake",  "2025-02-01", "2025-02-01", 200, "loss"))
    svc.add_session(_make_session("s3", "p1", "snake",  "2025-03-01", "2025-03-01", 150, "win"))

    all_p1 = svc.get_history("p1")
    wins = svc.filter_by(all_p1, "outcome", "win")
    assert len(wins) == 2, f"Expected 2 wins, got {len(wins)}"
    for s in wins:
        assert s["outcome"] == "win"
    print("PASS test_filter_by_outcome")


def test_filter_by_date_range():
    svc = MatchHistoryService()
    svc.add_session(_make_session("s1", "p1", "pong", "2024-12-01", "2024-12-01", 80,  "loss"))
    svc.add_session(_make_session("s2", "p1", "pong", "2025-02-10", "2025-02-10", 120, "win"))
    svc.add_session(_make_session("s3", "p1", "pong", "2025-05-20", "2025-05-20", 200, "win"))
    svc.add_session(_make_session("s4", "p1", "pong", "2026-01-01", "2026-01-01", 90,  "loss"))

    all_p1 = svc.get_history("p1")
    in_range = svc.filter_by(all_p1, "date_range", ("2025-01-01", "2025-06-01"))
    assert len(in_range) == 2, f"Expected 2 sessions in range, got {len(in_range)}"
    for s in in_range:
        assert "2025-01-01" <= s["start_time"] <= "2025-06-01"
    print("PASS test_filter_by_date_range")


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
