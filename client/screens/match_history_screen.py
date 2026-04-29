import pygame
from ui_helpers import BACKGROUND, BLACK, DARK_GRAY, CARD, Button, draw_text


class MatchHistoryScreen:
    def __init__(self, app):
        self.app = app
        self.back_button = Button(40, 560, 120, 42, "Back")

    def handle_event(self, event):
        if self.back_button.is_clicked(event):
            self.app.change_screen("catalog")

    def update(self):
        pass

    def draw(self, surface):
        if self.app.current_user is None:
            self.app.change_screen("login")
            return
        surface.fill(BACKGROUND)
        draw_text(surface, "Match History", self.app.title_font, BLACK, 40, 35)

        player_id = self.app.current_user.get_player_id()
        rows = self.app.api.get_match_history(player_id)
        draw_text(surface, "Player ID: " + player_id, self.app.small_font, DARK_GRAY, 45, 90)

        pygame.draw.rect(surface, (220, 230, 240), pygame.Rect(45, 140, 810, 40))
        draw_text(surface, "Game", self.app.font, BLACK, 65, 148)
        draw_text(surface, "Score", self.app.font, BLACK, 335, 148)
        draw_text(surface, "Date", self.app.font, BLACK, 480, 148)
        draw_text(surface, "Outcome", self.app.font, BLACK, 680, 148)

        y = 185
        if len(rows) == 0:
            draw_text(surface, "No match history yet.", self.app.font, DARK_GRAY, 70, y + 20)
        else:
            for row in rows:
                pygame.draw.rect(surface, CARD, pygame.Rect(45, y, 810, 38))
                pygame.draw.rect(surface, (210, 210, 210), pygame.Rect(45, y, 810, 38), 1)
                draw_text(surface, row.game, self.app.font, BLACK, 65, y + 7)
                draw_text(surface, row.score, self.app.font, BLACK, 345, y + 7)
                draw_text(surface, row.date, self.app.font, BLACK, 480, y + 7)
                draw_text(surface, row.outcome, self.app.font, BLACK, 690, y + 7)
                y += 42

        draw_text(surface, "Uses teammate MatchHistoryService and Mergesort through api_client.py.", self.app.small_font, DARK_GRAY, 80, 525)
        self.back_button.draw(surface, self.app.small_font)