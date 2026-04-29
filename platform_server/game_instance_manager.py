"""
Manages active game sessions on the platform.
Each session tracks which players are connected and what game is running.
No player cap is enforced by default — sessions accept as many players
as connect. A per-game cap can optionally be set at creation time.

Author: Ibrahim Chatila
Date: 2026-04-26
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from data_structures.array_list import ArrayList


class GameSession:
    """Represents one active game instance with its connected players."""

    def __init__(self, session_id, game_id, max_players=None):
        """
        Create a new game session.

        Args:
            session_id:  unique identifier for this session.
            game_id:     which game is being played.
            max_players: optional player cap. None means unlimited.
        """
        self.session_id  = session_id
        self.game_id     = game_id
        self.max_players = max_players  # None = unlimited
        self._players    = ArrayList()

    def add_player(self, player_id):
        """
        Add a player to this session.
        Returns True on success, False if the session is full.
        """
        if self.max_players is not None and len(self._players) >= self.max_players:
            return False
        for pid in self._players:
            if pid == player_id:
                return True  # already in session
        self._players.append(player_id)
        return True

    def remove_player(self, player_id):
        """Remove a player from the session. Does nothing if not found."""
        for i in range(len(self._players)):
            if self._players[i] == player_id:
                self._players.pop(i)
                return

    def has_player(self, player_id):
        return player_id in self._players

    def player_count(self):
        return len(self._players)

    def is_full(self):
        """Returns True only if a cap is set and it has been reached."""
        if self.max_players is None:
            return False
        return len(self._players) >= self.max_players

    def get_players(self):
        """Return an ArrayList of all player IDs in this session."""
        result = ArrayList()
        for pid in self._players:
            result.append(pid)
        return result

    def __str__(self):
        return (f"GameSession(id={self.session_id}, game={self.game_id}, "
                f"players={len(self._players)}, cap={self.max_players})")


class GameInstanceManager:
    """
    Tracks all active game sessions on the platform.
    Sessions have no player cap by default. A cap can be passed
    per session if the game design requires one.
    """

    def __init__(self):
        self._sessions = ArrayList()

    def create_session(self, session_id, game_id, max_players=None):
        """
        Create and register a new game session.

        Args:
            session_id:  unique session identifier.
            game_id:     game being played.
            max_players: optional cap. Leave as None for unlimited players.

        Returns:
            The new GameSession, or None if session_id already exists.
        """
        if self.get_session(session_id) is not None:
            return None
        session = GameSession(session_id, game_id, max_players=max_players)
        self._sessions.append(session)
        return session

    def get_session(self, session_id):
        """Return the GameSession with the given ID, or None if not found."""
        for session in self._sessions:
            if session.session_id == session_id:
                return session
        return None

    def remove_session(self, session_id):
        """Remove a session by ID. Does nothing if not found."""
        for i in range(len(self._sessions)):
            if self._sessions[i].session_id == session_id:
                self._sessions.pop(i)
                return

    def join_session(self, session_id, player_id):
        """
        Add a player to an existing session.
        Returns True on success, False if session not found or is full.
        """
        session = self.get_session(session_id)
        if session is None:
            return False
        return session.add_player(player_id)

    def leave_session(self, session_id, player_id):
        """Remove a player from a session."""
        session = self.get_session(session_id)
        if session is not None:
            session.remove_player(player_id)

    def active_session_count(self):
        return len(self._sessions)

    def get_all_sessions(self):
        """Return an ArrayList of all active GameSession objects."""
        result = ArrayList()
        for session in self._sessions:
            result.append(session)
        return result
