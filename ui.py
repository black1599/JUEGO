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
