# 🐾 Desktop Pet

A custom desktop companion app — a cartoon character based on a real person, that lives on your desktop, watches what you do, wanders around showing off, and reacts when you interact with it.

Built with **Python + PyQt6**, runs natively on **Windows and Mac**.

---

## ✨ Features

- **Supervisor Mode** — Sits on your desktop and watches what software you have open. Reacts with different poses and speech bubbles depending on the app (e.g. judging you for too much Netflix or Bilibili, proud when you're coding). Supports both **English and Chinese** window titles.
- **Wanderer Mode** — Drives around your desktop in a toy race car, traveling clockwise around the screen edges, stopping to strike cool poses and flex.
- **Interactive Mode** — Right-click the character to trigger fun actions like slapping or floating.
- **Custom Character** — The cartoon sprite is generated from real photos using AI style transfer, then cleaned up with background removal.

---

## 🚗 Animation System - Toy Car

The character **drives in a sleek toy race car** during Wanderer Mode:

- **Single image per direction**: One sprite for left, one for right (no wheel animation frames needed)
- **Two directions**: Left-facing car and right-facing car
- **Sad version**: When dragged away from the path, the character looks sad while driving back to the edge

### Required Sprite Files

Place these in `assets/sprites/`:

**Normal Driving (Happy):**
- `car_left.png` - Character in toy car facing left
- `car_right.png` - Character in toy car facing right

**Sad Driving (After being dragged):**
- `car_sad_left.png` - Sad character in toy car facing left
- `car_sad_right.png` - Sad character in toy car facing right

**Design Tips:**
- Dark body race car with white racing stripes
- Character's upper body visible above car
- Transparent background on all sprites (PNG format)

---

## 🎮 Interactive Mode Actions

Right-click the character in Interactive Mode to access:

- **👋 Slap** - Playful slap (shock → spinning → dizzy, freezes until done)
- **🎈 Float** - Character levitates with a magical sparkly aura
- **📤 Unfloat** - Returns to ground (only shown while floating)
- **🍪 Feed** - Give them a treat (eating animation, then satisfied)
- **💕 Pet** - Pet them affectionately (happy → hearts, freezes until done)

All actions have special floating variations when performed while the character is levitating!

---

## 🌏 Supervisor Mode — Supported Apps

The supervisor reacts to both English and Chinese window titles:

**Streaming:** Netflix, YouTube, Twitch, Bilibili, iQIYI, Youku, Tencent Video  
**Social/Chat:** WeChat, QQ, Instagram, TikTok, Douyin, Xiaohongshu, Weibo  
**Games:** Steam, Genshin Impact, Minecraft, League of Legends, 王者荣耀, 和平精英  
**Shopping:** Amazon, Taobao, JD.com, Pinduoduo, Xianyu  
**Work:** VSCode, PyCharm, Excel, Word, Slack, Teams, DingTalk, Feishu, WPS  
**Browsers:** Chrome, Firefox, Edge, 360浏览器, QQ浏览器, 搜狗浏览器

---

## 📂 Project Structure

```
desktop_pet/
├── main.py                     # Entry point & context menu
├── character.py                # Sprite loading, animation frame logic
├── window_manager.py           # Transparent, always-on-top PyQt6 window
├── app_monitor.py              # Detects active apps (Windows + Mac)
├── mode_manager.py             # Manages and switches between the 3 modes
├── movement.py                 # Clockwise movement system for Wanderer mode
├── config.py                   # App reactions map, settings, tunable values
├── desktop_pet.spec            # PyInstaller packaging config
├── environment_windows.yml     # Windows conda environment
├── environment_mac.yml         # Mac conda environment
├── assets/
│   ├── icon.ico                # App icon (Windows)
│   └── sprites/                # PNG sprites — gitignored, keep local backup!
├── .github/
│   └── workflows/
│       └── build_mac.yml       # Automated Mac .app build via GitHub Actions
└── README.md
```

---

## 🛠️ Setup for Development

### Prerequisites
- **Windows 10/11** or **macOS**
- **Anaconda** or **Miniconda**
- **Git**

> On Windows, run all commands in **Anaconda Prompt**.

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/desktop_pet.git
cd desktop_pet
```

### 2. Create the Conda Environment

**Windows:**
```bash
conda env create -f environment_windows.yml
conda activate desktop_pet
```

**Mac:**
```bash
conda env create -f environment_mac.yml
conda activate desktop_pet
```

### 3. Add Your Sprites
Place all PNG sprite files in `assets/sprites/`. These are gitignored — keep a local backup.

### 4. Run
```bash
python main.py
```

---

## 📦 Packaging

### Windows → `.exe`
```bash
conda activate desktop_pet
pyinstaller desktop_pet.spec
```
Output: `dist/DesktopPet.exe` — single file, no installation needed.

### Mac → `.app` (no Mac required!)
The Mac build runs automatically on GitHub's servers via GitHub Actions:

1. Temporarily allow sprites in `.gitignore`, then push everything
2. Go to GitHub → **Actions** → **Build Mac App** → **Run workflow**
3. Wait ~1 minute → download **DesktopPet-mac** artifact
4. The workflow automatically removes assets from GitHub after building

The recipient right-clicks `DesktopPet.app` → **Open** → **Open** on first launch (unsigned app warning, only once).

---

## 🎨 Creating Sprites

### Recommended Workflow:
1. Generate base character using AI art tools (Midjourney, ChatGPT, etc.)
2. Remove background using `rembg` (included in environment):
   ```bash
   cd assets/sprites
   rembg i input.png output_nobg.png
   ```
3. Export as PNG with transparent background at 200×200px or larger

### All Required Sprites (32 total):
| Category | Files |
|----------|-------|
| Idle | `idle_open.png`, `idle_blink.png` |
| Driving | `car_left.png`, `car_right.png` |
| Sad driving | `car_sad_left.png`, `car_sad_right.png` |
| Drag | `dragged_ear.png`, `touching_ears_sad.png` |
| Supervisor reactions | `judging.png`, `proud.png`, `surprised.png`, `disappointed.png`, `working_hard.png`, `playing_game.png` |
| Slap | `slap_shocked.png`, `slap_spinning.png`, `slap_dizzy.png` |
| Feed | `eating_1.png`, `satisfied_happy.png` |
| Pet | `pet_happy_1.png`, `pet_happy_2.png`, `pet_hearts.png` |
| Float | `float_active.png`, `float_calm.png` |
| Float + Slap | `float_slap_shocked.png`, `float_slap_spinning.png`, `float_slap_dizzy.png` |
| Float + Feed | `float_eating_1.png`, `float_satisfied.png` |
| Float + Pet | `float_pet_happy_1.png`, `float_pet_happy_2.png`, `float_pet_hearts.png` |

---

## 🗺️ Development Roadmap

| Phase | What | Status |
|-------|------|--------|
| 1 | Project setup, Git, Conda env | ✅ Done |
| 2 | Core transparent window + sprite display | ✅ Done |
| 3 | Sprite animation (blinking, driving frames) | ✅ Done |
| 4 | Mode 1 — Supervisor (app detection + reactions) | ✅ Done |
| 5 | Mode 2 — Wanderer (clockwise driving + poses) | ✅ Done |
| 6 | Mode 3 — Interactive (click actions) | ✅ Done |
| 7 | Cross-platform (Mac support + packaging) | ✅ Done |

---

## 🛡️ License

This is a personal project. No license file included — not intended for public distribution.
