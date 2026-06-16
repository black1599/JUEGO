"""
Presenter — Energy Manager
"""
from src.state import GameState
from src.view  import GameView
from src.constants import SOURCES_DATA, GREEN_LIGHT, RED, ORANGE, GRAY_LIGHT

SIDEBAR_X = 860   # = SCREEN_W - SIDEBAR_W
TOPBAR_H  = 90

class GamePresenter:
    """
    Patrón MVP:
      Model     → GameState  (lógica y datos puros)
      View      → GameView   (renderizado pygame)
      Presenter → este archivo (mediador sin estado propio de juego)
    """

    def __init__(self, view: GameView):
        self._model = GameState()
        self._view  = view
        self._screen_mode = "game"   # "game" | "gameover"

        # Conectar callbacks de la vista a métodos del presenter
        self._view.on_next_turn   = self._on_next_turn
        self._view.on_sell_excess = self._on_sell_excess
        self._view.on_reset       = self._on_reset
        self._view.on_buy_source  = self._on_buy_source


