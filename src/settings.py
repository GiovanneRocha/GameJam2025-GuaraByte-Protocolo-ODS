# -*- coding: utf-8 -*-
"""Runtime settings and dynamic scaling for portrait window.
Use init_runtime(width, height) to set the actual window size at runtime.
"""

# Base design resolution (portrait 9:16)
BASE_W, BASE_H = 540, 960

# These will be set at runtime by main.py
WIDTH, HEIGHT = BASE_W, BASE_H
SCALE = 1.0
FPS = 60
TITLE = "GuaraByte: Protocolo ODS — Portrait"

# Colors
COLOR_TEXT_DEFAULT = (255, 255, 255)
COLOR_TEXT_TYPING  = (0, 255, 255)
COLOR_TEXT_ERROR   = (255, 80, 80)
COLOR_PLAYER_INPUT = (120, 230, 160)
COLOR_PANEL_BG     = (22, 22, 30)

# Gameplay
CORRUPCAO_INICIAL = 100
CORRUPCAO_PERDA   = 10

# Spawn & speed (tuned for portrait)
BASE_SPAWN_INTERVAL = 1.3  # seconds between spawns at factor=1.0
MIN_SPAWN_INTERVAL  = 0.4
ENEMY_VY_RANGE      = (90.0, 220.0)  # px/s vertical
ENEMY_VX_RANGE      = (-35.0, 35.0)  # px/s horizontal drift
MARGIN_X = 18  # side safe area in px at base scale (scaled)
# Default base enemy speed (used by entities when no explicit speed passed).
# Chosen near the middle of ENEMY_VY_RANGE so behavior matches expected fall rates.
DEFAULT_ENEMY_SPEED = (ENEMY_VY_RANGE[0] + ENEMY_VY_RANGE[1]) / 2.0

# Fonts
PREF_FONT = None  # use system default; can point to a TTF path in assets/fonts

# Demo / recording
DEMO_DIR = None  # set by main

# Configurações de áudio
MUSIC_VOLUME = 0.1
SOUND_VOLUME = 0.1

# Dimensões iniciais da janela
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

# Resolução para tela cheia
FULLSCREEN_WIDTH = 1920
FULLSCREEN_HEIGHT = 1080


def init_runtime(width: int, height: int, demo_dir: str | None = None):
    global WIDTH, HEIGHT, SCALE, DEMO_DIR
    WIDTH, HEIGHT = width, height
    SCALE = min(WIDTH/BASE_W, HEIGHT/BASE_H)
    DEMO_DIR = demo_dir

# cores de texto usadas pela UI / menu / mensagens
COLOR_TEXT = (220, 220, 220)
COLOR_TEXT_ERROR = (255, 80, 80)