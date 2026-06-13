# ── Pantalla ──────────────────────────────────────────────────────────────────
SCREEN_W = 1000
SCREEN_H = 600

# ── Colores ───────────────────────────────────────────────────────────────────
BLACK       = (0,   0,   0)
WHITE       = (255, 255, 255)
DARK_BG     = (18,  22,  36)
PANEL_BG    = (26,  32,  50)
PANEL_LIGHT = (36,  44,  66)
BORDER      = (55,  65,  95)
BORDER_HL   = (90, 110, 160)

GREEN       = (39,  174, 96)
GREEN_DARK  = (27,  120, 66)
GREEN_LIGHT = (88,  214, 141)
RED         = (231, 76,  60)
RED_DARK    = (180, 50,  40)
ORANGE      = (230, 126, 34)
ORANGE_DARK = (180, 90,  20)
BLUE        = (52,  152, 219)
BLUE_DARK   = (30,  100, 180)
BLUE_LIGHT  = (110, 190, 240)
YELLOW      = (241, 196, 15)
YELLOW_DARK = (190, 150, 10)
PURPLE      = (155, 89,  182)
TEAL        = (26,  188, 156)
GRAY        = (100, 110, 130)
GRAY_LIGHT  = (150, 160, 180)
GRAY_DARK   = (60,  68,  88)

# ── Fuentes de energía ────────────────────────────────────────────────────────
SOURCES_DATA = [
    {
        "id": "coal",
        "name": "Carbón",
        "emoji": "C",
        "color": (120, 100, 80),
        "mw": 10,
        "cost": 80,
        "op_cost": 5,
        "pollutes": True,
        "pollution_amt": 3,
        "unlock_level": 1,
        "description": "Barato pero contaminante",
    },
    {
        "id": "solar",
        "name": "Solar",
        "emoji": "S",
        "color": (241, 196, 15),
        "mw": 8,
        "cost": 150,
        "op_cost": 1,
        "pollutes": False,
        "pollution_amt": 0,
        "unlock_level": 1,
        "description": "Limpia, bajo mantenimiento",
    },
    {
        "id": "wind",
        "name": "Eólico",
        "emoji": "W",
        "color": (110, 190, 240),
        "mw": 15,
        "cost": 220,
        "op_cost": 2,
        "pollutes": False,
        "pollution_amt": 0,
        "unlock_level": 1,
        "description": "Buena relación coste/MW",
    },
{
        "id": "hydro",
        "name": "Hidroeléctrica",
        "emoji": "H",
        "color": (52, 152, 219),
        "mw": 25,
        "cost": 400,
        "op_cost": 3,
        "pollutes": False,
        "pollution_amt": 0,
        "unlock_level": 2,
        "description": "Alta potencia y limpia",
    },
    {
        "id": "gas",
        "name": "Gas Natural",
        "emoji": "G",
        "color": (230, 126, 34),
        "mw": 22,
        "cost": 280,
        "op_cost": 9,
        "pollutes": True,
        "pollution_amt": 2,
        "unlock_level": 2,
        "description": "Rápido pero caro de operar",
    },
    {
        "id": "nuclear",
        "name": "Nuclear",
        "emoji": "N",
        "color": (155, 89, 182),
        "mw": 80,
        "cost": 1400,
        "op_cost": 18,
        "pollutes": False,
        "pollution_amt": 0,
        "unlock_level": 3,
        "description": "Enorme potencia, coste alto",
    },
    {
        "id": "geothermal",
        "name": "Geotérmica",
        "emoji": "T",
        "color": (231, 76, 60),
        "mw": 35,
        "cost": 700,
        "op_cost": 4,
        "pollutes": False,
        "pollution_amt": 0,
        "unlock_level": 4,
        "description": "Estable y muy eficiente",
    },
    {
        "id": "fusion",
        "name": "Fusión Nuclear",
        "emoji": "F",
        "color": (26, 188, 156),
        "mw": 200,
        "cost": 5500,
        "op_cost": 25,
        "pollutes": False,
        "pollution_amt": 0,
        "unlock_level": 5,
        "description": "El futuro de la energía",
    },
]

