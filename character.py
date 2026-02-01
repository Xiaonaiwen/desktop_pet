# character.py
# ---------------------------------------------------------------------------
# Manages the character's sprite and animation.
#
# How animation works:
#   - An animation is a list of (image, duration) frames defined in config.py.
#   - A QTimer ticks every ANIMATION_TICK_MS (100ms).
#   - Each tick we check: has enough time passed to move to the next frame?
#     If yes, advance. If no, stay on the current frame.
#   - This lets each frame have its OWN duration (e.g. eyes-open lasts 600ms,
#     blink lasts 150ms) while still checking smoothly.
#   - When the last frame is reached, it loops back to frame 0.
# ---------------------------------------------------------------------------

import os
from PyQt6.QtGui import QPixmap, QColor, QPainter
from PyQt6.QtCore import Qt, QTimer, QElapsedTimer

import config


class Character:
    """Loads sprites and drives the animation loop."""

    def __init__(self):
        # --- Animation state ---
        self._current_anim_name = None   # e.g. "idle"
        self._frames = []                # list of (QPixmap, duration_ms) for current animation
        self._frame_index = 0            # which frame we're on right now
        self._frame_timer = QElapsedTimer()  # measures how long current frame has been showing

        # --- The Qt timer that drives animation ticks ---
        self._tick_timer = QTimer()
        self._tick_timer.setInterval(config.ANIMATION_TICK_MS)
        self._tick_timer.timeout.connect(self._on_tick)

        # --- Callback: window_manager connects here to know when to repaint ---
        # Set this to a function and it will be called every time the frame changes.
        self.on_frame_changed = None

        # Start with the default animation
        self.set_animation(config.DEFAULT_ANIMATION)
        self._tick_timer.start()

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------
    def get_pixmap(self) -> QPixmap:
        """Return the current frame's pixmap. Called by window_manager to draw."""
        if self._frames:
            return self._frames[self._frame_index][0]   # [0] = the QPixmap
        return self._make_placeholder("No frames")

    def set_animation(self, name: str):
        """
        Switch to a different animation by name (e.g. "idle", "walk_left").
        Loads all the frames defined in config.ANIMATIONS[name].
        """
        if name == self._current_anim_name:
            return  # already playing this one, do nothing

        self._current_anim_name = name
        self._frame_index = 0
        self._frame_timer.restart()
        self._frames = self._load_animation(name)
        print(f"[character] Playing animation: {name} ({len(self._frames)} frames)")

    # ------------------------------------------------------------------
    # Internal — animation tick
    # ------------------------------------------------------------------
    def _on_tick(self):
        """
        Called every ANIMATION_TICK_MS by the Qt timer.
        Checks if the current frame's duration has elapsed.
        If yes, advances to the next frame and notifies the window to repaint.
        """
        if not self._frames:
            return

        current_duration = self._frames[self._frame_index][1]  # [1] = duration_ms

        if self._frame_timer.elapsed() >= current_duration:
            # Advance to next frame (loop back to 0 at the end)
            self._frame_index = (self._frame_index + 1) % len(self._frames)
            self._frame_timer.restart()

            # Tell the window to repaint
            if self.on_frame_changed:
                self.on_frame_changed()

    # ------------------------------------------------------------------
    # Internal — loading
    # ------------------------------------------------------------------
    def _load_animation(self, name: str) -> list:
        """
        Load all frames for an animation from config.ANIMATIONS.
        Returns a list of (QPixmap, duration_ms) tuples.
        If any sprite file is missing, falls back to a placeholder pixmap
        for that frame so the animation still runs.
        """
        if name not in config.ANIMATIONS:
            print(f"[character] Animation '{name}' not found in config. Falling back to placeholder.")
            return [(self._make_placeholder(f"Unknown: {name}"), 1000)]

        frames = []
        all_missing = True

        for filename, duration in config.ANIMATIONS[name]:
            path = os.path.join(config.SPRITES_DIR, filename)

            if os.path.isfile(path):
                pixmap = QPixmap(path)
                if not pixmap.isNull():
                    pixmap = pixmap.scaled(
                        config.WINDOW_WIDTH,
                        config.WINDOW_HEIGHT,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                    frames.append((pixmap, duration))
                    all_missing = False
                    continue

            # File missing or failed to load — use a placeholder for this frame
            frames.append((self._make_placeholder(filename), duration))

        if all_missing:
            print(f"[character] No sprite files found for '{name}' — using animated placeholder.")

        return frames

    # ------------------------------------------------------------------
    # Internal — placeholder drawing
    # ------------------------------------------------------------------
    def _make_placeholder(self, label: str) -> QPixmap:
        """
        Draw a placeholder rectangle for a single frame.
        The label shows which sprite file it's standing in for,
        so you can see the animation cycling through frames.
        """
        pixmap = QPixmap(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)

        # Background rounded rectangle
        r, g, b = config.PLACEHOLDER_COLOR
        painter.setBrush(QColor(r, g, b, 200))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(10, 10, config.WINDOW_WIDTH - 20, config.WINDOW_HEIGHT - 20, 20, 20)

        # Title
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(pixmap.rect().adjusted(0, 20, 0, -40), Qt.AlignmentFlag.AlignCenter, "🐾 Desktop Pet")

        # Frame label — shows which sprite this placeholder is standing in for
        painter.setPen(QColor(200, 200, 255))
        painter.drawText(pixmap.rect().adjusted(0, 40, 0, 0), Qt.AlignmentFlag.AlignCenter, f"[{label}]")

        painter.end()
        return pixmap
