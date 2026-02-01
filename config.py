# config.py
# ---------------------------------------------------------------------------
# Central configuration for the desktop pet.
# Change values here to tweak behaviour without touching other files.
# ---------------------------------------------------------------------------

import os

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
# Base directory: wherever this file lives (project root)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPRITES_DIR = os.path.join(BASE_DIR, "assets", "sprites")

# ---------------------------------------------------------------------------
# Window settings
# ---------------------------------------------------------------------------
# Default size of the pet window in pixels.
# Adjust to match your sprite resolution.
WINDOW_WIDTH = 200
WINDOW_HEIGHT = 200

# Default starting position (pixels from top-left of screen).
# None means centre of screen.
WINDOW_START_X = None
WINDOW_START_Y = None

# ---------------------------------------------------------------------------
# Sprite settings
# ---------------------------------------------------------------------------
# The default sprite image shown on startup.
# This is just a filename — the full path is built automatically from SPRITES_DIR.
DEFAULT_SPRITE = "idle.png"

# ---------------------------------------------------------------------------
# Placeholder colour (used when no sprite file exists yet)
# ---------------------------------------------------------------------------
# While you're still generating sprites, the app will show a coloured
# rectangle with this colour so you can see the window is working.
PLACEHOLDER_COLOR = (100, 149, 237)   # cornflower blue (R, G, B)
