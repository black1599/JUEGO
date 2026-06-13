# ⚡ Energy Manager — Simulador de Gestión de Energía

## Instalación y ejecución

### Requisitos
- Python 3.10+
- pygame 2.x

### Pasos
```bash
# 1. Instalar dependencia
pip install pygame

# 2. Ejecutar el juego
python main.py
```

En **PyCharm**: abre la carpeta `energy_manager` como proyecto, instala pygame en el intérprete y ejecuta `main.py`.

---

## Cómo jugar

### Objetivo
Mantener la producción de energía ≥ demanda de la ciudad mientras gestionas el presupuesto.

### Mecánicas
| Acción | Efecto |
|---|---|
| **Comprar fuente** | Clic en una tarjeta del sidebar |
| **Siguiente turno** | Cobra ingresos / paga costes / crece demanda |
| **Vender exceso** | Vende los MW sobrantes por dinero |
| **Reiniciar** | Comienza desde el principio |

### Economía por turno
- **Ingresos**: €3 por MW satisfecho
- **Déficit**: -€5 por MW en falta
- **Costes operativos**: según las fuentes construidas
- **Contaminación > 20**: multa ambiental cada turno
- **Eventos aleatorios**: subvenciones o averías (10% cada uno)

### Progresión
| Nivel | Novedad |
|---|---|
| 1 | Carbón, Solar, Eólico |
| 2 | Hidroeléctrica, Gas Natural |
| 3 | Nuclear |
| 4 | Geotérmica |
| 5 | Fusión Nuclear |

La demanda crece cada 3 turnos. ¡Si el dinero baja de -€800, quiebras!

---

## Estructura del proyecto
```
energy_manager/
├── main.py          ← Punto de entrada
├── requirements.txt
├── README.md
└── src/
    ├── __init__.py
    ├── constants.py ← Todos los valores configurables
    ├── state.py     ← Lógica del juego (sin pygame)
    ├── ui.py        ← Widgets: botones, barras, tarjetas
    ├── city.py      ← Renderizador de ciudad animada
    └── game.py      ← Bucle principal y pantallas
```
