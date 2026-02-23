# 🐾 Desktop Pet

A custom desktop companion app — a cartoon character based on a real person, that lives on your desktop, watches what you do, wanders around showing off, and reacts when you interact with it.

Built with **Python + PyQt6**, runs natively on **Windows**.

---

## ✨ Features

- **Supervisor Mode** — Sits on your desktop and watches what software you have open. Reacts with different poses and speech bubbles depending on the app (e.g. judging you for too much Netflix, proud when you're coding).
- **Wanderer Mode** — Drives around your desktop in a toy car, traveling clockwise around the screen edges, stopping to strike cool poses and flex.
- **Interactive Mode** — Click the character to trigger fun actions like slapping or hanging.
- **Custom Character** — The cartoon sprite is generated from real photos using AI style transfer, then cleaned up with background removal.

---

## 🚗 Animation System - Toy Car Concept

Since walking animations are difficult to create, the character **drives in a cute toy car** during Wanderer Mode! This means:

- **Movement is simplified**: The character sits in one pose inside a toy car
- **The car creates the motion effect**: Animated wheels rolling give the impression of movement
- **Two directions**: Left-facing car and right-facing car
- **Sad version**: When dragged away from the path, the character looks sad while driving back to the edge

### Required Sprite Files for Toy Car System

Place these in `assets/sprites/`:

**Normal Driving (Happy):**
- `car_left_1.png` - Character in toy car facing left (wheels position 1)
- `car_left_2.png` - Character in toy car facing left (wheels position 2 - rolled forward)
- `car_right_1.png` - Character in toy car facing right (wheels position 1)
- `car_right_2.png` - Character in toy car facing right (wheels position 2 - rolled forward)

**Sad Driving (After being dragged):**
- `car_sad_left_1.png` - Sad character in toy car facing left (wheels position 1)
- `car_sad_left_2.png` - Sad character in toy car facing left (wheels position 2)
- `car_sad_right_1.png` - Sad character in toy car facing right (wheels position 1)
- `car_sad_right_2.png` - Sad character in toy car facing right (wheels position 2)

**Design Tips:**
- Keep the character's pose simple (sitting, maybe holding steering wheel)
- Use a simple, cute toy car design (colorful, child-like)
- Animate just the wheels between frames (rotate them slightly)
- For sad version, change character's expression (droopy ears, sad eyes) but keep car the same
- Transparent background on all sprites (PNG format)

---

## 📂 Project Structure

```
desktop_pet/
├── main.py                 # Application entry point & main event loop
├── character.py            # Sprite loading, animation frame logic
├── window_manager.py       # Transparent, always-on-top PyQt6 window
├── app_monitor.py          # Detects active/open applications on Windows
├── mode_manager.py         # Manages and switches between the 3 modes
├── movement.py             # Clockwise movement system for Wanderer mode
├── config.py               # App reactions map, settings, tunable values
├── assets/
│   └── sprites/            # PNG sprites with transparent backgrounds (gitignored)
├── environment.yml         # Conda environment definition
├── .gitignore
└── README.md               # This file
```

---

## 🛠️ Setup (Windows + Anaconda)

### 1. Prerequisites

- **Windows 10/11**
- **Anaconda** or **Miniconda** installed on Windows
- **Git** installed on Windows

> **Important:** All commands below should be run inside **Anaconda Prompt**, not PowerShell or Windows Terminal. Search for "Anaconda Prompt" in your Start menu.

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/desktop_pet.git
cd desktop_pet
```

### 3. Create the Conda Environment

```bash
conda env create -f environment.yml
conda activate desktop_pet
```

### 4. Verify the Environment

```bash
python --version       # Should show 3.11.x
pip list               # Confirm PyQt6, Pillow, psutil, pywin32, etc. are installed
```

### 5. Add Your Sprites

Generate or commission your cartoon sprites following the toy car concept above, then place them in:

```
assets/sprites/
```

These are gitignored on purpose — they contain your personal likeness and can be large image files. Keep a local backup.

---

## 🚀 Running the App (Development)

Open **Anaconda Prompt**, then:

```bash
conda activate desktop_pet
python main.py
```

Right-click on the character to switch between modes:
- **📊 Supervisor Mode** - Watches your apps and reacts
- **🚶 Wanderer Mode** - Drives around in toy car, striking poses
- **🎮 Interactive Mode** - Manual control with actions (Slap, Hang, Feed, Pet)

---

## 🎨 Creating Sprites

### Recommended Workflow:

1. **Generate base character** using AI art tools (Midjourney, Stable Diffusion, etc.)
2. **Remove background** using tools like remove.bg or rembg (included in environment)
3. **Create toy car template** - design a simple, cute toy car in your art style
4. **Compose sprites** - place character in car, create 2 frames with slightly rotated wheels
5. **Export as PNG** with transparent background at 200x200px (or larger, will be auto-scaled)

### Tips:
- Keep character pose consistent across all car sprites
- Only animate the wheels between frames for simplicity
- Use bright, cheerful colors for the car
- Add small details like exhaust puffs or motion lines for extra charm

---

## 📦 Packaging (Later)

When the app is complete, it will be packaged into a single Windows `.exe` using PyInstaller so the end user just double-clicks to launch. Details will be added here in a later phase.

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
| 7 | Polish: system tray, settings, packaging | ⬜ Planned |

---

## 🎮 Interactive Mode Actions

When in Interactive Mode, right-click the character to access these actions:

- **👋 Slap** - Give them a playful slap (shows shock and spinning reaction)
- **🪢 Hang** - Hang them with a rope (they struggle, then dangle calmly)
- **📤 Unhang** - Release them from hanging (only shown when hanging)
- **🍪 Feed** - Give them a treat (eating animation, then satisfied)
- **💕 Pet** - Pet them affectionately (happy reaction with hearts)

All actions have special variations when performed while the character is hanging!

---

## 🛡️ License

This is a personal project. No license file included — not intended for public distribution.
