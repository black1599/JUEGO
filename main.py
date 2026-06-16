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

        # ── Conectar callbacks de la vista a métodos del presenter ────────────
        self._view.on_next_turn   = self._on_next_turn
        self._view.on_sell_excess = self._on_sell_excess
        self._view.on_reset       = self._on_reset
        self._view.on_buy_source  = self._on_buy_source


    # ── Bucle principal (llamado desde main) ──────────────────────────────────

    def handle_event(self, event):
        snapshot = self._build_snapshot()
        self._view.handle_event(event, self._screen_mode, snapshot)

    def update(self, dt: float):
        self._view.update(dt, self._model.level)

    def render(self):
        snapshot = self._build_snapshot()
        self._view.render(snapshot)


    # ── Snapshot: convierte el estado del modelo en datos planos para la vista ─

    def _build_snapshot(self) -> dict:
        m = self._model
        return {
            "screen_mode": self._screen_mode,
            # Turno / progresión
            "turn":        m.turn,
            "total_turns": m.total_turns,
            "level":       m.level,
            "xp":          m.xp,
            "xp_needed":   m.xp_needed,
            # Economía / energía
            "money":       m.money,
            "production":  m.production,
            "demand":      m.demand,
            "balance":     m.balance,
            "pollution":   m.pollution,
            # Plantas poseídas
            "owned":       dict(m.owned),
            # Log
            "log_entries": list(m.log_entries),
        }
