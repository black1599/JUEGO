import math
import pygame
from src.constants import (
    SCREEN_W, SCREEN_H, SIDEBAR_W, TOPBAR_H,
    SOURCES_DATA, CARD_W, CARD_H, CARD_PAD, CARD_COLS,
    DARK_BG, PANEL_BG, PANEL_LIGHT, BORDER, BORDER_HL,
    WHITE, BLACK, GRAY, GRAY_LIGHT, GRAY_DARK,
    GREEN, GREEN_DARK, GREEN_LIGHT, RED, RED_DARK,
    BLUE, BLUE_DARK, BLUE_LIGHT, ORANGE, YELLOW, YELLOW_DARK,
    PURPLE, TEAL,
)
from src.ui import (
    draw_rect_rounded, draw_text, draw_bar,
    Button, SourceCard, LOG_COLORS, font,
)
from src.city import CityRenderer
# ── Dimensiones calculadas ────────────────────────────────────────────────────
CITY_W  = SCREEN_W - SIDEBAR_W
CITY_H  = SCREEN_H - TOPBAR_H
SIDEBAR_X = CITY_W

class FloatingText:
    """Texto flotante animado para feedback visual. Es visual."""

    def __init__(self, text, pos, color):
        self.text  = text
        self.x, self.y = pos
        self.color = color
        self.life  = 1.5
        self.alpha = 255

    def update(self, dt):
        self.life -= dt
        self.y    -= 35 * dt
        self.alpha = max(0, int(255 * (self.life / 1.5)))


    def alive(self):
        return self.life > 0

    def draw(self, surf):
        f = font(14, bold=True)
        rendered = f.render(self.text, True, self.color)
        rendered.set_alpha(self.alpha)
        surf.blit(rendered, (int(self.x), int(self.y)))

