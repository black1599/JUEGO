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
