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

    def draw(self, surf, production, demand):
        # Cielo degradado manual
        sky_top    = (10, 15, 35)
        sky_bottom = (22, 28, 55)
        for y in range(self.h):
            t = y / self.h
            r = int(sky_top[0] + t * (sky_bottom[0] - sky_top[0]))
            g = int(sky_top[1] + t * (sky_bottom[1] - sky_top[1]))
            b = int(sky_top[2] + t * (sky_bottom[2] - sky_top[2]))
            pygame.draw.line(surf, (r, g, b), (0, y), (self.w, y))

        # Estrellas
        for sx, sy in self._stars:
            br = 120 + int(50 * math.sin(self._time * 1.2 + sx * 0.1))
            pygame.draw.circle(surf, (br, br, br + 30), (sx, sy), 1)

        # Luna
        moon_x = self.w - 80
        moon_y = 50
        pygame.draw.circle(surf, (230, 230, 200), (moon_x, moon_y), 18)
        pygame.draw.circle(surf, (10, 15, 35), (moon_x - 6, moon_y - 4), 12)

        # Edificios
        for b in self._buildings:
            bx = b["x"]
            by = self.h - b["h"]
            pygame.draw.rect(surf, b["col"], (bx, by, b["w"], b["h"]))
            # Borde sutil
            pygame.draw.rect(surf, (b["col"][0]+15, b["col"][1]+15, b["col"][2]+15),
                             (bx, by, b["w"], b["h"]), width=1)
            # Ventanas
            for wx, wy, lit in b["windows"]:
                if 0 <= wx < self.w and 0 <= wy < self.h:
                    col = (240, 220, 100) if lit else (30, 35, 55)
                    pygame.draw.rect(surf, col, (wx, wy, 8, 8))

            # Antena en edificios altos
            if b["h"] > 80:
                ax = bx + b["w"] // 2
                pygame.draw.line(surf, (80, 85, 100), (ax, by), (ax, by - 12), 1)
                blink_on = int(self._time * 2) % 2 == 0
                pygame.draw.circle(surf, (255, 60, 60) if blink_on else (100, 30, 30),
                                   (ax, by - 13), 2)

        # Suelo
        pygame.draw.rect(surf, (30, 35, 55), (0, self.h - 4, self.w, 4))

        # Indicador de balance energético como aurora
        if production >= demand:
            aurora_alpha = min(180, int((production - demand) * 3))
            aurora_surf = pygame.Surface((self.w, 40), pygame.SRCALPHA)
            for i in range(40):
                t = i / 40
                a = int(aurora_alpha * math.sin(t * math.pi))
                wave = math.sin(self._time * 0.8 + i * 0.3) * 8
                color = (50, 200, 120, a)
                pygame.draw.line(aurora_surf, color,
                                 (0, 20 + int(wave)),
                                 (self.w, 20 + int(wave * 0.5)), 2)
            surf.blit(aurora_surf, (0, self.h // 3 - 20))
