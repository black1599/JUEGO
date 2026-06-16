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


    def update(self, dt: float, level: int):
        """Actualiza animaciones internas de la vista."""
        self._time  += dt
        self._pulse  = math.sin(self._time * 2.0)
        self.city.update(dt, level)
        for btn in self.all_buttons:
            btn.update(dt)
        for card, _ in self.cards:
            card.update(dt)
        self._floats = [f for f in self._floats if f.alive]
        for f in self._floats:
            f.update(dt)

    def render(self, snapshot: dict):
        """Renderiza el frame completo a partir del snapshot."""
        mode = snapshot.get("screen_mode", "game")
        if mode == "gameover":
            self._draw_gameover(snapshot)
        else:
            self._draw_game(snapshot)
        for f in self._floats:
            f.draw(self.screen)


    # ── Renderizado del juego ─────────────────────────────────────────────────

    def _draw_game(self, s: dict):
        city_surf = pygame.Surface((CITY_W, CITY_H))
        self.city.draw(city_surf, s["production"], s["demand"])
        self.screen.blit(city_surf, (0, TOPBAR_H))

        self._draw_topbar(s)
        self._draw_sidebar(s)
        self._draw_hud_overlay(s)

    def _draw_topbar(self, s: dict):
        pygame.draw.rect(self.screen, PANEL_BG, (0, 0, SCREEN_W, TOPBAR_H))
        pygame.draw.line(self.screen, BORDER, (0, TOPBAR_H), (SCREEN_W, TOPBAR_H), 1)

        draw_text(self.screen, "⚡ ENERGY MANAGER", (16, 12), YELLOW, 18, bold=True)
        draw_text(self.screen, f"Turno {s['turn']}", (16, 40), GRAY_LIGHT, 12)

        stats = [
            ("💰 Dinero",     f"€{s['money']:,}",
             GREEN if s["money"] >= 0 else RED),
            ("⚡ Producción", f"{s['production']} MW",
             GREEN if s["production"] >= s["demand"] else RED),
            ("🏙 Demanda",    f"{s['demand']} MW", BLUE_LIGHT),
            ("☁ Contam.",    f"{s['pollution']}",
             GREEN if s["pollution"] <= 20 else ORANGE),
        ]
        sx = 200
        for label, val, col in stats:
            draw_text(self.screen, label, (sx, 10), GRAY_LIGHT, 11)
            draw_text(self.screen, val,   (sx, 28), col, 16, bold=True)
            sx += 160

        lv_x = SCREEN_W - 220
        draw_text(self.screen, f"Nivel {s['level']}", (lv_x, 10), YELLOW, 13, bold=True)
        xp_rect = pygame.Rect(lv_x, 30, 190, 10)
        draw_bar(self.screen, xp_rect, s["xp"], s["xp_needed"], YELLOW_DARK, border_color=BORDER)
        draw_text(self.screen, f"{s['xp']}/{s['xp_needed']} XP", (lv_x, 44), GRAY, 10)

    def _draw_sidebar(self, s: dict):
        pygame.draw.rect(self.screen, PANEL_BG, (SIDEBAR_X, 0, SIDEBAR_W, SCREEN_H))
        pygame.draw.line(self.screen, BORDER, (SIDEBAR_X, 0), (SIDEBAR_X, SCREEN_H), 1)
        draw_text(self.screen, "FUENTES DE ENERGÍA",
                  (SIDEBAR_X + 12, TOPBAR_H + 8), GRAY_LIGHT, 11)

        owned     = s["owned"]
        level     = s["level"]
        money     = s["money"]
        for card, src_id in self.cards:
            src_data   = next(src for src in SOURCES_DATA if src["id"] == src_id)
            locked     = src_data["unlock_level"] > level
            count      = owned.get(src_id, 0)
            can_afford = money >= src_data["cost"]
            card.draw(self.screen, count, locked, can_afford)

        for btn in self.all_buttons:
            btn.draw(self.screen)

    def _draw_hud_overlay(self, s: dict):
        hud_x, hud_y = 12, TOPBAR_H + 12
        panel_w, panel_h = 240, 85
        panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (*PANEL_BG, 200), panel_surf.get_rect(), border_radius=10)
        self.screen.blit(panel_surf, (hud_x, hud_y))
        pygame.draw.rect(self.screen, BORDER,
                         (hud_x, hud_y, panel_w, panel_h), width=1, border_radius=10)

        draw_text(self.screen, "RED ELÉCTRICA", (hud_x + 10, hud_y + 8), GRAY_LIGHT, 10)

        bar_max = max(s["demand"] * 1.5, s["production"] + 20, 50)
        draw_text(self.screen, "Prod.", (hud_x + 10, hud_y + 24), GRAY_LIGHT, 10)
        draw_bar(self.screen, pygame.Rect(hud_x + 55, hud_y + 24, 150, 10),
                 s["production"], bar_max, GREEN, border_color=BORDER)
        draw_text(self.screen, f"{s['production']}", (hud_x + 210, hud_y + 24), GREEN, 10)

        draw_text(self.screen, "Dem.", (hud_x + 10, hud_y + 40), GRAY_LIGHT, 10)
        draw_bar(self.screen, pygame.Rect(hud_x + 55, hud_y + 40, 150, 10),
                 s["demand"], bar_max, RED, border_color=BORDER)
        draw_text(self.screen, f"{s['demand']}", (hud_x + 210, hud_y + 40), RED, 10)

        bal     = s["balance"]
        bal_col = GREEN if bal >= 0 else RED
        draw_text(self.screen, f"Balance: {'+' if bal >= 0 else ''}{bal} MW",
                  (hud_x + 10, hud_y + 60), bal_col, 12, bold=True)

        # Log
        log_x = 12
        log_y = TOPBAR_H + CITY_H - 170
        log_w, log_h = CITY_W - 24, 155
        log_surf = pygame.Surface((log_w, log_h), pygame.SRCALPHA)
        pygame.draw.rect(log_surf, (*PANEL_BG, 200), log_surf.get_rect(), border_radius=10)
        self.screen.blit(log_surf, (log_x, log_y))
        pygame.draw.rect(self.screen, BORDER,
                         (log_x, log_y, log_w, log_h), width=1, border_radius=10)
        draw_text(self.screen, "REGISTRO", (log_x + 10, log_y + 8), GRAY_LIGHT, 10)
        for i, (msg, col_key) in enumerate(s["log_entries"][:8]):
            col = LOG_COLORS.get(col_key, GRAY_LIGHT)
            draw_text(self.screen, msg, (log_x + 10, log_y + 24 + i * 16), col, 11)

    def _draw_gameover(self, s: dict):
        self.screen.fill(DARK_BG)
        cx, cy = SCREEN_W // 2, SCREEN_H // 2
        overlay = pygame.Surface((600, 320), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (*PANEL_BG, 230), overlay.get_rect(), border_radius=18)
        self.screen.blit(overlay, (cx - 300, cy - 160))
        pygame.draw.rect(self.screen, RED, (cx - 300, cy - 160, 600, 320), width=2, border_radius=18)

        draw_text(self.screen, "QUIEBRA", (cx, cy - 110), RED, 42, bold=True, anchor="center")
        draw_text(self.screen, "Tu ciudad se quedó sin luz...", (cx, cy - 55),
                  GRAY_LIGHT, 16, anchor="center")
        draw_text(self.screen, f"Turnos jugados: {s['total_turns']}",
                  (cx, cy - 15), WHITE, 14, anchor="center")
        draw_text(self.screen, f"Nivel alcanzado: {s['level']}",
                  (cx, cy + 15), WHITE, 14, anchor="center")
        pulse = int(200 + 55 * math.sin(self._time * 3))
        draw_text(self.screen, "Clic o [R] para reiniciar",
                  (cx, cy + 80), (pulse, pulse, pulse), 16, anchor="center")






