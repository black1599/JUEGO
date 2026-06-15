import random
from src.constants import (
    SOURCES_DATA, LEVEL_XP, INCOME_PER_MW, SELL_RATE,
    DEFICIT_PENALTY, POLLUTION_FINE, POLLUTION_LIMIT,
    DEMAND_GROWTH_TURNS,
)


class GameState:
    """Contiene toda la lógica y datos del juego sin depender de pygame."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.money        = 500
        self.turn         = 1
        self.level        = 1
        self.xp           = 0
        self.demand       = 30
        self.pollution    = 0
        self.owned        = {s["id"]: 0 for s in SOURCES_DATA}
        self.log_entries  = []
        self.game_over    = False
        self.total_turns  = 0
        self._log("¡Bienvenido! Construye tu red eléctrica.", "info")