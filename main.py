"""
Energy Manager - Simulador de Gestión de Energía
Ejecutar: python main.py
Requiere: pip install pygame
"""

import pygame
import sys
from src.game import Game


def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((1200, 750))
    pygame.display.set_caption("Energy Manager - Simulador de Energía")
    clock = pygame.time.Clock()

    game = Game(screen)

    while True:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(event)

        game.update(dt)
        game.draw()
        pygame.display.flip()


if __name__ == "__main__":
    main()
