"""
Stores and queries player match sessions.
No built-in list or dict used as a high-level data structure.

Session fields: session_id, player_id, game_id, start_time, end_time, score, outcome

Author: Ibrahim Chatila
Date: 2026-04-26
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from data_structures.array_list import ArrayList
from sorting.mergesort import Mergesort


class MatchHistoryService:

    def __init__(self):
        self.__sessions = ArrayList()
        self.__sorter   = Mergesort()

    def add_session(self, session):
        self.__sessions.append(session)

    def get_history(self, player_id, filters=None):
        """Return all sessions for a player sorted by start_time ascending."""
        results = ArrayList()
        for session in self.__sessions:
            if session["player_id"] == player_id:
                results.append(session)

        if filters:
            for field, value in filters:
                results = self.filter_by(results, field, value)

        results = self.__sorter.sort(results, key=lambda s: s["start_time"])
        return results

    def filter_by(self, sessions, field, value):
        """
        Filter sessions by field and value.
        Supported fields: game_id, outcome, date_range (value is a (start, end) tuple).
        """
        result = ArrayList()

        if field == "game_id":
            for session in sessions:
                if session["game_id"] == value:
                    result.append(session)

        elif field == "outcome":
            for session in sessions:
                if session["outcome"] == value:
                    result.append(session)

        elif field == "date_range":
            start_date, end_date = value
            for session in sessions:
                if start_date <= session["start_time"] <= end_date:
                    result.append(session)

        else:
            for session in sessions:
                result.append(session)

        return result

    def get_all_sessions(self):
        all_sessions = ArrayList()
        for session in self.__sessions:
            all_sessions.append(session)
        return all_sessions
