# 🐾 Desktop Pet

A custom desktop companion app — a cartoon character based on a real person, that lives on your desktop, watches what you do, wanders around showing off, and reacts when you interact with it.

Built with **Python + PyQt6**, runs natively on **Windows**.

---

## ✨ Features

- **Supervisor Mode** — Sits on your desktop and watches what software you have open. Reacts with different poses and speech bubbles depending on the app (e.g. judging you for too much Netflix, proud when you're coding).
- **Wanderer Mode** — Walks around your desktop randomly, stopping to strike cool poses and flex.
- **Interactive Mode** — Click the character to trigger fun actions like slapping or hanging.
- **Custom Character** — The cartoon sprite is generated from real photos using AI style transfer, then cleaned up with background removal.

---

## 📂 Project Structure

```
desktop_pet/
├── main.py                 # Application entry point & main event loop
├── character.py            # Sprite loading, animation frame logic
├── window_manager.py       # Transparent, always-on-top PyQt6 window
├── app_monitor.py          # Detects active/open applications on Windows
├── mode_manager.py         # Manages and switches between the 3 modes
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

Generate or commission your cartoon sprites (see the guide in the outline), then place them in:

```
assets/sprites/
```

These are gitignored on purpose — they contain your personal likeness and can be large image files. Keep a local backup.

---

## 🚀 Running the App (Development)

> **Currently in early development.** Only the core window and sprite rendering are implemented so far.

Open **Anaconda Prompt**, then:

```bash
conda activate desktop_pet
python main.py
```

---

## 📦 Packaging (Later)

When the app is complete, it will be packaged into a single Windows `.exe` using PyInstaller so the end user just double-clicks to launch. Details will be added here in a later phase.

---

## 🗺️ Development Roadmap

| Phase | What | Status |
|-------|------|--------|
| 1 | Project setup, Git, Conda env | ✅ Done |
| 2 | Core transparent window + sprite display | 🔨 In Progress |
| 3 | Sprite animation (blinking, walking frames) | ⬜ Planned |
| 4 | Mode 1 — Supervisor (app detection + reactions) | ⬜ Planned |
| 5 | Mode 2 — Wanderer (random walk + poses) | ⬜ Planned |
| 6 | Mode 3 — Interactive (click actions) | ⬜ Planned |
| 7 | Polish: system tray, settings, packaging | ⬜ Planned |

---

## 🛡️ License

This is a personal project. No license file included — not intended for public distribution.
