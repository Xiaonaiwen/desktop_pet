# config.py
# ---------------------------------------------------------------------------
# Central configuration for the desktop pet.
# Change values here to tweak behaviour without touching other files.
# ---------------------------------------------------------------------------

import os

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPRITES_DIR = os.path.join(BASE_DIR, "assets", "sprites")

# ---------------------------------------------------------------------------
# Window settings
# ---------------------------------------------------------------------------
WINDOW_WIDTH = 200
WINDOW_HEIGHT = 200

# Default starting position (pixels from top-left of screen).
# None means centre of screen.
WINDOW_START_X = None
WINDOW_START_Y = None

# ---------------------------------------------------------------------------
# Animation settings
# ---------------------------------------------------------------------------
ANIMATION_TICK_MS = 100

ANIMATIONS = {
    "idle": [
        ("idle_open.png",  600),
        ("idle_open.png",  400),
        ("idle_blink.png", 150),
    ],
    "walk_left": [
        ("walk_left_1.png", 150),
        ("walk_left_2.png", 150),
    ],
    "walk_right": [
        ("walk_right_1.png", 150),
        ("walk_right_2.png", 150),
    ],
    # Supervisor reaction animations — when you have real sprites,
    # add the actual filenames here. For now they fall back to placeholder.
    "judging": [
        ("judging.png", 2000),
    ],
    "proud": [
        ("proud.png", 2000),
    ],
    "surprised": [
        ("surprised.png", 2000),
    ],
    "disappointed": [
        ("disappointed.png", 2000),
    ],
    "working_hard": [
        ("working_hard.png", 2000),
    ],
    "playing_game": [
        ("playing_game.png", 2000),
    ],
}

DEFAULT_ANIMATION = "idle"

# ---------------------------------------------------------------------------
# Supervisor Mode — app detection and reactions
# ---------------------------------------------------------------------------
# How often (in ms) the app monitor checks the active window.
# 2000ms = checks every 2 seconds. Don't set too low — it wastes CPU.
APP_CHECK_INTERVAL_MS = 2000

# Reaction map: maps keywords in window titles to (animation, speech bubble text).
# Checked in order — first match wins. Put more specific apps before general ones.
# The keyword matching is case-insensitive.
APP_REACTIONS = [
    # --- Streaming / Entertainment ---
    ("netflix",     "judging",       "Really? Netflix again? 👀"),
    ("youtube",     "judging",       "YouTube rabbit hole detected... 🐰"),
    ("twitch",      "surprised",     "Watching streams? Interesting..."),

    # --- Social Media / Chat ---
    ("wechat",      "judging",       "又在摸鱼吗？专注！"),
    ("weixin",      "judging",       "又在摸鱼吗？专注！"),
    ("qq",          "judging",       "又在摸鱼吗？专注！"),
    ("instagram",   "disappointed",  "Scrolling Instagram? Come on..."),
    ("twitter",     "disappointed",  "Twitter? In this economy? 😏"),
    ("facebook",    "surprised",     "Facebook? Really? 👀"),
    ("tiktok",      "judging",       "TikTok? You're never getting that time back."),

    # --- Coding / Productivity ---
    ("notion",      "working_hard",  "我们一起努力✍️"),
    ("visual studio code", "proud",  "Coding! I'm proud of you! 💪"),
    ("vscode",      "proud",         "Coding! I'm proud of you! 💪"),
    ("pycharm",     "proud",         "Python dev! That's my person! 🐍"),
    ("intellij",    "proud",         "Java? Bold choice. I respect it."),
    ("notepad++",   "proud",         "Writing code? Nice! 👍"),

    # --- Games ---
    ("steam",       "playing_game",  "Let's play together! 🎮"),
    ("genshin",     "surprised",     "Genshin Impact?! Pull me something good! ✨"),
    ("minecraft",   "proud",         "Building things! Creative! 🧱"),
    ("fortnite",    "judging",       "Fortnite? Seriously? 😒"),

    # --- Shopping ---
    ("amazon",      "surprised",     "Shopping again? 🛒"),
    ("ebay",        "surprised",     "eBay? What are you hunting for? 🔍"),

    # --- Work / School ---
    ("excel",       "proud",         "Spreadsheets! You're a boss! 📊"),
    ("word",        "proud",         "Writing something important? 📝"),
    ("powerpoint",  "proud",         "Making a presentation? Go you! 🎯"),
    ("google docs", "proud",         "Docs! Productive day? 👏"),
    ("slack",       "proud",         "Working hard! I see you! 💼"),
    ("teams",       "surprised",     "Another meeting? Hang in there..."),

    # --- Web Browsers (put AFTER specific site checks) ---
    ("chrome",      "idle",          None),   # None = no speech bubble
    ("firefox",     "idle",          None),
    ("edge",        "idle",          None),
]

# How long (in ms) a speech bubble stays visible before disappearing.
SPEECH_BUBBLE_DURATION_MS = 3000

# ---------------------------------------------------------------------------
# Placeholder colour (used when no sprite file exists yet)
# ---------------------------------------------------------------------------
PLACEHOLDER_COLOR = (100, 149, 237)   # cornflower blue (R, G, B)
