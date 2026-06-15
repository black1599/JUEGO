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

class GameView:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.city   = CityRenderer(CITY_W, CITY_H)
        self._floats: list[FloatingText] = []
        self._time   = 0.0
        self._pulse  = 0.0

        # ── Widgets ────────────────────────────────────────────────────────────
        btn_y = SCREEN_H - 60
        self.btn_turn = Button(
            (SIDEBAR_X + 12, btn_y, SIDEBAR_W - 24, 36),
            "Siguiente turno", BLUE, BLUE_DARK, font_size=14,
        )
        self.btn_sell = Button(
            (SIDEBAR_X + 12, btn_y - 46, (SIDEBAR_W - 30) // 2, 32),
            "Vender exceso", GREEN_DARK, (20, 90, 50), font_size=12,
        )
        self.btn_reset = Button(
            (SIDEBAR_X + 12 + (SIDEBAR_W - 30) // 2 + 6, btn_y - 46,
             (SIDEBAR_W - 30) // 2, 32),
            "Reiniciar", (80, 40, 40), (120, 40, 40), font_size=12,
        )
        self.all_buttons = [self.btn_turn, self.btn_sell, self.btn_reset]

        self.cards: list[tuple[SourceCard, str]] = []
        self._build_cards()

        # ── Callbacks asignados por el Presenter ───────────────────────────────
        self.on_next_turn   = None   # ()
        self.on_sell_excess = None   # ()
        self.on_reset       = None   # ()
        self.on_buy_source  = None   # (source_id: str)

    # ── Construcción interna de widgets ───────────────────────────────────────

    def _build_cards(self):
        cols = CARD_COLS
        start_y = TOPBAR_H + 10
        for i, src in enumerate(SOURCES_DATA):
            col = i % cols
            row = i // cols
            x = SIDEBAR_X + 12 + col * (CARD_W + CARD_PAD)
            y = start_y + row * (CARD_H + CARD_PAD)
            card = SourceCard((x, y, CARD_W, CARD_H), src)
            self.cards.append((card, src["id"]))

    # ── API pública ───────────────────────────────────────────────────────────

    def add_float(self, text: str, pos: tuple, color: tuple):
        """Añade un texto flotante animado."""
        import random
        jitter = (random.randint(-20, 20), random.randint(-5, 5))
        self._floats.append(FloatingText(text, (pos[0] + jitter[0], pos[1] + jitter[1]), color))


    def handle_event(self, event: pygame.event.Event, screen_mode: str, snapshot: dict):
        """
        Procesa un evento pygame.

        """
        if screen_mode == "gameover":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if self.on_reset:
                    self.on_reset()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.on_reset:
                    self.on_reset()
            return

        if self.btn_turn.handle_event(event):
            if self.on_next_turn:
                self.on_next_turn()

        if self.btn_sell.handle_event(event):
            if self.on_sell_excess:
                self.on_sell_excess()

        if self.btn_reset.handle_event(event):
            if self.on_reset:
                self.on_reset()

        level = snapshot.get("level", 1)
        for card, src_id in self.cards:
            src_data = next(s for s in SOURCES_DATA if s["id"] == src_id)
            locked = src_data["unlock_level"] > level
            if card.handle_event(event, locked):
                if self.on_buy_source:
                    self.on_buy_source(src_id)

