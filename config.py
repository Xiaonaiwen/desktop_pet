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
# Animation settings
# ---------------------------------------------------------------------------
# How often the animation timer ticks, in milliseconds.
# Lower = smoother but uses more CPU. 100ms = 10 frames per second.
ANIMATION_TICK_MS = 100

# ---------------------------------------------------------------------------
# Sprite definitions
# ---------------------------------------------------------------------------
# Each animation is a list of (filename, duration_in_ms) tuples.
# The character cycles through these frames in order, then loops.
#
# When you have real sprites, add the actual filenames here.
# For now, these files won't exist — the placeholder system will kick in
# and animate the placeholder box instead so you can see it working.
#
ANIMATIONS = {
    "idle": [
        ("idle_open.png",  600),   # eyes open — shown for 600ms
        ("idle_open.png",  400),   # eyes open again — shown for 400ms
        ("idle_blink.png", 150),   # eyes closed (blink) — shown for 150ms
    ],
    "walk_left": [
        ("walk_left_1.png", 150),
        ("walk_left_2.png", 150),
    ],
    "walk_right": [
        ("walk_right_1.png", 150),
        ("walk_right_2.png", 150),
    ],
}

# The animation that plays on startup
DEFAULT_ANIMATION = "idle"

# ---------------------------------------------------------------------------
# Placeholder colour (used when no sprite file exists yet)
# ---------------------------------------------------------------------------
# While you're still generating sprites, the app will show a coloured
# rectangle with this colour so you can see the window is working.
PLACEHOLDER_COLOR = (100, 149, 237)   # cornflower blue (R, G, B)
