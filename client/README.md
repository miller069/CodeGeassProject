# Chuqi Pygame Client

This folder contains Chuqi Zhang's Pygame client UI for **The Arcade**.

## Run

From the project root:

```bash
pip install pygame
python client/main.py
```

Or:

```bash
cd client
python main.py
```

## Current integration

`api_client.py` directly uses the teammate Python services:

- `platform_server.account_service.AccountService`
- `platform_server.leaderboard_service.LeaderboardService`
- `platform_server.match_history_service.MatchHistoryService`

Because the real server connection is not finished yet, `api_client.py` seeds local demo data when the CSV files are empty.

## Future integration

When the Python server or C++ server is ready, update:

- `api_client.py` for real platform server requests
- `game_launcher.py` for real C++ game server connection

The Pygame screen files should not need major changes.
