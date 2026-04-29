import random
import csv
from datetime import datetime, timedelta

# -------------------------
# CONFIG
# -------------------------

NUM_PLAYERS = 10000
NUM_SESSIONS = 100000
NUM_CHAT = 50000

GAMES = [
    ("baseball", "Baseball Dash"),
    ("ryan_game", "Ryan's Game"),
    ("chuqi_game", "Chuqi's Game"),
    ("ibrahim_game", "Ibrahim's Game"),
]

# -------------------------
# PLAYERS DATASET
# -------------------------

with open("data/players.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["player_id", "username", "password", "display_name", "country"])

    for i in range(1, NUM_PLAYERS + 1):
        pid = f"p{i:05d}"
        username = f"user{i}"
        password = "password"
        display = f"Player {i}"
        country = "USA"

        writer.writerow([pid, username, password, display, country])

print("players.csv created")

# -------------------------
# SESSIONS DATASET
# -------------------------

start_date = datetime(2025, 1, 1)

with open("data/sessions.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "session_id",
        "player_id",
        "game_id",
        "score",
        "start_time",
        "end_time",
        "outcome"
    ])

    for i in range(1, NUM_SESSIONS + 1):
        sid = f"s{i:06d}"

        player = random.randint(1, NUM_PLAYERS)
        player_id = f"p{player:05d}"

        game = random.choice(GAMES)[0]

        score = random.randint(0, 1000)

        start = start_date + timedelta(days=random.randint(0, 365))
        end = start + timedelta(minutes=random.randint(1, 30))

        outcome = random.choice(["win", "loss"])

        writer.writerow([
            sid,
            player_id,
            game,
            score,
            start.isoformat(),
            end.isoformat(),
            outcome
        ])

print("sessions.csv created")

# -------------------------
# CHAT DATASET
# -------------------------

messages = [
    "gg",
    "nice play",
    "wow",
    "that was close",
    "good game",
]

with open("data/chat.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["message_id", "player_id", "game_id", "timestamp", "content"])

    for i in range(1, NUM_CHAT + 1):
        mid = f"m{i:06d}"

        player = random.randint(1, NUM_PLAYERS)
        player_id = f"p{player:05d}"

        game = random.choice(GAMES)[0]

        time = start_date + timedelta(days=random.randint(0, 365))

        msg = random.choice(messages)

        writer.writerow([
            mid,
            player_id,
            game,
            time.isoformat(),
            msg
        ])

print("chat.csv created")

# -------------------------
# GAMES DATASET
# -------------------------

with open("data/games.csv", "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow(["game_id", "name", "team", "players", "status"])

    writer.writerow(["baseball", "Baseball Dash", "Nick", "Multiplayer", "Playable"])
    writer.writerow(["ryan_game", "Ryan's Game", "Ryan", "Multiplayer", "Playable"])
    writer.writerow(["chuqi_game", "Chuqi's Game", "Chuqi", "Multiplayer", "Playable"])
    writer.writerow(["ibrahim_game", "Ibrahim's Game", "Ibrahim", "Multiplayer", "Playable"])

print("games.csv created")