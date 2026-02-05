# app_monitor.py
# ---------------------------------------------------------------------------
# Detects what application is currently active on Windows,
# and looks up what reaction the pet should have.
#
# Uses pywin32 (win32gui) to call the Windows API directly —
# this is the only way to reliably get the active window title on Windows.
# ---------------------------------------------------------------------------

import win32gui

import config


class AppMonitor:
    """Polls the active window and returns the matching reaction."""

    def __init__(self):
        self._last_title = ""          # cache: avoid re-triggering on the same window
        self._last_reaction = None     # the reaction we last returned

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------
    def check(self) -> tuple | None:
        """
        Check the currently active window.
        Returns a (animation_name, speech_text) tuple if the active app
        changed since last check, or None if nothing changed.

        This is called by mode_manager on a timer — not continuously.
        """
        title = self._get_active_window_title()

        # Only trigger a new reaction if the window actually changed
        if title == self._last_title:
            return None

        self._last_title = title
        reaction = self._match_reaction(title)
        self._last_reaction = reaction

        if reaction:
            print(f"[app_monitor] Active window: '{title}' → reaction: {reaction[0]}")
        else:
            print(f"[app_monitor] Active window: '{title}' → no match")

        return reaction

    # ------------------------------------------------------------------
    # Internal — Windows API
    # ------------------------------------------------------------------
    def _get_active_window_title(self) -> str:
        """
        Use win32gui to get the title bar text of the currently focused window.
        Returns an empty string if no window is focused (e.g. desktop).
        """
        hwnd = win32gui.GetForegroundWindow()
        if hwnd == 0:
            return ""
        return win32gui.GetWindowText(hwnd)

    # ------------------------------------------------------------------
    # Internal — reaction matching
    # ------------------------------------------------------------------
    def _match_reaction(self, title: str) -> tuple | None:
        """
        Compare the window title against APP_REACTIONS in config.
        Matching is case-insensitive. First match wins.

        Returns (animation_name, speech_text) or None if no match.
        speech_text can be None (meaning: change animation but don't show bubble).
        """
        title_lower = title.lower()

        for keyword, animation, speech in config.APP_REACTIONS:
            if keyword.lower() in title_lower:
                return (animation, speech)

        # No match at all — return idle with no bubble
        return ("idle", None)
