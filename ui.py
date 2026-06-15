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
