"""
Presenter — Energy Manager
"""

from src.state import GameState
from src.view import GameView
from src.constants import SOURCES_DATA, GREEN_LIGHT, RED, GRAY_LIGHT


SIDEBAR_X = 860   # = SCREEN_W - SIDEBAR_W
TOPBAR_H = 90


class GamePresenter:
    """
    Patrón MVP:
      Model     → GameState  (lógica y datos puros)
      View      → GameView   (renderizado pygame)
      Presenter → este archivo (mediador sin estado propio de juego)
    """

    def __init__(self, view: GameView):
        self._model = GameState()
        self._view = view
        self._screen_mode = "game"   # "game" | "gameover"

        # Conectar callbacks de la vista a métodos del presenter
        self._view.on_next_turn = self._on_next_turn
        self._view.on_sell_excess = self._on_sell_excess
        self._view.on_reset = self._on_reset
        self._view.on_buy_source = self._on_buy_source

    # Bucle principal llamado desde main

    def handle_event(self, event):
        snapshot = self._build_snapshot()
        self._view.handle_event(event, self._screen_mode, snapshot)

    def update(self, dt: float):
        self._view.update(dt, self._model.level)

    def render(self):
        snapshot = self._build_snapshot()
        self._view.render(snapshot)

    # Snapshot: convierte el estado del modelo en datos planos para la vista

    def _build_snapshot(self) -> dict:
        m = self._model

        return {
            "screen_mode": self._screen_mode,

            # Turno / progresión
            "turn": m.turn,
            "total_turns": m.total_turns,
            "level": m.level,
            "xp": m.xp,
            "xp_needed": m.xp_needed,

            # Economía / energía
            "money": m.money,
            "production": m.production,
            "demand": m.demand,
            "balance": m.balance,
            "pollution": m.pollution,

            # Plantas poseídas
            "owned": dict(m.owned),

            # Log
            "log_entries": list(m.log_entries),
        }

    # Callbacks de acciones de UI hacia el modelo

    def _on_next_turn(self):
        events = self._model.next_turn()

        if events:
            for msg, col_key in events:
                from src.ui import LOG_COLORS

                c = LOG_COLORS.get(col_key, GRAY_LIGHT)

                self._view.add_float(
                    msg,
                    (SIDEBAR_X + 170, TOPBAR_H + 20),
                    c
                )

        if self._model.game_over:
            self._screen_mode = "gameover"

    def _on_sell_excess(self):
        earned = self._model.sell_excess()

        if earned:
            self._view.add_float(
                f"+€{earned}",
                (SIDEBAR_X + 170, 690),
                GREEN_LIGHT,
            )

    def _on_reset(self):
        self._model.reset()
        self._screen_mode = "game"

    def _on_buy_source(self, source_id: str):
        src_data = next(s for s in SOURCES_DATA if s["id"] == source_id)

        # Buscar la tarjeta para saber su posición visual
        card_pos = None

        for card, sid in self._view.cards:
            if sid == source_id:
                card_pos = card.rect.midtop
                break

        ok, msg = self._model.buy(source_id)

        if card_pos:
            if ok:
                self._view.add_float(
                    f"+{src_data['mw']} MW",
                    card_pos,
                    GREEN_LIGHT
                )
            else:
                self._view.add_float(
                    msg,
                    card_pos,
                    RED
                )