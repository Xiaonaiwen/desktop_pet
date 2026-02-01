# character.py
# ---------------------------------------------------------------------------
# Responsible for loading sprite images and providing them to the window.
# Later phases will add animation frames, pose switching, etc. here.
# ---------------------------------------------------------------------------

import os
from PyQt6.QtGui import QPixmap, QColor, QPainter
from PyQt6.QtCore import Qt

import config


class Character:
    """Loads and manages the current sprite for the desktop pet."""

    def __init__(self):
        self.sprite_path = os.path.join(config.SPRITES_DIR, config.DEFAULT_SPRITE)
        self.pixmap = self._load_sprite()

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------
    def get_pixmap(self) -> QPixmap:
        """Return the current sprite as a QPixmap ready to paint."""
        return self.pixmap

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------
    def _load_sprite(self) -> QPixmap:
        """
        Try to load the sprite PNG.
        If the file doesn't exist yet (sprites haven't been generated),
        fall back to a coloured placeholder rectangle so development
        can continue without blocking on assets.
        """
        if os.path.isfile(self.sprite_path):
            pixmap = QPixmap(self.sprite_path)
            if not pixmap.isNull():
                # Scale to the configured window size
                pixmap = pixmap.scaled(
                    config.WINDOW_WIDTH,
                    config.WINDOW_HEIGHT,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                return pixmap

        # --- Placeholder fallback ---
        print(f"[character] Sprite not found at '{self.sprite_path}' — using placeholder.")
        return self._make_placeholder()

    def _make_placeholder(self) -> QPixmap:
        """
        Draw a simple coloured rectangle with a label.
        This is purely for development so you can see the window working
        before real sprites are ready.
        """
        pixmap = QPixmap(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)

        # Background rounded rectangle
        r, g, b = config.PLACEHOLDER_COLOR
        painter.setBrush(QColor(r, g, b, 200))          # slightly transparent
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(10, 10, config.WINDOW_WIDTH - 20, config.WINDOW_HEIGHT - 20, 20, 20)

        # Label text
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "🐾 Desktop Pet\n(placeholder)")

        painter.end()
        return pixmap
