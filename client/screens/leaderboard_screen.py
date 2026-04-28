import os
import sys
import pygame

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ui_helpers import BACKGROUND, BLACK, DARK_GRAY, CARD, Button, draw_text
from data_structures.array_list import ArrayList


class LeaderboardScreen:
    def __init__(self, app):
        self.app = app
        self.back_button = Button(40, 560, 120, 42, "Back")

        self.game_buttons = ArrayList()
        x = 40
        for game in self.app.api.get_games():
            self.game_buttons.append((Button(x, 100, 135, 36, game.game_id), game.game_id))
            x += 150

    def handle_event(self, event):
        if self.back_button.is_clicked(event):
            self.app.change_screen("catalog")

        for button, game_id in self.game_buttons:
            if button.is_clicked(event):
                self.app.selected_game_id = game_id

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(BACKGROUND)
        draw_text(surface, "Leaderboard", self.app.title_font, BLACK, 40, 35)
        draw_text(surface, "Selected game: " + self.app.selected_game_id, self.app.small_font, DARK_GRAY, 45, 78)

        for button, game_id in self.game_buttons:
            button.draw(surface, self.app.small_font)

        rows = self.app.api.get_leaderboard(self.app.selected_game_id, 10)

        header = pygame.Rect(70, 165, 740, 40)
        pygame.draw.rect(surface, (220, 230, 240), header)
        draw_text(surface, "Rank", self.app.font, BLACK, 95, 173)
        draw_text(surface, "Player", self.app.font, BLACK, 250, 173)
        draw_text(surface, "Score", self.app.font, BLACK, 590, 173)

        y = 210
        if len(rows) == 0:
            draw_text(surface, "No leaderboard data for this game yet.", self.app.font, DARK_GRAY, 90, y + 20)
        else:
            for row in rows:
                pygame.draw.rect(surface, CARD, pygame.Rect(70, y, 740, 38))
                pygame.draw.rect(surface, (210, 210, 210), pygame.Rect(70, y, 740, 38), 1)
                draw_text(surface, row.rank, self.app.font, BLACK, 105, y + 7)
                draw_text(surface, row.username, self.app.font, BLACK, 250, y + 7)
                draw_text(surface, row.score, self.app.font, BLACK, 595, y + 7)
                y += 42

        draw_text(surface, "Uses teammate LeaderboardService with MaxHeap and AVLTree.", self.app.small_font, DARK_GRAY, 80, 525)
        self.back_button.draw(surface, self.app.small_font)
