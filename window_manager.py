# window_manager.py
# ---------------------------------------------------------------------------
# Creates and manages the main application window.
#
# Key behaviours:
#   - Fully transparent background (only the sprite is visible).
#   - Always stays on top of other windows.
#   - Has no title bar, borders, or window chrome.
#   - Can be dragged around the desktop by clicking and dragging.
#   - Repaints itself whenever character.py signals a new animation frame.
#   - Can show/hide a speech bubble above the character.
# ---------------------------------------------------------------------------

from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QColor, QFont, QFontMetrics
from PyQt6.QtCore import Qt, QPoint, QRect

import config
from character import Character


class PetWindow(QWidget):
    """The transparent, frameless, always-on-top window for the desktop pet."""

    def __init__(self, character: Character):
        super().__init__()
        self.character = character

        # --- Drag state ---
        self._drag_offset = QPoint(0, 0)
        self._is_dragging = False

        # --- Speech bubble state ---
        self._bubble_text = None    # None = bubble is hidden, string = bubble is showing
        
        # --- Callbacks for drag events ---
        self.on_drag_start = None   # Called when drag begins
        self.on_dragged = None      # Called when drag ends (release)

        # Connect to character's animation — repaint every time a new frame arrives
        self.character.on_frame_changed = self.update

        self._setup_window()
        self._set_starting_position()

    # ------------------------------------------------------------------
    # Window setup
    # ------------------------------------------------------------------
    def _setup_window(self):
        """Configure the window to be transparent, frameless, and on top."""
        flags = (
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        # On Mac, Tool windows don't always stay on top across spaces.
        # WindowDoesNotAcceptFocus prevents the pet stealing keyboard focus.
        import sys
        if sys.platform == "darwin":
            flags |= Qt.WindowType.WindowDoesNotAcceptFocus

        self.setWindowFlags(flags)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # On Mac, also set window level via native call so it stays above the Dock
        if sys.platform == "darwin":
            try:
                from AppKit import NSApp, NSFloatingWindowLevel
                self.show()  # window must exist before we can set level
                # Get the native NSWindow and raise its level
                nswindow = NSApp.windows()[-1]
                nswindow.setLevel_(NSFloatingWindowLevel)
            except Exception:
                pass  # AppKit not available — default flags still work fine

        self.setWindowTitle("Desktop Pet")
        self.setFixedSize(900, 900)

    def _set_starting_position(self):
        """Place the window at the configured starting position, or centre it."""
        if config.WINDOW_START_X is not None and config.WINDOW_START_Y is not None:
            self.move(config.WINDOW_START_X, config.WINDOW_START_Y)
        else:
            screen_geom = QApplication.primaryScreen().geometry()
            x = (screen_geom.width() - config.WINDOW_WIDTH) // 2
            y = (screen_geom.height() - config.WINDOW_HEIGHT) // 2
            self.move(x, y)

    # ------------------------------------------------------------------
    # Speech bubble — public interface for mode_manager
    # ------------------------------------------------------------------
    def show_speech_bubble(self, text: str):
        """Show a speech bubble with the given text above the character."""
        self._bubble_text = text
        self.update()

    def hide_speech_bubble(self):
        """Hide the speech bubble."""
        self._bubble_text = None
        self.update()

    # ------------------------------------------------------------------
    # Painting
    # ------------------------------------------------------------------
    def paintEvent(self, event):
        """Draw the character and optionally the speech bubble."""
        painter = QPainter(self)

        # Character draws at the center of the window
        char_x = (self.width() - config.WINDOW_WIDTH) // 2
        char_y = (self.height() - config.WINDOW_HEIGHT) // 2
        painter.drawPixmap(char_x, char_y, self.character.get_pixmap())

        # Draw speech bubble around the character if visible
        if self._bubble_text:
            self._paint_bubble(painter, char_x, char_y)

        painter.end()

    def _paint_bubble(self, painter: QPainter, char_x: int, char_y: int):
        """
        Draw a white speech bubble with a tail pointing to the character.
        The bubble auto-sizes based on text length.
        Places bubble around the character using priority: above > left > right > below.
        """
        # --- Measure the text so we can size the bubble ---
        font = QFont("Comic Sans MS", 12, QFont.Weight.Bold)
        painter.setFont(font)
        metrics = QFontMetrics(font)
        # Use 350px max width - wide enough for longest messages on one line
        text_rect = metrics.boundingRect(0, 0, 350, 200,
                                         Qt.TextFlag.TextWordWrap, self._bubble_text)
        bubble_w = text_rect.width() + 40  # padding for cloud puffs
        bubble_h = text_rect.height() + 28

        # --- Calculate character's center in screen coordinates ---
        char_center_screen_x = self.x() + char_x + config.WINDOW_WIDTH // 2
        char_center_screen_y = self.y() + char_y + config.WINDOW_HEIGHT // 2

        # --- Get screen bounds ---
        screen = QApplication.primaryScreen().geometry()
        screen_w = screen.width()
        screen_h = screen.height()

        # --- Calculate where bubble WOULD be placed in each direction ---
        # Then check if that placement would stay on-screen
        
        # Above: bubble top would be at char_y - bubble_h - 15
        bubble_top_if_above = self.y() + char_y - bubble_h - 15
        can_fit_above = bubble_top_if_above >= 0
        
        # Left: bubble left edge would be at char_x - bubble_w - 15
        bubble_left_if_left = self.x() + char_x - bubble_w - 15
        can_fit_left = bubble_left_if_left >= 0
        
        # Right: bubble right edge would be at char_x + WINDOW_WIDTH + 15 + bubble_w
        bubble_right_if_right = self.x() + char_x + config.WINDOW_WIDTH + 15 + bubble_w
        can_fit_right = bubble_right_if_right <= screen_w
        
        # Below: bubble bottom would be at char_y + WINDOW_HEIGHT + 15 + bubble_h
        bubble_bottom_if_below = self.y() + char_y + config.WINDOW_HEIGHT + 15 + bubble_h
        can_fit_below = bubble_bottom_if_below <= screen_h

        # --- Decide placement using priority order: above > left > right > below ---
        
        if can_fit_above:
            # Place above
            bubble_x = char_x + (config.WINDOW_WIDTH - bubble_w) // 2
            bubble_y = char_y - bubble_h - 15
            tail_x = char_x + config.WINDOW_WIDTH // 2
            tail_y = bubble_y + bubble_h
            tail_direction = "down"
        elif can_fit_left:
            # Place left
            bubble_x = char_x - bubble_w - 15
            bubble_y = char_y + (config.WINDOW_HEIGHT - bubble_h) // 2
            tail_x = bubble_x + bubble_w
            tail_y = bubble_y + bubble_h // 2
            tail_direction = "right"
        elif can_fit_right:
            # Place right
            bubble_x = char_x + config.WINDOW_WIDTH + 15
            bubble_y = char_y + (config.WINDOW_HEIGHT - bubble_h) // 2
            tail_x = bubble_x
            tail_y = bubble_y + bubble_h // 2
            tail_direction = "left"
        else:
            # Place below
            bubble_x = char_x + (config.WINDOW_WIDTH - bubble_w) // 2
            bubble_y = char_y + config.WINDOW_HEIGHT + 15
            tail_x = char_x + config.WINDOW_WIDTH // 2
            tail_y = bubble_y
            tail_direction = "up"

        # --- Draw cute fluffy cloud bubble ---
        # Cloud made of overlapping circles in soft pastel color
        cloud_color = QColor(255, 240, 245, 240)  # soft pink tint
        painter.setBrush(cloud_color)
        painter.setPen(Qt.PenStyle.NoPen)  # no outline for softer look
        
        # Main cloud body (large rounded rect)
        painter.drawRoundedRect(bubble_x, bubble_y, bubble_w, bubble_h, bubble_h // 2, bubble_h // 2)
        
        # Add fluffy circles around the edges to make it cloud-like
        circle_size = bubble_h // 3
        # Top-left puff
        painter.drawEllipse(bubble_x - circle_size // 3, bubble_y - circle_size // 4, circle_size, circle_size)
        # Top-right puff
        painter.drawEllipse(bubble_x + bubble_w - circle_size * 2 // 3, bubble_y - circle_size // 4, circle_size, circle_size)
        # Bottom-left puff
        painter.drawEllipse(bubble_x - circle_size // 4, bubble_y + bubble_h - circle_size * 3 // 4, circle_size, circle_size)
        # Bottom-right puff
        painter.drawEllipse(bubble_x + bubble_w - circle_size * 3 // 4, bubble_y + bubble_h - circle_size * 3 // 4, circle_size, circle_size)

        # --- Draw cute fluffy tail (cloud puffs creating path to character) ---
        from PyQt6.QtGui import QPolygon
        
        if tail_direction == "down":
            # Cloud puffs descending from bubble to character
            puff1_x, puff1_y = tail_x, tail_y + 2
            puff2_x, puff2_y = tail_x - 5, tail_y + 10
            puff3_x, puff3_y = tail_x + 3, tail_y + 18
            painter.drawEllipse(puff1_x - 7, puff1_y - 7, 14, 14)
            painter.drawEllipse(puff2_x - 5, puff2_y - 5, 10, 10)
            painter.drawEllipse(puff3_x - 4, puff3_y - 4, 8, 8)
        elif tail_direction == "up":
            # Cloud puffs ascending from bubble to character
            puff1_x, puff1_y = tail_x, tail_y - 2
            puff2_x, puff2_y = tail_x - 5, tail_y - 10
            puff3_x, puff3_y = tail_x + 3, tail_y - 18
            painter.drawEllipse(puff1_x - 7, puff1_y - 7, 14, 14)
            painter.drawEllipse(puff2_x - 5, puff2_y - 5, 10, 10)
            painter.drawEllipse(puff3_x - 4, puff3_y - 4, 8, 8)
        elif tail_direction == "left":
            # Cloud puffs going left from bubble to character
            puff1_x, puff1_y = tail_x - 2, tail_y
            puff2_x, puff2_y = tail_x - 10, tail_y - 5
            puff3_x, puff3_y = tail_x - 18, tail_y + 3
            painter.drawEllipse(puff1_x - 7, puff1_y - 7, 14, 14)
            painter.drawEllipse(puff2_x - 5, puff2_y - 5, 10, 10)
            painter.drawEllipse(puff3_x - 4, puff3_y - 4, 8, 8)
        else:  # right
            # Cloud puffs going right from bubble to character
            puff1_x, puff1_y = tail_x + 2, tail_y
            puff2_x, puff2_y = tail_x + 10, tail_y - 5
            puff3_x, puff3_y = tail_x + 18, tail_y + 3
            painter.drawEllipse(puff1_x - 7, puff1_y - 7, 14, 14)
            painter.drawEllipse(puff2_x - 5, puff2_y - 5, 10, 10)
            painter.drawEllipse(puff3_x - 4, puff3_y - 4, 8, 8)

        # --- Draw the cute text ---
        painter.setPen(QColor(200, 100, 150))  # soft pink-purple color
        painter.drawText(
            QRect(bubble_x + 15, bubble_y + 12, bubble_w - 30, bubble_h - 24),
            Qt.TextFlag.TextWordWrap | Qt.AlignmentFlag.AlignCenter,
            self._bubble_text
        )

    # ------------------------------------------------------------------
    # Dragging
    # ------------------------------------------------------------------
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_offset = event.position().toPoint()
            self._is_dragging = True
            
            # Notify drag start - show dragged_by_ear animation
            if self.on_drag_start:
                self.on_drag_start()
            
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton and self._is_dragging:
            new_pos = event.globalPosition().toPoint() - self._drag_offset
            self.move(new_pos)
            # Keep dragged animation playing during entire drag
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Only call on_dragged callback when drag ENDS (mouse released)
            # This triggers the return-to-edge behavior
            if self._is_dragging and self.on_dragged:
                self.on_dragged(self.pos())
            
            self._is_dragging = False
            event.accept()
        else:
            super().mouseReleaseEvent(event)
