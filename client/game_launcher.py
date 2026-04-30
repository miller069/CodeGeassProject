import os
import sys
import subprocess


# change this to whoever is running game_server.py on their machine
# leave it as localhost if you are the one running the server
GAME_SERVER_HOST = 'localhost'
GAME_SERVER_PORT = 8080


class GameLauncher:
    def __init__(self):
        self.last_message = ""
        self.client_dir = os.path.dirname(__file__)

    def launch_game(self, game_id, player_id):
        if game_id == "baseball":
            game_dir = os.path.join(
                self.client_dir,
                "Games",
                "baseball dash",
                "code",
                "game"
            )

            main_file = os.path.join(game_dir, "main.py")

            if not os.path.isfile(main_file):
                self.last_message = "Could not find baseball game main.py"
                return self.last_message

            subprocess.Popen(
                [sys.executable, main_file, str(player_id)],
                cwd=game_dir
            )

            self.last_message = "Launched Baseball Game"
            return self.last_message

        elif game_id == "ibrahim_game":
            game_dir = os.path.join(
                self.client_dir,
                "Games",
                "npc-dialog"
            )

            main_file = os.path.join(game_dir, "main.py")

            if not os.path.isfile(main_file):
                self.last_message = "Could not find npc-dialog game main.py"
                return self.last_message

            subprocess.Popen(
                [sys.executable, main_file, str(player_id),
                 '--server', GAME_SERVER_HOST,
                 '--port', str(GAME_SERVER_PORT)],
                cwd=game_dir
            )

            self.last_message = "Launched NPC Dialog Game"
            return self.last_message

        elif game_id == "chuqi_game":
            game_dir = os.path.join(
                self.client_dir,
                "Games",
                "chuqi-game"
            )

            main_file = os.path.join(game_dir, "main.py")

            if not os.path.isfile(main_file):
                self.last_message = "Could not find chuqi game main.py"
                return self.last_message

            subprocess.Popen(
                [sys.executable, main_file, str(player_id)],
                cwd=game_dir
            )

            self.last_message = "Launched Chuqi's Game"
            return self.last_message

        self.last_message = "Game not connected yet: " + str(game_id)
        return self.last_message