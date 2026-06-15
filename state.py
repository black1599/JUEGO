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

        # ── Propiedades derivadas ─────────────────────────────────────────────────
        @property
        def production(self):
            total = 0
            for s in SOURCES_DATA:
                total += s["mw"] * self.owned[s["id"]]
            return total

        @property
        def op_cost(self):
            total = 0
            for s in SOURCES_DATA:
                total += s["op_cost"] * self.owned[s["id"]]
            return total

        @property
        def balance(self):
            return self.production - self.demand

        @property
        def xp_needed(self):
            if self.level - 1 < len(LEVEL_XP):
                return LEVEL_XP[self.level] if self.level < len(LEVEL_XP) else 9999
            return 9999

        @property
        def xp_progress(self):
            needed = self.xp_needed
            if needed == 0:
                return 1.0
            return min(1.0, self.xp / needed)