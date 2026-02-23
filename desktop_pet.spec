# desktop_pet.spec
# ---------------------------------------------------------------------------
# PyInstaller spec file for Desktop Pet.
# Bundles all sprites inside the executable so no external files are needed.
#
# HOW TO BUILD:
#   Windows:  pyinstaller desktop_pet.spec
#   Mac:      pyinstaller desktop_pet.spec
#
# Output:
#   Windows:  dist/DesktopPet.exe  (single file)
#   Mac:      dist/DesktopPet.app  (app bundle)
# ---------------------------------------------------------------------------

import sys
import os

block_cipher = None

# ---------------------------------------------------------------------------
# Sprite files to bundle — all PNGs from assets/sprites/
# Format: (source_path, destination_folder_inside_bundle)
# ---------------------------------------------------------------------------
sprite_files = [
    "car_left.png",
    "car_right.png",
    "car_sad_left.png",
    "car_sad_right.png",
    "disappointed.png",
    "dragged_ear.png",
    "eating_1.png",
    "float_active.png",
    "float_calm.png",
    "float_eating_1.png",
    "float_pet_happy_1.png",
    "float_pet_happy_2.png",
    "float_pet_hearts.png",
    "float_satisfied.png",
    "float_slap_dizzy.png",
    "float_slap_shocked.png",
    "float_slap_spinning.png",
    "idle_blink.png",
    "idle_open.png",
    "judging.png",
    "pet_happy_1.png",
    "pet_happy_2.png",
    "pet_hearts.png",
    "playing_game.png",
    "proud.png",
    "satisfied_happy.png",
    "slap_dizzy.png",
    "slap_shocked.png",
    "slap_spinning.png",
    "surprised.png",
    "touching_ears_sad.png",
    "working_hard.png",
]

datas = [
    (os.path.join("assets", "sprites", sprite), os.path.join("assets", "sprites"))
    for sprite in sprite_files
]

# ---------------------------------------------------------------------------
# Hidden imports — modules PyInstaller can't auto-detect
# ---------------------------------------------------------------------------
hidden_imports = [
    "PyQt6.QtCore",
    "PyQt6.QtGui",
    "PyQt6.QtWidgets",
]

# Platform-specific hidden imports
if sys.platform == "win32":
    hidden_imports += ["win32gui", "win32api", "win32con"]
elif sys.platform == "darwin":
    hidden_imports += ["AppKit", "Foundation"]

# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude heavy packages we don't need — keeps the bundle smaller
        "onnxruntime",
        "rembg",
        "numpy",
        "PIL",
        "cv2",
        "torch",
        "tensorflow",
        "matplotlib",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# ---------------------------------------------------------------------------
# Windows: single .exe file
# Mac:     single binary inside .app bundle (see BUNDLE below)
# ---------------------------------------------------------------------------
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="DesktopPet",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,       # No terminal window pops up
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Windows only: set the .exe icon
    icon="assets/icon.ico",
)

# ---------------------------------------------------------------------------
# Mac only: wrap the exe in a proper .app bundle
# ---------------------------------------------------------------------------
if sys.platform == "darwin":
    app = BUNDLE(
        exe,
        name="DesktopPet.app",
        icon="assets/icon.icns",
        bundle_identifier="com.desktoppet.app",
        info_plist={
            # Allow the app to stay on top and be seen on all Spaces
            "NSHighResolutionCapable": True,
            "LSUIElement": True,        # Hides the app from the Dock (background app style)
            "CFBundleName": "Desktop Pet",
            "CFBundleDisplayName": "Desktop Pet",
            "CFBundleVersion": "1.0.0",
            "CFBundleShortVersionString": "1.0",
            # Needed on Mac to access accessibility/window info
            "NSAppleEventsUsageDescription": "Desktop Pet needs this to detect which app is active.",
        },
    )
