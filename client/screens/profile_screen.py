from ui_helpers import BACKGROUND, BLACK, DARK_GRAY, Button, draw_text


class ProfileScreen:
    def __init__(self, app):
        self.app = app
        self.back_button = Button(40, 560, 120, 42, "Back")

    def handle_event(self, event):
        if self.back_button.is_clicked(event):
            self.app.change_screen("catalog")

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(BACKGROUND)
        draw_text(surface, "Player Profile", self.app.title_font, BLACK, 40, 35)

        profile = self.app.api.get_profile(self.app.current_user["player_id"])
        lines = [
            "Display Name: " + profile["display_name"],
            "Username: " + profile["username"],
            "Player ID: " + profile["player_id"],
            "Games Played: " + str(profile["games_played"]),
            "Wins: " + str(profile["wins"]),
            "Losses: " + str(profile["losses"]),
            "Win Rate: " + profile["win_rate"],
            "Total Score: " + str(profile["total_score"]),
            "Favorite Game: " + profile["favorite_game"],
        ]

        y = 130
        for line in lines:
            draw_text(surface, line, self.app.font, BLACK, 80, y)
            y += 43

        draw_text(surface, "Data comes from AccountService and MatchHistoryService through api_client.py.", self.app.small_font, DARK_GRAY, 80, 515)
        self.back_button.draw(surface, self.app.small_font)
