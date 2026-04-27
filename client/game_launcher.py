"""
client/game_launcher.py

Placeholder for Ryan's C++ game server connection.

The UI can call launch_game(game_id, player_id) now. Later, the inside of this
method can be replaced with a real socket connection without changing the screens.
"""


class GameLauncher:
    def __init__(self):
        self.last_message = ""

    def launch_game(self, game_id, player_id):
        # Future integration idea:
        # 1. Open socket to C++ server host/port.
        # 2. Send player_id and game_id.
        # 3. Wait for session assignment.
        # 4. Start live game loop.
        self.last_message = "Connecting player " + str(player_id) + " to game " + str(game_id) + "..."
        print(self.last_message)
        return self.last_message
