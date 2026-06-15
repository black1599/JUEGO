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

    def _init_stars(self):
        random.seed(42)
        self._stars = [(random.randint(0, self.w), random.randint(0, self.h // 3))
                       for _ in range(60)]
        random.seed()

    def _generate_buildings(self, level):
        """Genera los edificios con altura y densidad según nivel."""
        self._buildings = []
        count = 18 + level * 4
        x = 0
        for _ in range(count):
            w = random.randint(28, 55)
            base_h = random.randint(40, 80 + level * 18)
            floors = max(2, base_h // 14)
            color_idx = random.randint(0, 2)
            colors = [
                (45, 55, 80), (40, 50, 70), (55, 65, 90),
                (35, 60, 75), (50, 45, 72),
            ]
            col = colors[color_idx % len(colors)]
            windows = []
            for fy in range(floors):
                for fx in range(max(1, w // 14)):
                    wx = x + 4 + fx * 12
                    wy = self.h - base_h + fy * 14 + 4
                    lit = random.random() < 0.6
                    windows.append((wx, wy, lit))
            self._buildings.append({
                "x": x, "w": w, "h": base_h, "col": col,
                "windows": windows, "floors": floors,
            })
            x += w + random.randint(2, 6)
        self._last_level = level

    def update(self, dt, level):
        self._time += dt
        if level != self._last_level:
            self._generate_buildings(level)
        # Parpadeo de ventanas lento
        if random.random() < 0.02:
            if self._buildings:
                b = random.choice(self._buildings)
                if b["windows"]:
                    idx = random.randint(0, len(b["windows"]) - 1)
                    wx, wy, lit = b["windows"][idx]
                    b["windows"][idx] = (wx, wy, not lit)
