"""
platform_server/match_history_service.py - Player match history store

Author: Ibrahim Chatila
Date:   2026-04-26
Project: The Arcade — ECE 3822

Session dict schema
-------------------
{
    "session_id" : str,
    "player_id"  : str,
    "game_id"    : str,
    "start_time" : str,   # ISO-8601 date string, e.g. "2025-03-15"
    "end_time"   : str,
    "score"      : int | float,
    "outcome"    : str,   # "win" | "loss" | "draw" | …
}
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sorting.mergesort import Mergesort


class MatchHistoryService:
    """
    Stores and queries match sessions for all players on the platform.

    All sessions are kept in a flat list; queries are filtered and
    sorted on demand using the custom Mergesort implementation.
    """

    def __init__(self):
        self.__sessions = []
        self.__sorter   = Mergesort()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def add_session(self, session):
        """
        Append a session dict to the store.

        Args:
            session : dict with keys session_id, player_id, game_id,
                      start_time, end_time, score, outcome.
        """
        self.__sessions.append(session)

    def get_history(self, player_id, filters=None):
        """
        Return all sessions belonging to player_id, sorted by
        start_time (oldest first).

        Args:
            player_id : str — the player whose history to fetch.
            filters   : list of (field, value) tuples, or None.

        Returns:
            list of session dicts sorted by start_time ascending.
        """
        # Collect matching sessions
        results = []
        for s in self.__sessions:
            if s["player_id"] == player_id:
                results.append(s)

        # Apply each filter in sequence
        if filters:
            for field, value in filters:
                results = self.filter_by(results, field, value)

        # Sort by start_time (lexicographic order works for ISO dates)
        results = self.__sorter.sort(results, key=lambda s: s["start_time"])
        return results

    def filter_by(self, sessions, field, value):
        """
        Filter a list of sessions by a field/value pair.

        Supported fields
        ----------------
        "game_id"    — exact match on session["game_id"]
        "outcome"    — exact match on session["outcome"]
        "date_range" — value is (start_date, end_date) strings (inclusive)

        Args:
            sessions : list of session dicts to filter.
            field    : str — field name.
            value    : the value to filter by (str or tuple for date_range).

        Returns:
            list of matching session dicts.
        """
        result = []
        if field == "game_id":
            for s in sessions:
                if s["game_id"] == value:
                    result.append(s)

        elif field == "outcome":
            for s in sessions:
                if s["outcome"] == value:
                    result.append(s)

        elif field == "date_range":
            start_date, end_date = value
            for s in sessions:
                if start_date <= s["start_time"] <= end_date:
                    result.append(s)

        else:
            # Unknown field — return sessions unchanged
            result = sessions

        return result

    def get_all_sessions(self):
        """Return all stored sessions, unfiltered and unsorted."""
        all_s = []
        for s in self.__sessions:
            all_s.append(s)
        return all_s
