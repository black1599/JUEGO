"""
game.py — Energy Manager
Clase orquestadora ligera.
Crea la View y el Presenter y delega todo en ellos.
No contiene lógica de negocio ni código de renderizado propio.
"""

import pygame
from src.view      import GameView
from src.presenter import GamePresenter

class Game:
    """
    Punto de integración: une View y Presenter y expone
    la interfaz que main.py necesita (handle_event / update / draw).
    """

    def __init__(self, screen: pygame.Surface):
        self._view      = GameView(screen)
        self._presenter = GamePresenter(self._view)

    def handle_event(self, event: pygame.event.Event):
        self._presenter.handle_event(event)

    def update(self, dt: float):
        self._presenter.update(dt)

    def draw(self):
        self._presenter.render()

