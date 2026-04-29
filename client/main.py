"""
client/main.py

Chuqi Zhang's Pygame client.

Run from the project root:
    python client/main.py

Or run from inside client/:
    cd client
    python main.py
"""

import pygame
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from api_client import ApiClient
from game_launcher import GameLauncher
from screens.login_screen import LoginScreen
from screens.catalog_screen import CatalogScreen
from screens.profile_screen import ProfileScreen
from screens.leaderboard_screen import LeaderboardScreen
from screens.match_history_screen import MatchHistoryScreen
from data_structures.hash_table import HashTable


class ArcadeClientApp:
    def __init__(self):
        pygame.init()

        self.width = 900
        self.height = 640
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("The Arcade - Pygame Client")

        self.clock = pygame.time.Clock()
        self.running = True

        self.title_font = pygame.font.SysFont("arial", 40, bold=True)
        self.font = pygame.font.SysFont("arial", 24)
        self.small_font = pygame.font.SysFont("arial", 18)

        self.api = ApiClient()
        self.launcher = GameLauncher()

        self.current_user = None
        self.selected_game_id = "snake"

        self.screens = HashTable()
        self.current_screen = None
        self.current_screen_name = "login"

        self.build_screens()
        self.change_screen("login")

    def build_screens(self):
        self.screens.insert("login", LoginScreen(self))
        self.screens.insert("catalog", CatalogScreen(self))
        self.screens.insert("profile", ProfileScreen(self))
        self.screens.insert("leaderboard", LeaderboardScreen(self))
        self.screens.insert("history", MatchHistoryScreen(self))

    def change_screen(self, name):
        if self.screens.contains(name):
            self.current_screen_name = name
            self.current_screen = self.screens.get(name)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.current_screen is not None:
                self.current_screen.handle_event(event)

    def update(self):
        if self.current_screen is not None:
            self.current_screen.update()

    def draw(self):
        if self.current_screen is not None:
            self.current_screen.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    app = ArcadeClientApp()
    app.run()
