"""
Presenter — Energy Manager
Responsabilidad única: mediar entre Model (GameState) y View (GameView).
- Lee el estado del modelo y construye un snapshot para la vista.
- Traduce las acciones de UI en llamadas al modelo.
- No dibuja nada, no contiene lógica de negocio propia.
"""

from src.state import GameState
from src.view  import GameView
from src.constants import SOURCES_DATA, GREEN_LIGHT, RED, ORANGE, GRAY_LIGHT


SIDEBAR_X = 860   # = SCREEN_W - SIDEBAR_W
TOPBAR_H  = 90

