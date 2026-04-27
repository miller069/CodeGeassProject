import pygame
from ui_helpers import BACKGROUND, BLACK, DARK_GRAY, RED, GREEN, Button, TextInput, draw_text


class LoginScreen:
    def __init__(self, app):
        self.app = app
        self.username_input = TextInput(300, 230, 310, 44, "username, e.g. chuqi")
        self.password_input = TextInput(300, 290, 310, 44, "password", is_password=True)
        self.login_button = Button(300, 365, 145, 45, "Login")
        self.create_button = Button(465, 365, 145, 45, "Create")
        self.message = "Use chuqi / any password for the local demo."
        self.message_color = DARK_GRAY

    def handle_event(self, event):
        self.username_input.handle_event(event)
        self.password_input.handle_event(event)

        if self.login_button.is_clicked(event):
            result = self.app.api.login(self.username_input.text, self.password_input.text)
            self.message = result["message"]
            self.message_color = GREEN if result["success"] else RED
            if result["success"]:
                self.app.current_user = result["user"]
                self.app.change_screen("catalog")

        if self.create_button.is_clicked(event):
            result = self.app.api.create_account(self.username_input.text, self.password_input.text)
            self.message = result["message"]
            self.message_color = GREEN if result["success"] else RED
            if result["success"]:
                self.app.current_user = result["user"]
                self.app.change_screen("catalog")

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(BACKGROUND)
        draw_text(surface, "The Arcade", self.app.title_font, BLACK, 330, 90)
        draw_text(surface, "Pygame client connected to local Python service classes", self.app.small_font, DARK_GRAY, 255, 145)

        draw_text(surface, "Username", self.app.small_font, BLACK, 300, 205)
        self.username_input.draw(surface, self.app.font)
        draw_text(surface, "Password", self.app.small_font, BLACK, 300, 265)
        self.password_input.draw(surface, self.app.font)

        self.login_button.draw(surface, self.app.font)
        self.create_button.draw(surface, self.app.font)
        draw_text(surface, self.message, self.app.small_font, self.message_color, 300, 430)
