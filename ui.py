import pygame
from src.constants import (
    WHITE, BLACK, BORDER, BORDER_HL, PANEL_BG, PANEL_LIGHT,
    GRAY, GRAY_LIGHT, GRAY_DARK, GREEN, GREEN_DARK, RED, RED_DARK,
    BLUE, BLUE_DARK, ORANGE, YELLOW, YELLOW_DARK, TEAL,
)


def load_font(size, bold=False):
    """Carga la fuente del sistema, con fallback seguro."""
    try:
        name = pygame.font.match_font("segoeui,dejavusans,ubuntu,arial,freesans")
        if name:
            return pygame.font.Font(name, size)
    except Exception:
        pass
    return pygame.font.SysFont("arial", size, bold=bold)


# ── Fuentes globales (se inicializan en la primera llamada) ───────────────────
_fonts = {}


def font(size, bold=False):
    key = (size, bold)
    if key not in _fonts:
        _fonts[key] = load_font(size, bold)
    return _fonts[key]

# ── Colores de log ────────────────────────────────────────────────────────────
LOG_COLORS = {
    "good":  (88, 214, 141),
    "bad":   (231, 76, 60),
    "warn":  (230, 126, 34),
    "info":  (150, 170, 210),
    "level": (241, 196, 15),
}

# ── Funciones de dibujo básicas ───────────────────────────────────────────────

def draw_rect_rounded(surf, color, rect, radius=8, border=0, border_color=None):
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    if border > 0 and border_color:
        pygame.draw.rect(surf, border_color, rect, width=border, border_radius=radius)


def draw_text(surf, text, pos, color=WHITE, size=14, bold=False, anchor="topleft"):
    f = font(size, bold)
    rendered = f.render(str(text), True, color)
    r = rendered.get_rect()
    setattr(r, anchor, pos)
    surf.blit(rendered, r)
    return r


def draw_bar(surf, rect, value, max_value, fg_color, bg_color=GRAY_DARK, radius=4, border_color=None):
    """Dibuja una barra de progreso."""
    pygame.draw.rect(surf, bg_color, rect, border_radius=radius)
    if max_value > 0:
        fill_w = max(0, int(rect.width * min(1.0, value / max_value)))
        if fill_w > 0:
            fill_rect = pygame.Rect(rect.x, rect.y, fill_w, rect.height)
            pygame.draw.rect(surf, fg_color, fill_rect, border_radius=radius)
    if border_color:
        pygame.draw.rect(surf, border_color, rect, width=1, border_radius=radius)

class Button:
    """Botón simple con hover y click."""

    def __init__(self, rect, label, color=BLUE, hover_color=BLUE_DARK,
                 text_color=WHITE, font_size=13, radius=6, icon=""):
        self.rect       = pygame.Rect(rect)
        self.label      = label
        self.color      = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font_size  = font_size
        self.radius     = radius
        self.icon       = icon
        self.hovered    = False
        self.enabled    = True
        self._anim      = 0.0   # para efecto de click

    def handle_event(self, event):
        if not self.enabled:
            return False
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self._anim = 0.15
                return True
        return False

    def update(self, dt):
        if self._anim > 0:
            self._anim = max(0, self._anim - dt)

    def draw(self, surf):
        col = self.hover_color if self.hovered else self.color
        if not self.enabled:
            col = GRAY_DARK
        offset = 1 if self._anim > 0 else 0
        r = self.rect.move(0, offset)
        draw_rect_rounded(surf, col, r, self.radius, border=1, border_color=BORDER_HL)
        txt = f"{self.icon} {self.label}" if self.icon else self.label
        tc = GRAY if not self.enabled else self.text_color
        draw_text(surf, txt, r.center, tc, self.font_size, anchor="center")

class SourceCard:
    """Tarjeta de fuente de energía."""

    def __init__(self, rect, source_data):
        self.rect   = pygame.Rect(rect)
        self.src    = source_data
        self.hovered = False
        self._anim  = 0.0

    def handle_event(self, event, locked):
        if locked:
            return False
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and not locked:
                self._anim = 0.15
                return True
        return False

    def update(self, dt):
        if self._anim > 0:
            self._anim = max(0, self._anim - dt)

    def draw(self, surf, count, locked, can_afford):
        bg = PANEL_LIGHT if self.hovered and not locked else PANEL_BG
        alpha_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

        if locked:
            pygame.draw.rect(alpha_surf, (*PANEL_BG, 140), alpha_surf.get_rect(), border_radius=8)
            surf.blit(alpha_surf, self.rect.topleft)
            pygame.draw.rect(surf, BORDER, self.rect, width=1, border_radius=8)
            draw_text(surf, "?", self.rect.center, GRAY, 28, bold=True, anchor="center")
            unlock_lv = self.src["unlock_level"]
            draw_text(surf, f"Nv.{unlock_lv}", (self.rect.centerx, self.rect.bottom - 14),
                      GRAY, 11, anchor="center")
            return

        border_col = self.src["color"] if self.hovered else BORDER
        draw_rect_rounded(surf, bg, self.rect, radius=8, border=1, border_color=border_col)

        # Icono / letra grande con fondo coloreado
        icon_r = pygame.Rect(self.rect.x + 6, self.rect.y + 8, 32, 32)
        draw_rect_rounded(surf, self.src["color"], icon_r, radius=6)
        draw_text(surf, self.src["emoji"], icon_r.center, BLACK, 15, bold=True, anchor="center")

        # Nombre
        draw_text(surf, self.src["name"], (self.rect.x + 45, self.rect.y + 10),
                  WHITE, 12, bold=True)

        # MW
        draw_text(surf, f"{self.src['mw']} MW", (self.rect.x + 45, self.rect.y + 26),
                  GRAY_LIGHT, 11)

        # Coste
        cost_col = GREEN if can_afford else RED
        draw_text(surf, f"€{self.src['cost']}", (self.rect.x + 6, self.rect.y + 50),
                  cost_col, 12, bold=True)

        # Op cost
        draw_text(surf, f"Op:€{self.src['op_cost']}/t", (self.rect.x + 6, self.rect.y + 66),
                  GRAY, 10)

        # Contaminante
        if self.src["pollutes"]:
            draw_text(surf, "♻ contam.", (self.rect.x + 6, self.rect.y + 80),
                      (200, 140, 60), 9)

        # Contador
        if count > 0:
            badge_r = pygame.Rect(self.rect.right - 26, self.rect.y + 6, 22, 18)
            draw_rect_rounded(surf, GREEN_DARK, badge_r, radius=4)
            draw_text(surf, str(count), badge_r.center, WHITE, 11, bold=True, anchor="center")
