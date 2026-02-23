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
    # TOY CAR ANIMATIONS - Character sits in a cute toy car
    # The character sprite stays in one pose, the car underneath creates the movement
    "driving_left": [
        ("car_left.png", 150),  # Character in toy car facing left
    ],
    "driving_right": [
        ("car_right.png", 150),  # Character in toy car facing right
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
    # SAD DRIVING ANIMATIONS - Character looks sad while in the toy car
    "driving_sad_left": [
        ("car_sad_left.png", 150),  # Sad character in toy car facing left
    ],
    "driving_sad_right": [
        ("car_sad_right.png", 150),  # Sad character in toy car facing right
    ],
    "touching_ears_sad": [
        ("touching_ears_sad.png", 2000),  # Touching own ears sadly after being dragged
    ],
    # Interactive Mode - Slap reaction
    "slap_reaction": [
        ("slap_shocked.png",  600),   # Initial shock - held longer
        ("slap_spinning.png", 400),   # Spinning from impact
        ("slap_spinning.png", 400),   # Loop
        ("slap_dizzy.png",   9999),   # Dizzy - freeze here until action ends
    ],
    # Interactive Mode - Float action (character levitates with magical sparkly aura)
    "float_active": [
        ("float_active.png", 300),   # Character floating with magical aura, active
        ("float_active.png", 300),   # (loops - same frame for consistency)
    ],
    "float_calm": [
        ("float_calm.png", 2000),  # Character floating peacefully, calm
    ],
    # Interactive Mode - Feed action
    "eating": [
        ("eating_1.png", 9999),  # Eating - single frame, freeze until action ends
    ],
    "eating_satisfied": [
        ("satisfied_happy.png", 1500),  # Content after eating
    ],
    # Interactive Mode - Pet action
    "petting_happy": [
        ("pet_happy_1.png", 600),   # Eyes closed, smiling
        ("pet_happy_2.png", 600),   # Slight movement
        ("pet_hearts.png",  9999),  # Hearts appear - freeze here until action ends
    ],
    # Interactive Mode - Float combinations (different animations when floating)
    "float_slap_reaction": [
        ("float_slap_shocked.png",  600),   # Shocked while floating - held longer
        ("float_slap_spinning.png", 400),   # Spinning from impact while floating
        ("float_slap_dizzy.png",   9999),   # Dizzy - freeze here until action ends
    ],
    "float_eating": [
        ("float_eating_1.png", 9999),  # Eating while floating - single frame, freeze
    ],
    "float_eating_satisfied": [
        ("float_satisfied.png", 1500),  # Content after eating, still floating
    ],
    "float_petting_happy": [
        ("float_pet_happy_1.png", 600),   # Happy while floating
        ("float_pet_happy_2.png", 600),   # Enjoying pets while floating
        ("float_pet_hearts.png",  9999),  # Hearts appear - freeze here until action ends
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
    # Chinese streaming
    ("bilibili",    "judging",       "B站又刷了多久了? 👀"),
    ("哔哩哔哩",     "judging",       "B站又刷了多久了? 👀"),
    ("爱奇艺",       "judging",       "追剧呢? 专注一点! 📺"),
    ("iqiyi",       "judging",       "追剧呢? 专注一点! 📺"),
    ("优酷",         "judging",       "又在看视频? 😑"),
    ("youku",       "judging",       "又在看视频? 😑"),
    ("腾讯视频",     "judging",       "腾讯视频? 去学习! 📺"),
    ("芒果tv",       "judging",       "追综艺呢? 😏"),

    # --- Social Media / Chat ---
    ("wechat",      "judging",       "又在摸鱼吗? 专注!"),
    ("weixin",      "judging",       "又在摸鱼吗? 专注!"),
    ("微信",         "judging",       "又在摸鱼吗? 专注!"),
    ("qq",          "judging",       "QQ挂着呢? 专注工作!"),
    ("腾讯qq",       "judging",       "QQ挂着呢? 专注工作!"),
    ("instagram",   "disappointed",  "Scrolling Instagram? Come on..."),
    ("twitter",     "disappointed",  "Twitter? In this economy? 😬"),
    ("facebook",    "surprised",     "Facebook? Really? 👀"),
    ("tiktok",      "judging",       "TikTok? You're never getting that time back."),
    ("抖音",         "judging",       "抖音刷起来了? 时间都没了! 📱"),
    ("小红书",       "judging",       "逛小红书呢? 种草可以等等! 🌿"),
    ("微博",         "judging",       "刷微博? 摸鱼被我抓到了! 🐟"),
    ("weibo",       "judging",       "刷微博? 摸鱼被我抓到了! 🐟"),

    # --- Coding / Productivity ---
    ("notion",      "working_hard",  "我们一起努力✊"),
    ("visual studio code", "proud",  "Coding! I'm proud of you! 💪"),
    ("vscode",      "proud",         "Coding! I'm proud of you! 💪"),
    ("pycharm",     "proud",         "Python dev! That's my person! 🐍"),
    ("intellij",    "proud",         "Java? Bold choice. I respect it."),
    ("notepad++",   "proud",         "Writing code? Nice! 👍"),
    ("记事本",       "proud",         "在写东西? 继续加油! 📝"),

    # --- Games ---
    ("steam",       "playing_game",  "Let's play together! 🎮"),
    ("genshin",     "surprised",     "Genshin Impact?! Pull me something good! ✨"),
    ("原神",         "surprised",     "原神启动?! 抽到SSR了吗! ✨"),
    ("minecraft",   "proud",         "Building things! Creative! 🧱"),
    ("我的世界",     "proud",         "建造中! 好有创意! 🧱"),
    ("fortnite",    "judging",       "Fortnite? Seriously? 😑"),
    ("王者荣耀",     "playing_game",  "王者上分中? 别送! 🏆"),
    ("英雄联盟",     "playing_game",  "打LOL呢? carry全场! ⚔️"),
    ("league of legends", "playing_game", "Playing League? Carry them! ⚔️"),
    ("和平精英",     "playing_game",  "吃鸡去了? 稳住! 🍗"),
    ("pubg",        "playing_game",  "PUBG? Don't get thirsted! 🍗"),
    ("崩坏",         "playing_game",  "崩坏开舰了? 氪金警告! 💸"),
    ("明日方舟",     "playing_game",  "方舟肝活动? 注意休息! 🎮"),

    # --- Shopping ---
    ("amazon",      "surprised",     "Shopping again? 🛒"),
    ("ebay",        "surprised",     "eBay? What are you hunting for? 🔍"),
    ("taobao",      "surprised",     "淘宝购物中? 钱包注意了! 🛒"),
    ("淘宝",         "surprised",     "淘宝购物中? 钱包注意了! 🛒"),
    ("天猫",         "surprised",     "天猫购物? 克制一下! 🛍️"),
    ("tmall",       "surprised",     "天猫购物? 克制一下! 🛍️"),
    ("京东",         "surprised",     "京东买买买? 钱不是大风刮来的! 💸"),
    ("jd.com",      "surprised",     "京东买买买? 钱不是大风刮来的! 💸"),
    ("拼多多",       "judging",       "拼多多砍一刀? 真的有用吗... 😑"),
    ("pinduoduo",   "judging",       "拼多多砍一刀? 真的有用吗... 😑"),
    ("闲鱼",         "surprised",     "逛闲鱼? 淘到宝了吗? 🐟"),

    # --- Work / School ---
    ("excel",       "proud",         "Spreadsheets! You're a boss! 📊"),
    ("word",        "proud",         "Writing something important? 📝"),
    ("powerpoint",  "proud",         "Making a presentation? Go you! 🎯"),
    ("google docs", "proud",         "Docs! Productive day? 👍"),
    ("slack",       "proud",         "Working hard! I see you! 💼"),
    ("teams",       "surprised",     "Another meeting? Hang in there..."),
    ("钉钉",         "proud",         "打卡了! 好员工! 💼"),
    ("dingtalk",    "proud",         "打卡了! 好员工! 💼"),
    ("飞书",         "proud",         "用飞书干活? 效率很高嘛! 🚀"),
    ("lark",        "proud",         "Lark open! Stay productive! 🚀"),
    ("企业微信",     "proud",         "企业微信工作中! 加油! 💪"),
    ("wps",         "proud",         "WPS工作中! 认真的样子很帅! 📄"),

    # --- Web Browsers (put AFTER specific site checks) ---
    ("chrome",      "idle",          None),
    ("firefox",     "idle",          None),
    ("edge",        "idle",          None),
    ("360安全浏览器", "idle",         None),
    ("360极速浏览器", "idle",         None),
    ("qq浏览器",     "idle",          None),
    ("搜狗浏览器",   "idle",          None),
    ("uc浏览器",     "idle",          None),
]

# How long (in ms) a speech bubble stays visible before disappearing.
SPEECH_BUBBLE_DURATION_MS = 3000

# ---------------------------------------------------------------------------
# Wanderer Mode settings
# ---------------------------------------------------------------------------
# How often (in ms) the movement controller updates position during driving.
# 50ms = 20 updates per second for smooth movement.
MOVEMENT_UPDATE_INTERVAL_MS = 50

# Movement speed (pixels per update tick).
# At 50ms intervals, speed of 3 = 60 pixels/second.
DRIVE_SPEED = 3  # Renamed from WALK_SPEED

# Edge strip thickness - defines how wide the edge zones are (pixels).
# Pet will ONLY visit the edge strips (left, right, top, bottom).
# Larger value = thicker edge strips (more room for pet to wander).
# Smaller value = thinner edge strips (pet stays closer to screen borders).
CENTER_AVOID_MARGIN = 250  # Also called edge_thickness in movement.py

# Duration ranges for driving and posing (in seconds).
# Renamed from walking to driving
MIN_DRIVE_DURATION = 3
MAX_DRIVE_DURATION = 8
MIN_POSE_DURATION = 2
MAX_POSE_DURATION = 5
MIN_IDLE_DURATION = 1
MAX_IDLE_DURATION = 3

# Chance (0.0 to 1.0) that the character will do a pose after finishing driving.
# 0.7 = 70% chance to pose, 30% chance to just go idle.
POSE_AFTER_DRIVE_CHANCE = 0.7  # Renamed from POSE_AFTER_WALK_CHANCE

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

# Float behavior timings
FLOAT_ACTIVE_DURATION_MS = 3000   # How long to float actively before going calm
FLOAT_CALM_DURATION_MS = 5000     # How long to float calmly before going active again
