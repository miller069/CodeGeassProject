"""
client/api_client.py

Simple bridge between the Pygame UI and backend services.
Uses custom ArrayList and HashTable instead of Python lists/dicts.
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from data_structures.array_list import ArrayList
from data_structures.hash_table import HashTable
from platform_server.account_service import AccountService
from platform_server.leaderboard_service import LeaderboardService


class GameEntry:
    def __init__(self, game_id, name, team, players, status):
        self.game_id = str(game_id)
        self.name = str(name)
        self.team = str(team)
        self.players = str(players)
        self.status = str(status)


class LoginResult:
    def __init__(self, success, message, user=None):
        self.success = success
        self.message = message
        self.user = user


class LeaderboardRow:
    def __init__(self, rank, player_id, username, score):
        self.rank = rank
        self.player_id = player_id
        self.username = username
        self.score = score


class HistoryRow:
    def __init__(self, game, game_id, score, date, outcome):
        self.game = game
        self.game_id = game_id
        self.score = score
        self.date = date
        self.outcome = outcome


class ProfileData:
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
    def __init__(self, player_id, username, password, display_name=None, country="Unknown"):
        self.player_id = str(player_id)
        self.username = str(username).strip().lower()
        self.password = str(password).strip()
        self.display_name = str(display_name or username).strip()
        self.country = str(country or "Unknown")

    def get_player_id(self):
        return self.player_id

    def get_username(self):
        return self.username

    def get_display_name(self):
        return self.display_name

    def check_password(self, password):
        return self.password == str(password).strip()

    def is_valid(self):
        return self.player_id != "" and self.username != "" and self.password != ""


class ClientSession:
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


class ApiClient:
    def __init__(self):
        self.accounts = AccountService()
        self.leaderboards = LeaderboardService()

        self.current_user = None
        self.players_by_id = HashTable()
        self.sessions = ArrayList()
        self.games = ArrayList()

        self._load_games()
        self._load_players()
        self._load_sessions()

    def _data_path(self, filename):
        return os.path.join(PROJECT_ROOT, "data", filename)

    def _csv_has_rows(self, path):
        return os.path.exists(path) and os.path.getsize(path) > 0

    def _get_field(self, line, index):
        current_index = 0
        field = ""

        for ch in line:
            if ch == ",":
                if current_index == index:
                    return field.strip()
                current_index += 1
                field = ""
            else:
                field += ch

        if current_index == index:
            return field.strip()

        return ""

    def _find_column(self, header, name):
        index = 0
        current = ""

        for ch in header:
            if ch == ",":
                if current.strip().lower() == name:
                    return index
                index += 1
                current = ""
            else:
                current += ch

        if current.strip().lower() == name:
            return index

        return -1

    def _add_player(self, player):
        if player.is_valid():
            self.accounts.add_player(player)
            self.players_by_id.insert(player.get_player_id(), player)

    def _add_session(self, session):
        if session.is_valid():
            self.sessions.append(session)
            self.leaderboards.record_session(session)

    def _load_games(self):
        path = self._data_path("games.csv")

        if self._csv_has_rows(path):
            with open(path, "r", encoding="utf-8") as file:
                header = file.readline().strip()

                game_id_col = self._find_column(header, "game_id")
                name_col = self._find_column(header, "name")
                team_col = self._find_column(header, "team")
                players_col = self._find_column(header, "players")
                status_col = self._find_column(header, "status")

                for line in file:
                    line = line.strip()

                    if line != "":
                        game_id = self._get_field(line, game_id_col)
                        name = self._get_field(line, name_col)
                        team = self._get_field(line, team_col)
                        players = self._get_field(line, players_col)
                        status = self._get_field(line, status_col)

                        if players == "" or players == "1-10":
                            players = "Multiplayer"

                        if status == "":
                            status = "Playable"

                        self.games.append(GameEntry(game_id, name, team, players, status))

        if len(self.games) == 0:
            self.games.append(GameEntry("baseball", "Baseball Dash", "Nick", "Multiplayer", "Playable"))
            self.games.append(GameEntry("ryan_game", "Ryan's Game", "Ryan", "Multiplayer", "Playable"))
            self.games.append(GameEntry("chuqi_game", "Chuqi's Game", "Chuqi", "Multiplayer", "Playable"))
            self.games.append(GameEntry("ibrahim_game", "Ibrahim's Game", "Ibrahim", "Multiplayer", "Playable"))

    def _load_players(self):
        path = self._data_path("players.csv")

        if self._csv_has_rows(path):
            with open(path, "r", encoding="utf-8") as file:
                header = file.readline().strip()

                id_col = self._find_column(header, "player_id")
                username_col = self._find_column(header, "username")
                password_col = self._find_column(header, "password")
                display_col = self._find_column(header, "display_name")
                country_col = self._find_column(header, "country")

                index = 1

                for line in file:
                    line = line.strip()

                    if line != "":
                        player_id = self._get_field(line, id_col)
                        username = self._get_field(line, username_col)
                        password = self._get_field(line, password_col)
                        display_name = self._get_field(line, display_col)
                        country = self._get_field(line, country_col)

                        if player_id == "":
                            player_id = "p" + str(index).zfill(3)

                        if password == "":
                            password = "password"

                        self._add_player(ClientPlayer(player_id, username, password, display_name, country))
                        index += 1

        

    def _load_sessions(self):
        path = self._data_path("sessions.csv")

        if self._csv_has_rows(path):
            with open(path, "r", encoding="utf-8") as file:
                header = file.readline().strip()

                session_col = self._find_column(header, "session_id")
                player_col = self._find_column(header, "player_id")
                game_col = self._find_column(header, "game_id")
                score_col = self._find_column(header, "score")
                start_col = self._find_column(header, "start_time")
                end_col = self._find_column(header, "end_time")
                outcome_col = self._find_column(header, "outcome")

                index = 1

                for line in file:
                    line = line.strip()

                    if line != "":
                        session_id = self._get_field(line, session_col)
                        player_id = self._get_field(line, player_col)
                        game_id = self._get_field(line, game_col)
                        score_text = self._get_field(line, score_col)
                        start_time = self._get_field(line, start_col)
                        end_time = self._get_field(line, end_col)
                        outcome = self._get_field(line, outcome_col)

                        if session_id == "":
                            session_id = "s" + str(index).zfill(3)

                        try:
                            score = int(float(score_text))
                        except ValueError:
                            score = 0

                        if score < 0:
                            score = 0

                        self._add_session(ClientSession(
                            session_id,
                            player_id,
                            game_id,
                            score,
                            start_time,
                            end_time,
                            outcome
                        ))

                        index += 1

        if len(self.sessions) == 0:
            self._add_session(ClientSession("s001", "p001", "ibrahim_game", 760, "2026-04-20", "2026-04-20", "win"))
            self._add_session(ClientSession("s002", "p002", "ibrahim_game", 720, "2026-04-20", "2026-04-20", "loss"))
            self._add_session(ClientSession("s003", "p003", "ibrahim_game", 690, "2026-04-21", "2026-04-21", "win"))

    def _next_free_player_id(self):
        i = 1

        while True:
            player_id = "p" + str(i).zfill(3)

            if not self.players_by_id.contains(player_id):
                return player_id

            i += 1

    def _save_new_player(self, player):
        path = self._data_path("players.csv")
        file_exists = os.path.exists(path)

        with open(path, "a", encoding="utf-8") as file:
            if not file_exists or os.path.getsize(path) == 0:
                file.write("player_id,username,password,display_name,country\n")

            file.write(
                player.get_player_id() + "," +
                player.get_username() + "," +
                player.password + "," +
                player.get_display_name() + "," +
                player.country + "\n"
            )

    def login(self, username, password):
        username = str(username).strip().lower()
        password = str(password).strip()

        if username == "" or password == "":
            return LoginResult(False, "Please enter username and password.")

        player = self.accounts.login(username)

        if player is None:
            return LoginResult(False, "User not found. Try Create instead.")

        if not player.check_password(password):
            return LoginResult(False, "Incorrect password.")

        self.current_user = player
        return LoginResult(True, "Login successful.", player)

    def create_account(self, username, password):
        username = str(username).strip().lower()
        password = str(password).strip()

        if username == "" or password == "":
            return LoginResult(False, "Username and password cannot be empty.")

        existing = self.accounts.login(username)

        if existing is not None:
            return LoginResult(False, "Account already exists. Please log in.")

        player_id = self._next_free_player_id()
        player = ClientPlayer(player_id, username, password, username.title())

        self._add_player(player)
        self._save_new_player(player)

        self.current_user = player
        return LoginResult(True, "Account created.", player)

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

        games_played = 0
        wins = 0
        losses = 0
        total_score = 0
        favorite_game = "None"

        game_counts = HashTable()

        for session in self.sessions:
            if session.get_player_id() == player_id:
                games_played += 1
                total_score += session.get_score()

                outcome = session.outcome.lower()

                if outcome == "win":
                    wins += 1
                elif outcome == "loss":
                    losses += 1

                old_count = game_counts.get(session.get_game_id(), 0)
                game_counts.insert(session.get_game_id(), old_count + 1)

        best_count = -1

        for game_id, count in game_counts.items():
            if count > best_count:
                best_count = count
                favorite_game = self.get_game_name(game_id)

        win_rate = "0%"

        if games_played > 0:
            win_rate = str(round((wins / games_played) * 100)) + "%"

        return ProfileData(
            player.get_player_id(),
            player.get_username(),
            player.get_display_name(),
            games_played,
            wins,
            losses,
            win_rate,
            total_score,
            favorite_game
        )

    def get_match_history(self, player_id):
        rows = ArrayList()

        for session in self.sessions:
            if session.get_player_id() == player_id:
                rows.append(HistoryRow(
                    self.get_game_name(session.get_game_id()),
                    session.get_game_id(),
                    session.get_score(),
                    session.start_time,
                    session.outcome.title()
                ))

        return rows