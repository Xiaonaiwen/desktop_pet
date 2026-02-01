# window_manager.py
# ---------------------------------------------------------------------------
# Creates and manages the main application window.
#
# Key behaviours:
#   - Fully transparent background (only the sprite is visible).
#   - Always stays on top of other windows.
#   - Has no title bar, borders, or window chrome.
#   - Can be dragged around the desktop by clicking and dragging.
# ---------------------------------------------------------------------------

from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt, QPoint

import config
from character import Character


class PetWindow(QWidget):
    """The transparent, frameless, always-on-top window for the desktop pet."""

    def __init__(self, character: Character):
        super().__init__()
        self.character = character

        # Track mouse drag offset so dragging feels natural
        self._drag_offset = QPoint(0, 0)

        self._setup_window()
        self._set_starting_position()

    # ------------------------------------------------------------------
    # Window setup
    # ------------------------------------------------------------------
    def _setup_window(self):
        """Configure the window to be transparent, frameless, and on top."""
        # Remove title bar and borders
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint      # no title bar / border
            | Qt.WindowType.WindowStaysOnTopHint   # always on top
            | Qt.WindowType.Tool                   # doesn't appear in taskbar
        )

        # Make the window background fully transparent
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Set window size to match sprite size
        self.setFixedSize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

        # Remove the window title (not visible, but good practice)
        self.setWindowTitle("Desktop Pet")

    def _set_starting_position(self):
        """Place the window at the configured starting position, or centre it."""
        if config.WINDOW_START_X is not None and config.WINDOW_START_Y is not None:
            self.move(config.WINDOW_START_X, config.WINDOW_START_Y)
        else:
            # Centre on screen
            screen_geom = QApplication.primaryScreen().geometry()
            x = (screen_geom.width() - config.WINDOW_WIDTH) // 2
            y = (screen_geom.height() - config.WINDOW_HEIGHT) // 2
            self.move(x, y)

    # ------------------------------------------------------------------
    # Painting
    # ------------------------------------------------------------------
    def paintEvent(self, event):
        """Draw the character sprite onto the window each frame."""
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.character.get_pixmap())
        painter.end()

    # ------------------------------------------------------------------
    # Dragging — lets the user move the pet around the desktop
    # ------------------------------------------------------------------
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Record the offset between where we clicked and the window's top-left
            self._drag_offset = event.position().toPoint()
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            # Move window so the mouse stays at the same point on the sprite
            new_pos = event.globalPosition().toPoint() - self._drag_offset
            self.move(new_pos)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            event.accept()
        else:
            super().mouseReleaseEvent(event)
