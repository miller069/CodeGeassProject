import os
import sys
import time

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ui_helpers import BACKGROUND, BLACK, DARK_GRAY, Button, draw_text
from data_structures.array_list import ArrayList


class ProfileScreen:
    def __init__(self, app):
        self.app = app
        self.back_button = Button(40, 560, 120, 42, "Back")
        self.profile = None
        self.loaded_player_id = None

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
        draw_text(surface, "Player Profile", self.app.title_font, BLACK, 40, 35)
        player_id = self.app.current_user.get_player_id()

        if self.profile is None or self.loaded_player_id != player_id:
            start = time.perf_counter()

            self.app.api.reload_sessions()
            self.profile = self.app.api.get_profile(player_id)

            end = time.perf_counter()
            print(f"[ProfileScreen] reload + get_profile took {end - start:.4f} seconds")

            self.loaded_player_id = player_id

        profile = self.profile

        lines = ArrayList()
        lines.append("Display Name: " + profile.display_name)
        lines.append("Username: " + profile.username)
        lines.append("Player ID: " + profile.player_id)
        lines.append("Games Played: " + str(profile.games_played))
        lines.append("Wins: " + str(profile.wins))
        lines.append("Losses: " + str(profile.losses))
        lines.append("Win Rate: " + profile.win_rate)
        lines.append("Total Score: " + str(profile.total_score))
        lines.append("Favorite Game: " + profile.favorite_game)

        y = 130
        for line in lines:
            draw_text(surface, line, self.app.font, BLACK, 80, y)
            y += 43

        draw_text(surface, "Data comes from AccountService and MatchHistoryService through api_client.py.", self.app.small_font, DARK_GRAY, 80, 515)
        self.back_button.draw(surface, self.app.small_font)