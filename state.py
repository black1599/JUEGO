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

        # ── Acciones del jugador ──────────────────────────────────────────────────
        def buy(self, source_id):
            """Intenta comprar una unidad de la fuente indicada. Retorna mensaje."""
            src = self._get_source(source_id)
            if src["unlock_level"] > self.level:
                return False, f"Necesitas nivel {src['unlock_level']}."
            if self.money < src["cost"]:
                return False, "Fondos insuficientes."
            self.money -= src["cost"]
            self.owned[source_id] += 1
            if src["pollutes"]:
                self.pollution += src["pollution_amt"]
            self._log(f"+ {src['name']} ({src['mw']} MW)", "good")
            return True, ""

        def sell_excess(self):
            """Vende el exceso de producción."""
            excess = self.balance
            if excess <= 0:
                self._log("Sin exceso para vender.", "warn")
                return 0
            earned = round(excess * SELL_RATE)
            self.money += earned
            self._log(f"Vendido {excess} MW → +€{earned}", "good")
            return earned

        def next_turn(self):
            """Avanza un turno. Retorna lista de eventos del turno."""
            if self.game_over:
                return

            events = []
            self.turn += 1
            self.total_turns += 1

            # Costes operativos
            op = self.op_cost
            self.money -= op
            if op > 0:
                events.append((f"Costes operativos: -€{op}", "warn"))

            # Ingresos / penalizaciones por balance
            if self.production >= self.demand:
                income = round(self.demand * INCOME_PER_MW)
                self.money += income
                xp_gain = 10 + self.level * 6
                self.xp += xp_gain
                events.append((f"Demanda satisfecha +€{income} +{xp_gain}XP", "good"))
            else:
                deficit = self.demand - self.production
                penalty = round(deficit * DEFICIT_PENALTY)
                self.money -= penalty
                events.append((f"Déficit {deficit} MW → -€{penalty}", "bad"))

                # Subida de nivel
                if self.level < len(LEVEL_XP) and self.xp >= self.xp_needed:
                    self.level += 1
                    self.xp = max(0, self.xp - self.xp_needed)
                    events.append((f"¡Nivel {self.level}! Nuevas fuentes.", "level"))

                # Crecimiento de demanda cada N turnos
                if self.turn % DEMAND_GROWTH_TURNS == 0:
                    rate = 0.10 + self.level * 0.02
                    inc = max(5, round(self.demand * rate))
                    self.demand += inc
                    events.append((f"La ciudad crece +{inc} MW", "info"))

                    # ── Helpers ───────────────────────────────────────────────────────────────
                    def _get_source(self, source_id):
                        for s in SOURCES_DATA:
                            if s["id"] == source_id:
                                return s
                        raise KeyError(source_id)

                    def _log(self, msg, color_key="info"):
                        from src.constants import LOG_MAX
                        self.log_entries.insert(0, (f"T{self.turn}: {msg}", color_key))
                        if len(self.log_entries) > LOG_MAX:
                            self.log_entries.pop()

                    def source_unlocked(self, source_id):
                        src = self._get_source(source_id)
                        return src["unlock_level"] <= self.level

