import pygame
import random
import math
from src.constants import DARK_BG, PANEL_BG, BLUE, YELLOW, GREEN


class CityRenderer:
    """Dibuja una ciudad de fondo con edificios animados según el nivel."""

    def __init__(self, width, height):
        self.w = width
        self.h = height
        self._buildings = []
        self._stars      = []
        self._time       = 0.0
        self._last_level = 0
        self._init_stars()
        self._generate_buildings(1)
