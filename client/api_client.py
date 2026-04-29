"""
client/api_client.py

Bridge between Chuqi's Pygame UI and the teammate backend code.

Right now this file runs locally and directly uses the existing Python services:
- AccountService
- LeaderboardService
- MatchHistoryService

Later, if the team builds an actual socket/HTTP server, only this file should
need major changes. The Pygame screens should keep calling these same methods.
"""

import csv
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from data_structures.array_list import ArrayList
from data_structures.hash_table import HashTable
from platform_server.account_service import AccountService
from platform_server.leaderboard_service import LeaderboardService
from platform_server.match_history_service import MatchHistoryService


class GameEntry:
    """Represents one game in the catalog. Replaces a plain dict."""

    def __init__(self, game_id, name, team, players, status):
        self.game_id = str(game_id)
        self.name = str(name)
        self.team = str(team)
        self.players = str(players)
        self.status = str(status)


class LoginResult:
    """Return value from login() and create_account(). Replaces a plain dict."""

    def __init__(self, success, message, user=None):
        self.success = success
        self.message = message
        self.user = user


class LeaderboardRow:
    """One row in the leaderboard display. Replaces a plain dict."""

    def __init__(self, rank, player_id, username, score):
        self.rank = rank
        self.player_id = player_id
        self.username = username
        self.score = score


class HistoryRow:
    """One row in the match history display. Replaces a plain dict."""

    def __init__(self, game, game_id, score, date, outcome):
        self.game = game
        self.game_id = game_id
        self.score = score
        self.date = date
        self.outcome = outcome


class ProfileData:
    """Player profile statistics. Replaces a plain dict."""

    def __init__(self, player_id, username, display_name,
                 games_played, wins, losses, win_rate, total_score, favorite_game):
        self.player_id = player_id
        self.username = username
        self.display_name = display_name
        self.games_played = games_played
        self.wins = wins
        self.losses = losses
        self.win_rate = win_rate
        self.total_score = total_score
        self.favorite_game = favorite_game


class ClientPlayer:
    """Small player object that matches AccountService's expected interface."""

    def __init__(self, player_id, username, display_name=None, country="Unknown"):
        self.player_id = str(player_id)
        self.username = str(username).strip().lower()
        self.display_name = str(display_name or username).strip()
        self.country = str(country or "Unknown")

    def get_player_id(self):
        return self.player_id

    def get_username(self):
        return self.username

    def get_display_name(self):
        return self.display_name

    def is_valid(self):
        return self.player_id != "" and self.username != ""

    def to_dict(self):
        return {
            "player_id": self.player_id,
            "username": self.username,
            "display_name": self.display_name,
            "country": self.country,
        }


class ClientSession:
    """Small session object that matches LeaderboardService's expected interface."""

    def __init__(self, session_id, player_id, game_id, score, start_time, end_time, outcome):
        self.session_id = str(session_id)
        self.player_id = str(player_id)
        self.game_id = str(game_id)
        self.score = int(score)
        self.start_time = str(start_time)
        self.end_time = str(end_time)
        self.outcome = str(outcome)

    def get_session_id(self):
        return self.session_id

    def get_player_id(self):
        return self.player_id

    def get_game_id(self):
        return self.game_id

    def get_score(self):
        return self.score

    def is_valid(self):
        return self.player_id != "" and self.game_id != "" and self.score >= 0

    def to_history_dict(self):
        return {
            "session_id": self.session_id,
            "player_id": self.player_id,
            "game_id": self.game_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "score": self.score,
            "outcome": self.outcome,
        }


class ApiClient:
    """Frontend API used by Pygame screens."""

    def __init__(self):
        self.accounts = AccountService()
        self.leaderboards = LeaderboardService()
        self.match_history = MatchHistoryService()

        self.current_user = None
        self.players_by_id = HashTable()
        self.games = ArrayList()

        self._load_games()
        self._load_players()
        self._load_sessions()

    # ------------------------------------------------------------------
    # Loading / seeding data
    # ------------------------------------------------------------------

    def _data_path(self, filename):
        return os.path.join(PROJECT_ROOT, "data", filename)

    def _csv_has_rows(self, path):
        return os.path.exists(path) and os.path.getsize(path) > 0

    def _load_games(self):
        path = self._data_path("games.csv")
        if self._csv_has_rows(path):
            with open(path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    game_id = row.get("game_id") or row.get("id") or row.get("name")
                    name = row.get("name") or game_id
                    self.games.append(GameEntry(
                        game_id=str(game_id),
                        name=str(name),
                        team=row.get("team", "Code Geass"),
                        players=row.get("players", "1-10"),
                        status=row.get("status", "Playable Soon"),
                    ))

        if len(self.games) == 0:
            defaults = ArrayList()
            defaults.append(GameEntry("snake", "Snake Battle", "Code Geass", "1-10", "Mock Ready"))
            defaults.append(GameEntry("pong", "Multiplayer Pong", "Code Geass", "2-10", "Mock Ready"))
            defaults.append(GameEntry("space", "Space Shooter", "Code Geass", "1-10", "Mock Ready"))
            defaults.append(GameEntry("maze", "Maze Runner", "Code Geass", "1-10", "Mock Ready"))
            for entry in defaults:
                self.games.append(entry)

    def _add_player(self, player):
        if player.is_valid():
            self.accounts.add_player(player)
            self.players_by_id.insert(player.get_player_id(), player)

    def _load_players(self):
        path = self._data_path("players.csv")
        if self._csv_has_rows(path):
            with open(path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for index, row in enumerate(reader):
                    player_id = row.get("player_id") or row.get("id") or "p" + str(index + 1)
                    username = row.get("username") or row.get("display_name") or "player" + str(index + 1)
                    display_name = row.get("display_name") or username
                    country = row.get("country", "Unknown")
                    self._add_player(ClientPlayer(player_id, username, display_name, country))

        if not self.players_by_id.contains("p001"):
            sample_players = ArrayList()
            sample_players.append(ClientPlayer("p001", "chuqi", "Chuqi Zhang"))
            sample_players.append(ClientPlayer("p002", "ryan", "Ryan Miller"))
            sample_players.append(ClientPlayer("p003", "ibrahim", "Ibrahim Chatila"))
            sample_players.append(ClientPlayer("p004", "nicholas", "Nicholas Waller"))
            sample_players.append(ClientPlayer("p005", "alice", "Alice"))
            sample_players.append(ClientPlayer("p006", "bob", "Bob"))
            for player in sample_players:
                self._add_player(player)

    def _add_session(self, session):
        if session.is_valid():
            self.leaderboards.record_session(session)
            self.match_history.add_session(session.to_history_dict())

    def _load_sessions(self):
        path = self._data_path("sessions.csv")
        if self._csv_has_rows(path):
            with open(path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for index, row in enumerate(reader):
                    try:
                        score = int(float(row.get("score", 0) or 0))
                    except ValueError:
                        score = 0
                    if score < 0:
                        score = 0

                    session = ClientSession(
                        row.get("session_id") or "s" + str(index + 1),
                        row.get("player_id") or "p001",
                        row.get("game_id") or "snake",
                        score,
                        row.get("start_time") or row.get("date") or "2026-04-01",
                        row.get("end_time") or row.get("start_time") or "2026-04-01",
                        row.get("outcome") or "unknown",
                    )
                    self._add_session(session)

        if len(self.match_history.get_all_sessions()) == 0:
            sample_sessions = ArrayList()
            sample_sessions.append(ClientSession("s001", "p001", "snake", 760, "2026-04-20", "2026-04-20", "win"))
            sample_sessions.append(ClientSession("s002", "p002", "snake", 720, "2026-04-20", "2026-04-20", "loss"))
            sample_sessions.append(ClientSession("s003", "p003", "snake", 690, "2026-04-21", "2026-04-21", "win"))
            sample_sessions.append(ClientSession("s004", "p004", "snake", 980, "2026-04-21", "2026-04-21", "win"))
            sample_sessions.append(ClientSession("s005", "p005", "snake", 870, "2026-04-22", "2026-04-22", "loss"))
            sample_sessions.append(ClientSession("s006", "p006", "snake", 600, "2026-04-22", "2026-04-22", "loss"))
            sample_sessions.append(ClientSession("s007", "p001", "pong", 830, "2026-04-23", "2026-04-23", "loss"))
            sample_sessions.append(ClientSession("s008", "p004", "pong", 910, "2026-04-23", "2026-04-23", "win"))
            sample_sessions.append(ClientSession("s009", "p001", "maze", 640, "2026-04-24", "2026-04-24", "win"))
            for session in sample_sessions:
                self._add_session(session)

    # ------------------------------------------------------------------
    # Public methods called by the Pygame UI
    # ------------------------------------------------------------------

    def login(self, username, password):
        username = str(username).strip().lower()
        password = str(password).strip()

        if username == "" or password == "":
            return LoginResult(False, "Please enter username and password.")

        player = self.accounts.login(username)
        if player is None:
            return LoginResult(False, "User not found. Try Create instead.")

        self.current_user = player
        return LoginResult(True, "Login successful.", user=player)

    def _next_free_player_id(self):
        """Find the next unused player_id of the form pNNN.

        Using len(players_by_id) + 1 is unsafe because the dataset can have
        gaps (e.g. p001, p003, p050). If the generated id already exists,
        HashTable.insert silently overwrites the old entry, so a newly
        created account can wipe out a player that came from the CSV.
        Linear-scan from 1 until we find a free slot.
        """
        i = 1
        while True:
            candidate = "p" + str(i).zfill(3)
            if not self.players_by_id.contains(candidate):
                return candidate
            i += 1

    def create_account(self, username, password):
        username = str(username).strip().lower()
        password = str(password).strip()

        if username == "" or password == "":
            return LoginResult(False, "Username and password cannot be empty.")

        existing = self.accounts.login(username)
        if existing is not None:
            self.current_user = existing
            return LoginResult(True, "Account already exists. Logged in.", user=existing)

        player_id = self._next_free_player_id()
        player = ClientPlayer(player_id, username, username.title())
        self._add_player(player)
        self.current_user = player
        return LoginResult(True, "Account created locally.", user=player)

    def get_games(self):
        return self.games

    def get_game_name(self, game_id):
        for game in self.games:
            if game.game_id == game_id:
                return game.name
        return game_id

    def get_leaderboard(self, game_id, n=10):
        entries = self.leaderboards.get_top_n(game_id, n)
        rows = ArrayList()
        rank = 1
        for entry in entries:
            player = self.players_by_id.get(entry.player_id)
            username = entry.player_id
            if player is not None:
                username = player.get_display_name()
            rows.append(LeaderboardRow(rank, entry.player_id, username, entry.score))
            rank += 1
        return rows

    def get_profile(self, player_id):
        player = self.players_by_id.get(player_id)
        if player is None:
            return ProfileData(player_id, player_id, player_id, 0, 0, 0, "0%", 0, "None")

        sessions = self.match_history.get_history(player_id)
        games_played = len(sessions)
        wins = 0
        losses = 0
        total_score = 0
        game_counts = HashTable()

        for session in sessions:
            total_score += int(session.get("score", 0))
            outcome = str(session.get("outcome", "")).lower()
            if outcome == "win":
                wins += 1
            elif outcome == "loss":
                losses += 1
            game_id = session.get("game_id", "unknown")
            game_counts.insert(game_id, game_counts.get(game_id, 0) + 1)

        win_rate = "0%"
        if games_played > 0:
            win_rate = str(round((wins / games_played) * 100)) + "%"

        favorite_game = "None"
        best_count = -1
        for gid, count in game_counts.items():
            if count > best_count:
                favorite_game = self.get_game_name(gid)
                best_count = count

        return ProfileData(
            player.get_player_id(),
            player.get_username(),
            player.get_display_name(),
            games_played, wins, losses, win_rate, total_score, favorite_game,
        )

    def get_match_history(self, player_id):
        sessions = self.match_history.get_history(player_id)
        rows = ArrayList()
        for session in sessions:
            game_id = session.get("game_id", "unknown")
            rows.append(HistoryRow(
                game=self.get_game_name(game_id),
                game_id=game_id,
                score=session.get("score", 0),
                date=session.get("start_time", ""),
                outcome=str(session.get("outcome", "unknown")).title(),
            ))
        return rows