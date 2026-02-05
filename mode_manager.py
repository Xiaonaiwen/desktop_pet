# mode_manager.py
# ---------------------------------------------------------------------------
# Manages the current mode of the desktop pet and coordinates between
# the other systems (character, window, app_monitor).
#
# Phase 4 implements Supervisor Mode only.
# Phases 5 and 6 will add Wanderer and Interactive modes here.
# ---------------------------------------------------------------------------

from PyQt6.QtCore import QTimer

import config
from character import Character
from window_manager import PetWindow
from app_monitor import AppMonitor


class ModeManager:
    """
    Owns the current mode and runs the logic for it.
    Right now only Supervisor mode exists — more will be added later.
    """

    def __init__(self, character: Character, window: PetWindow):
        self.character = character
        self.window = window
        self.app_monitor = AppMonitor()

        # Timer that periodically checks the active window
        self._check_timer = QTimer()
        self._check_timer.setInterval(config.APP_CHECK_INTERVAL_MS)
        self._check_timer.timeout.connect(self._on_supervisor_tick)

        # Timer that hides the speech bubble after its duration
        self._bubble_timer = QTimer()
        self._bubble_timer.setInterval(config.SPEECH_BUBBLE_DURATION_MS)
        self._bubble_timer.timeout.connect(self._hide_bubble)

        # Start in Supervisor mode by default
        self.start_supervisor()

    # ------------------------------------------------------------------
    # Supervisor Mode
    # ------------------------------------------------------------------
    def start_supervisor(self):
        """Enter Supervisor mode — sit still and watch what apps are open."""
        print("[mode_manager] Entering Supervisor mode")
        self._check_timer.start()

    def _on_supervisor_tick(self):
        """
        Called every APP_CHECK_INTERVAL_MS.
        Asks app_monitor if the active window changed.
        If it did, switches the character's animation and shows a speech bubble.
        """
        reaction = self.app_monitor.check()

        if reaction is None:
            return  # nothing changed, do nothing

        animation_name, speech_text = reaction

        # Switch the character to the reaction animation
        self.character.set_animation(animation_name)

        # Show or hide the speech bubble
        if speech_text:
            self.window.show_speech_bubble(speech_text)
            # Auto-hide after the configured duration
            self._bubble_timer.start()
        else:
            self._hide_bubble()

    def _hide_bubble(self):
        """Hide the speech bubble and stop the bubble timer."""
        self._bubble_timer.stop()
        self.window.hide_speech_bubble()
        # After the bubble disappears, go back to idle
        self.character.set_animation("idle")
