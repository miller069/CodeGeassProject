import os
import sys
import pygame

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ui_helpers import BACKGROUND, CARD, BLACK, DARK_GRAY, BLUE, Button, draw_text
from data_structures.array_list import ArrayList


class CatalogScreen:
    def __init__(self, app):
        self.app = app
        self.profile_button = Button(40, 560, 130, 42, "Profile")
        self.leader_button = Button(190, 560, 150, 42, "Leaderboard")
        self.history_button = Button(360, 560, 130, 42, "History")
        self.logout_button = Button(740, 560, 120, 42, "Logout")
        self.game_buttons = ArrayList()
        self.launch_message = ""
        self.refresh_games()

    def refresh_games(self):
        self.game_buttons = ArrayList()
        y = 145
        for game in self.app.api.get_games():
            self.game_buttons.append((Button(680, y + 8, 140, 38, "Launch"), game))
            y += 82

    def handle_event(self, event):
        if self.profile_button.is_clicked(event):
            self.app.change_screen("profile")
        if self.leader_button.is_clicked(event):
            self.app.change_screen("leaderboard")
        if self.history_button.is_clicked(event):
            self.app.change_screen("history")
        if self.logout_button.is_clicked(event):
            self.app.current_user = None
            self.app.change_screen("login")

        for button, game in self.game_buttons:
            if button.is_clicked(event):
                self.app.selected_game_id = game.game_id
                player_id = self.app.current_user.get_player_id()
                self.launch_message = self.app.launcher.launch_game(game.game_id, player_id)

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(BACKGROUND)
        draw_text(surface, "Game Catalog", self.app.title_font, BLACK, 40, 35)

        if self.app.current_user is not None:
            draw_text(surface, "Logged in as: " + self.app.current_user.get_display_name(), self.app.small_font, DARK_GRAY, 45, 90)

        y = 145
        games = self.app.api.get_games()
        for i in range(len(games)):
            game = games[i]
            card = pygame.Rect(40, y, 800, 62)
            pygame.draw.rect(surface, CARD, card, border_radius=8)
            pygame.draw.rect(surface, (205, 205, 205), card, 1, border_radius=8)
            draw_text(surface, game.name, self.app.font, BLACK, 60, y + 8)
            draw_text(surface, "Game ID: " + game.game_id, self.app.small_font, DARK_GRAY, 60, y + 36)
            draw_text(surface, "Players: " + game.players, self.app.small_font, DARK_GRAY, 245, y + 36)
            draw_text(surface, "Status: " + game.status, self.app.small_font, DARK_GRAY, 400, y + 36)
            self.game_buttons[i][0].draw(surface, self.app.small_font)
            y += 82

        if self.launch_message:
            draw_text(surface, self.launch_message, self.app.small_font, BLUE, 40, 520)

        self.profile_button.draw(surface, self.app.small_font)
        self.leader_button.draw(surface, self.app.small_font)
        self.history_button.draw(surface, self.app.small_font)
        self.logout_button.draw(surface, self.app.small_font)
