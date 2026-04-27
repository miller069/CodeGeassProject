"""Shared Pygame UI helpers for Chuqi's client screens."""

import pygame

WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
GRAY = (175, 175, 175)
DARK_GRAY = (70, 70, 70)
BLUE = (55, 120, 220)
LIGHT_BLUE = (110, 170, 245)
RED = (210, 70, 70)
GREEN = (70, 160, 90)
BACKGROUND = (238, 243, 250)
CARD = (255, 255, 255)


def draw_text(surface, text, font, color, x, y):
    image = font.render(str(text), True, color)
    surface.blit(image, (x, y))


def draw_centered_text(surface, text, font, color, rect):
    image = font.render(str(text), True, color)
    text_rect = image.get_rect(center=rect.center)
    surface.blit(image, text_rect)


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, surface, font):
        mouse_pos = pygame.mouse.get_pos()
        color = LIGHT_BLUE if self.rect.collidepoint(mouse_pos) else BLUE
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=8)
        draw_centered_text(surface, self.text, font, WHITE, self.rect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


class TextInput:
    def __init__(self, x, y, width, height, placeholder="", is_password=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.placeholder = placeholder
        self.is_password = is_password
        self.text = ""
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return
            elif event.key == pygame.K_TAB:
                return
            else:
                if len(self.text) < 30:
                    self.text += event.unicode

    def draw(self, surface, font):
        border = BLUE if self.active else GRAY
        pygame.draw.rect(surface, WHITE, self.rect, border_radius=6)
        pygame.draw.rect(surface, border, self.rect, 2, border_radius=6)

        if self.text == "":
            shown = self.placeholder
            color = GRAY
        else:
            shown = "*" * len(self.text) if self.is_password else self.text
            color = BLACK

        draw_text(surface, shown, font, color, self.rect.x + 10, self.rect.y + 9)
