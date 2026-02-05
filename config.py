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
    # Drag interaction animations
    "dragged_by_ear": [
        ("dragged_ear.png", 100),  # Hand grabbing elongated ear - fast loop for smooth drag
    ],
    "sad_walk_left": [
        ("sad_walk_left_1.png", 150),  # Sad walking left with elongated ears
        ("sad_walk_left_2.png", 150),
    ],
    "sad_walk_right": [
        ("sad_walk_right_1.png", 150),  # Sad walking right with elongated ears
        ("sad_walk_right_2.png", 150),
    ],
    "touching_ears_sad": [
        ("touching_ears_sad.png", 2000),  # Touching own ears sadly after being dragged
    ],
    # Interactive Mode - Slap reaction
    "slap_reaction": [
        ("slap_shocked.png",  200),   # Initial shock
        ("slap_spinning.png", 150),   # Spinning from impact
        ("slap_spinning.png", 150),   # Loop
        ("slap_spinning.png", 150),   # Loop
        ("slap_dizzy.png",   1000),   # Dizzy with stars
    ],
    # Interactive Mode - Hang action (sprite shows rope circling character + roof)
    "hang_struggling": [
        ("hang_struggling.png", 300),   # Character wrapped in rope, struggling
        ("hang_struggling.png", 300),   # (loops - same frame for consistency)
    ],
    "hang_dangling": [
        ("hang_dangling.png", 2000),  # Character wrapped in rope, calm/resigned
    ],
    # Interactive Mode - Feed action
    "eating": [
        ("eating_1.png", 400),  # Taking bite
        ("eating_2.png", 400),  # Chewing
        ("eating_1.png", 400),  # Another bite
    ],
    "eating_satisfied": [
        ("satisfied_happy.png", 1500),  # Content after eating
    ],
    # Interactive Mode - Pet action
    "petting_happy": [
        ("pet_happy_1.png", 300),  # Eyes closed, smiling
        ("pet_happy_2.png", 300),  # Slight movement
        ("pet_hearts.png",  800),  # Hearts appear
    ],
    # Interactive Mode - Hang combinations (different animations when hanging)
    "hang_slap_reaction": [
        ("hang_slap_shocked.png",  200),   # Shocked while hanging in rope
        ("hang_slap_spinning.png", 150),   # Spinning in rope from impact
        ("hang_slap_spinning.png", 150),   # Loop
        ("hang_slap_dizzy.png",   1000),   # Dizzy with stars, still in rope
    ],
    "hang_eating": [
        ("hang_eating_1.png", 400),  # Taking bite while hanging
        ("hang_eating_2.png", 400),  # Chewing while hanging
        ("hang_eating_1.png", 400),  # Another bite while hanging
    ],
    "hang_eating_satisfied": [
        ("hang_satisfied.png", 1500),  # Content after eating, still hanging
    ],
    "hang_petting_happy": [
        ("hang_pet_happy_1.png", 300),  # Happy while hanging
        ("hang_pet_happy_2.png", 300),  # Enjoying pets while hanging
        ("hang_pet_hearts.png",  800),  # Hearts appear while hanging
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
# Wanderer Mode settings
# ---------------------------------------------------------------------------
# How often (in ms) the movement controller updates position during walking.
# 50ms = 20 updates per second for smooth movement.
MOVEMENT_UPDATE_INTERVAL_MS = 50

# Movement speed (pixels per update tick).
# At 50ms intervals, speed of 3 = 60 pixels/second.
WALK_SPEED = 3

# Edge strip thickness - defines how wide the edge zones are (pixels).
# Pet will ONLY visit the edge strips (left, right, top, bottom).
# Larger value = thicker edge strips (more room for pet to wander).
# Smaller value = thinner edge strips (pet stays closer to screen borders).
CENTER_AVOID_MARGIN = 250  # Also called edge_thickness in movement.py

# Duration ranges for walking and posing (in seconds).
MIN_WALK_DURATION = 3
MAX_WALK_DURATION = 8
MIN_POSE_DURATION = 2
MAX_POSE_DURATION = 5
MIN_IDLE_DURATION = 1
MAX_IDLE_DURATION = 3

# Chance (0.0 to 1.0) that the character will do a pose after finishing a walk.
# 0.7 = 70% chance to pose, 30% chance to just go idle.
POSE_AFTER_WALK_CHANCE = 0.7

# List of pose animations to randomly choose from in Wanderer mode.
# Make sure these exist in the ANIMATIONS dict above!
WANDERER_POSES = [
    "proud",          # Proud stance
    "surprised",      # Surprised look
    "judging",        # Judgmental pose
    "disappointed",   # Disappointed look
    "working_hard",   # Working hard pose
    "playing_game",   # Playing game pose
]

# ---------------------------------------------------------------------------
# Placeholder colour (used when no sprite file exists yet)
# ---------------------------------------------------------------------------
PLACEHOLDER_COLOR = (100, 149, 237)   # cornflower blue (R, G, B)

# ---------------------------------------------------------------------------
# Interactive Mode settings
# ---------------------------------------------------------------------------
# Duration actions play before returning to idle (in milliseconds)
SLAP_REACTION_DURATION_MS = 2000
EATING_DURATION_MS = 2000
SATISFIED_DURATION_MS = 1500
PETTING_DURATION_MS = 1500

# Hang behavior timings
HANG_STRUGGLING_DURATION_MS = 3000  # How long to struggle before dangling
HANG_DANGLING_DURATION_MS = 5000    # How long to dangle before struggling again

